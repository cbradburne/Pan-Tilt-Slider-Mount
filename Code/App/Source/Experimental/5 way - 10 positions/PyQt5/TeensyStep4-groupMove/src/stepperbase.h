#pragma once

#include "Arduino.h"
#pragma push_macro("abs")
#undef abs

#include "timers/interfaces.h"
#include "timers/timerfactory.h"
#include <algorithm>
#include <cstdint>
#include <string>

namespace TS4
{
    
    class StepperBase
    {
     public:
        std::string name;
        bool isMoving = false;
        void emergencyStop();
        void overrideSpeed(float factor);


     protected:
        StepperBase(const int stepPin, const int dirPin);

        void startMoveTo(int32_t s_tgt, int32_t v_e, uint32_t v_max, uint32_t a);
        void startMoveToGroup(int32_t s_tgt, int32_t v_e, uint32_t v_max, uint32_t a);
        void startRotate(int32_t v_max, uint32_t a);
        void startStopping(int32_t va_end, uint32_t a);


        inline void setDir(int d);
        int32_t dir;
        int32_t vDir;

        volatile int32_t pos;
        volatile int32_t target;

        int32_t s_tgt;
        int32_t v_tgt, v_tgt_orig;
        int64_t v_tgt_sqr;

        int32_t twoA;
        int32_t decStart, accEnd;

        volatile int32_t s;
        volatile int32_t v;
        volatile int64_t v_sqr;

        inline void doStep();
        inline void doGroupStep();

        const int stepPin, dirPin;

        ITimer* stpTimer;
        inline void stepISR();
        inline void stepGroupISR();
        inline void rotISR();
        inline void resetISR();
        inline void resetGroupISR();

        enum class mode_t {
            group,
            async,
            stopping,
        } mode = mode_t::async;

        // Bresenham:
        StepperBase* next = nullptr; // linked list of steppers, maintained from outside
        int32_t A, B;                // Bresenham parameters (https://en.wikipedia.org/wiki/Bresenham)

        friend class StepperGroupBase;
    };

    //========================================================================================================
    // Inline implementation
    //========================================================================================================

    void StepperBase::doStep()
    {
        digitalWriteFast(stepPin, HIGH);
        s += 1;
        pos += dir;

        if (mode = mode_t::group) {
            StepperBase* stepper = next;

            while (stepper != nullptr)                              // move slave motors if required
            {
                if (stepper->B >= 0)
                {
                    digitalWriteFast(stepper->stepPin, HIGH);
                    stepper->pos += stepper->dir;
                    stepper->B -= this->A;
                }
                stepper->B += stepper->A;
                stepper = stepper->next;
            }
        }
    }

    void StepperBase::doGroupStep()
    {
        digitalWriteFast(stepPin, HIGH);
        s += 1;
        pos += dir;

        StepperBase* stepper = next;

        while (stepper != nullptr)                              // move slave motors if required
        {
            if (stepper->B >= 0)
            {
                digitalWriteFast(stepper->stepPin, HIGH);
                stepper->pos += stepper->dir;
                stepper->B -= this->A;
            }
            stepper->B += stepper->A;
            stepper = stepper->next;
        }
    }

    void StepperBase::stepISR()
    {
        if (mode == mode_t::stopping){
            mode = mode_t::async;
            if (s < accEnd)                                     // still accelerating
            { 
                accEnd = decStart = 0;                          // start deceleration
                s_tgt             = 2 * s;                      // we need the same way to decelerate as we traveled so far
            } else if (s < decStart)                            // constant speed phase
            {
                decStart = 0;                                   // start deceleration
                s_tgt    = s + accEnd;                          // normal deceleration distance  ds = distance to end
            }
        }

        if (s < accEnd)                                         // accelerating
        {
            v = signum(v_sqr) * sqrtf(std::abs(v_sqr));
            v_sqr += twoA;
            stpTimer->updateFrequency(std::abs(v));
            doStep();
        } else if (s < decStart)                                // constant speed
        {
            v = std::min(sqrtf(v_sqr), sqrtf(v_tgt_sqr));
            stpTimer->updateFrequency(v);
            doStep();
        } else if (s < s_tgt)                                   // decelerating
        {
            v_sqr -= twoA;
            v = signum(v_sqr) * sqrtf(std::abs(v_sqr));
            stpTimer->updateFrequency(std::abs(v));
            doStep();
        } else                                                  // target reached
        {
            stpTimer->stop();
            TimerFactory::returnTimer(stpTimer);
            stpTimer = nullptr;
            isMoving = false;
        }
    }

    void StepperBase::stepGroupISR()
    {
        if (mode == mode_t::stopping){
            mode = mode_t::group;
            if (s < accEnd)                                     // still accelerating
            { 
                accEnd = decStart = 0;                          // start deceleration
                s_tgt             = 2 * s;                      // we need the same way to decelerate as we traveled so far
            } else if (s < decStart)                            // constant speed phase
            {
                decStart = 0;                                   // start deceleration
                s_tgt    = s + accEnd;                          // normal deceleration distance  ds = distance to end
            }
        }

        if (s < accEnd)                                         // accelerating
        {
            v = signum(v_sqr) * sqrtf(std::abs(v_sqr));
            v_sqr += twoA;
            stpTimer->updateFrequency(std::abs(v));
            doGroupStep();
        } else if (s < decStart)                                // constant speed
        {
            v = std::min(sqrtf(v_sqr), sqrtf(v_tgt_sqr));
            stpTimer->updateFrequency(v);
            doGroupStep();
        } else if (s < s_tgt)                                   // decelerating
        {
            v_sqr -= twoA;
            v = signum(v_sqr) * sqrtf(std::abs(v_sqr));
            stpTimer->updateFrequency(std::abs(v));
            doGroupStep();
        } else                                                  // target reached
        {
            stpTimer->stop();
            TimerFactory::returnTimer(stpTimer);
            stpTimer = nullptr;
            isMoving = false;
        }
    }

    void StepperBase::rotISR()
    {
        mode = mode_t::async;
        int32_t v_abs;

        if (std::abs(v_sqr - v_tgt_sqr) > twoA)                 // target speed not yet reached
        {
            v_sqr += vDir * twoA;

            dir = signum(v_sqr);
            digitalWriteFast(dirPin, dir > 0 ? HIGH : LOW);
            delayMicroseconds(5);

            v_abs = sqrtf(std::abs(v_sqr));
            stpTimer->updateFrequency(v_abs);
            doStep();
        } else
        {
            dir = signum(v_sqr);
            digitalWriteFast(dirPin, dir > 0 ? HIGH : LOW);
            delayMicroseconds(5);

            if (v_tgt != 0)
            {
                v_abs = sqrtf(std::abs(v_sqr));
                stpTimer->updateFrequency(v_abs);
                doStep();
            } else
            {
                stpTimer->stop();
                TimerFactory::returnTimer(stpTimer);
                stpTimer = nullptr;
                isMoving = false;
                v_sqr = 0;
                
                //mode = mode_t::group;
            }
        }
    }

    void StepperBase::resetISR()
    {
        StepperBase* stepper = this;
        while (stepper != nullptr)
        {
            digitalWriteFast(stepper->stepPin, LOW);
            stepper = stepper->next;
        }
    }
    void StepperBase::resetGroupISR()
    {
        StepperBase* stepper = this;
        while (stepper != nullptr)
        {
            digitalWriteFast(stepper->stepPin, LOW);
            stepper = stepper->next;
        }
    }
}
#pragma pop_macro("abs")
