#include "Arduino.h"

#pragma push_macro("abs")
#undef abs

#include "stepperbase.h"
#include <algorithm>

namespace TS4
{
    StepperBase::StepperBase(int _stepPin, int _dirPin)
        : s(0), v(0), v_sqr(0), stepPin(_stepPin), dirPin(_dirPin)
    {
        pinMode(stepPin, OUTPUT);
        pinMode(dirPin, OUTPUT);
    }

    void StepperBase::startRotate(int32_t _v_tgt, uint32_t a)
    {
        v_tgt     = _v_tgt;
        v_tgt_orig = v_tgt;
        v_tgt_sqr = (int64_t)signum(v_tgt) * v_tgt * v_tgt;
        vDir      = (int32_t)signum(v_tgt_sqr - v_sqr);
        twoA      = 2 * a;

        if (!isMoving)
        {
            stpTimer = TimerFactory::makeTimer();
            stpTimer->setPulseParams(8, stepPin);
            stpTimer->attachCallbacks([this] { rotISR(); }, [this] { resetISR(); });
            v_sqr = vDir * 200 * 200;
            mode  = mode_t::async;
            stpTimer->start();
            isMoving = true;
        }
    }

    void StepperBase::startMoveTo(int32_t _s_tgt, int32_t v_e, uint32_t v_tgt, uint32_t a)
    {
        s          = 0;
        int32_t ds = std::abs(_s_tgt - pos);
        s_tgt      = ds;

        dir = signum(_s_tgt - pos);
        digitalWriteFast(dirPin, dir > 0 ? HIGH : LOW);
        delayMicroseconds(5);

        twoA = 2 * a;
        // v_sqr      = (int64_t) v * v;
        v_sqr     = 0;
        v         = 0;
        v_tgt_orig = v_tgt;
        v_tgt_sqr = (int64_t)v_tgt * v_tgt;

        int64_t accLength = (v_tgt_sqr - v_sqr) / twoA + 1;
        if (accLength >= ds / 2) accLength = ds / 2;

        accEnd   = accLength - 1;
        decStart = s_tgt - accLength;

        if (!isMoving)
        {
            stpTimer = TimerFactory::makeTimer();

            stpTimer->attachCallbacks([this] { stepISR(); }, [this] { resetISR(); });
            stpTimer->setPulseParams(8, stepPin);
            isMoving = true;
            v_sqr    = 200 * 200;
            stpTimer->start();
        }
    }

    void StepperBase::startMoveToGroup(int32_t _s_tgt, int32_t v_e, uint32_t v_tgt, uint32_t a)
    {
        s          = 0;
        int32_t ds = std::abs(_s_tgt - pos);
        s_tgt      = ds;

        dir = signum(_s_tgt - pos);
        digitalWriteFast(dirPin, dir > 0 ? HIGH : LOW);
        delayMicroseconds(5);

        twoA = 2 * a;
        v_sqr     = 0;
        v         = 0;
        v_tgt_orig = v_tgt;
        v_tgt_sqr = (int64_t)v_tgt * v_tgt;

        int64_t accLength = (v_tgt_sqr - v_sqr) / twoA + 1;
        if (accLength >= ds / 2) accLength = ds / 2;

        accEnd   = accLength - 1;
        decStart = s_tgt - accLength;

        if (!isMoving)
        {
            stpTimer = TimerFactory::makeTimer();

            stpTimer->attachCallbacks([this] { stepGroupISR(); }, [this] { resetGroupISR(); });
            stpTimer->setPulseParams(8, stepPin);
            isMoving = true;
            v_sqr    = 200 * 200;
            mode     = mode_t::target;
            stpTimer->start();
        }
    }

    void StepperBase::startStopping(int32_t v_end, uint32_t a)
    {
        if (mode == mode_t::async){
            mode = mode_t::stopping;
            startRotate(v_end, a);
            mode = mode_t::stopping;
        } else {
            mode = mode_t::stopping;
        }
    }

    void StepperBase::emergencyStop()
    {
        stpTimer->stop();
        TimerFactory::returnTimer(stpTimer);
        stpTimer = nullptr;
        isMoving = false;
        v_sqr    = 0;
    }

    void StepperBase::overrideSpeed(float factor)
    {
        if (mode == mode_t::async)
        {
            noInterrupts();
            v_tgt =v_tgt_orig * factor;
            v_tgt_sqr = (int64_t)signum(v_tgt) * v_tgt * v_tgt;
            vDir      = (int32_t)signum(v_tgt_sqr - v_sqr);
            interrupts();
        }
    }
}

#pragma pop_macro("abs")