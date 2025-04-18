#pragma push_macro("abs")
#undef abs

#include "teensystep4.h"
#include "timers/timerfactory.h"
#include "timers/interfaces.h"
#include "timers/Teensy4/TMR/TMR.h"


namespace TS4
{
    void begin(bool useDefaultModule)
    {
        if(useDefaultModule)
        {
            TimerFactory::attachModule(new TMRModule<3>());
            TimerFactory::attachModule(new TMRModule<0>()); // added for more than 4 motors, remove to restore to original file
        }
    }
}

#pragma pop_macro("abs")