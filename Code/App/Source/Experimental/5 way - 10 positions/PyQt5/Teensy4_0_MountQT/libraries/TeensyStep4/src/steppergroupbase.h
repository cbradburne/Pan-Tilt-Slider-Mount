#pragma once
#include "Arduino.h"

#pragma push_macro("abs")
#undef abs

#include "stepper.h"
#include <vector>

namespace TS4
{
    class StepperGroupBase
    {
     public:
        void startMove()
        {
            if (steppers.empty()) return;

            auto deltaSorter = [](Stepper* a, Stepper* b) { return std::abs(a->target - a->pos) > std::abs(b->target - b->pos); };

            std::vector<Stepper*> sorted = steppers;                    // copy stepper list..
            std::sort(sorted.begin(), sorted.end(), deltaSorter);       // ...and sort by "steps to do"

            leadStepper = sorted[0]; // this stepper will lead the movement, steps of the other motors are calculated by Bresenham algorithm

            leadStepper->A       = std::abs(leadStepper->target - leadStepper->pos);
            //Serial.printf("%s tgt:%d A:%d B:%d\n", leadStepper->name.c_str(), leadStepper->target, leadStepper->A, leadStepper->B);
            

            for (unsigned i = 1; i < sorted.size(); i++)                // loop through the dependent motors
            {
                Stepper* stepper    = sorted[i];                        //
                int32_t delta       = stepper->target - stepper->pos;   //
                sorted[i - 1]->next = stepper;                          // set up linked list
                stepper->A          = std::abs(delta);                  //
                stepper->B          = 2 * stepper->A - leadStepper->A;  // set bresenham params for dependent steppers
                stepper->dir        = (delta >= 0) ? 1 : -1;
                digitalWriteFast(stepper->dirPin, delta >= 0 ? HIGH : LOW);
                // Serial.printf("%s tgt:%d A:%d B:%d\n", stepper->name.c_str(), stepper->target, stepper->A, stepper->B);
                // Serial.flush();
            }
            sorted[sorted.size() - 1]->next = nullptr;                  // end of linked list
            sorted[0]->moveAsync();                                     // start lead stepper
        }

     protected:
        std::vector<Stepper*> steppers;
        Stepper* leadStepper;
    };
}

#pragma pop_macro("abs")