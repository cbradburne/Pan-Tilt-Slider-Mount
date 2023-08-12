//  Receive Serial data, and process


void SerialData(void) {
  char instruction;
  if (Serial.available() > 0) {
    instruction = Serial.read();
    if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);  //wait to make sure all data in the Serial2 message has arived
      instruction = Serial.read();
      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial.read();
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial.available()) {                    //set elemetns of stringText to the Serial2 values sent
          char digit = Serial.read();                   //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial2Flush();                            //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);  //converts stringText to an int
      } else {
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial.available()) {                    //set elemetns of stringText to the Serial2 values sent
          char digit = Serial.read();                   //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial2Flush();                              //Clear any excess data in the Serial2 buffer
        SerialCommandValueInt = atoi(stringText);    //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);  //converts stringText to a float
        if (instruction == '+') {                    //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);                                //wait to make sure all data in the Serial2 message has arived
          Serial2Flush();                            //Clear any excess data in the Serial2 buffer
          return;
        }
      }
    } else {
      return;
    }
  }



  else if (Serial1.available() > 0) {
    instruction = Serial1.read();
    //Serial.println(instruction);
    if (instruction == INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED) {
      int count = 0;
      while (Serial1.available() < 6) {  //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
        count++;
        if (count > 100) {
          Serial1Flush();  //  Clear the Serial1 buffer
          break;
        }
      }

      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;
      atPos7 = false;
      atPos8 = false;
      atPos9 = false;
      atPos0 = false;

      short sliderStepSpeed = (Serial1.read() << 8) + Serial1.read();
      if (!withSlider) {
        sliderStepSpeed = 0;
      }
      short panStepSpeed = (Serial1.read() << 8) + Serial1.read();
      short tiltStepSpeed = (Serial1.read() << 8) + Serial1.read();

      float sliderStepSpeed2 = sliderStepSpeed;
      float panStepSpeed2 = panStepSpeed;
      float tiltStepSpeed2 = tiltStepSpeed;

      float speedFactorS = map(sliderStepSpeed2, -255, 255, -sliderMaxFactor, sliderMaxFactor);
      float speedFactorP = map(panStepSpeed2, -255, 255, -panMaxFactor, panMaxFactor);
      float speedFactorT = map(tiltStepSpeed2, -255, 255, -tiltMaxFactor, tiltMaxFactor);


      previousMillisMoveCheck = millis();

      if (speedFactorP == 0.0) {
        if (panRunning) {
          panRunning = false;
          stepper_pan.overrideSpeed(0);
          stepper_pan.stopAsync();
        }
      } else {
        if (!panRunning) {
          panRunning = true;
          stepper_pan.setAcceleration(10000);            //pan_accel *
          stepper_pan.rotateAsync(pan_set_speed * 100);  //, 10000);
        }
        if (upsideDown) {
          speedFactorP = (speedFactorP * -1);
        }
        stepper_pan.overrideSpeed(speedFactorP);
        
        //Serial.print("Factor P - ");
        //Serial.println(speedFactorP);
      }

      if (speedFactorT == 0.0) {
        if (tiltRunning) {
          tiltRunning = false;
          stepper_tilt.overrideSpeed(0);
          stepper_tilt.stopAsync();
        }
      } else {
        if (!tiltRunning) {
          tiltRunning = true;
          stepper_tilt.setAcceleration(10000);             //tilt_accel *
          stepper_tilt.rotateAsync(tilt_set_speed * 100);  //, 10000);
        }
        if (upsideDown) {
          speedFactorT = (speedFactorT * -1);
        }
        stepper_tilt.overrideSpeed(speedFactorT);
        
        //Serial.print("Factor T - ");
        //Serial.println(speedFactorT);
      }

      if (speedFactorS == 0.0) {
        if (sliderRunning) {
          sliderRunning = false;
          stepper_slider.overrideSpeed(0);
          stepper_slider.stopAsync();
        }
      } else {
        if (!sliderRunning) {
          sliderRunning = true;
          stepper_slider.setAcceleration(10000);               //slider_accel *
          stepper_slider.rotateAsync(slider_set_speed * 100);  //, 10000);
        }
        if (slideReverse) {
          speedFactorS = (speedFactorS * -1);
        }
        stepper_slider.overrideSpeed(speedFactorS);
        
        //Serial.print("Factor S - ");
        //Serial.println(speedFactorS);
      }

      if (speedFactorP == 0.0) {
        stepper_pan.setAcceleration(pan_accel);
      }
      if (speedFactorT == 0.0) {
        stepper_tilt.setAcceleration(tilt_accel);
      }
      if (speedFactorS == 0.0) {
        stepper_slider.setAcceleration(slider_accel);
      }

      if ((speedFactorS == 0.0) && (speedFactorP == 0.0) && (speedFactorT == 0.0)) {
        isManualMove = false;
      } else {
        isManualMove = true;
        previousMillisMoveCheck = millis();
      }




    } else if (instruction == INSTRUCTION_IS_COMMAND) {
      delay(2);  //wait to make sure all data in the Serial1 message has arived
      instruction = Serial1.read();
      //Serial.println(instruction);

      if (instruction == INSTRUCTION_IS_CAM_DELAY) {
        delay(2);
        dlyPos = Serial1.read();
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial1.available()) {                   //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial1Flush();                            //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);  //converts stringText to an int
      } else {
        memset(&stringText[0], 0, sizeof(stringText));  //clear the array
        while (Serial1.available()) {                   //set elemetns of stringText to the Serial1 values sent
          char digit = Serial1.read();                  //read in a char
          strncat(stringText, &digit, 1);               //add digit to the end of the array
        }
        Serial1Flush();                              //Clear any excess data in the Serial1 buffer
        SerialCommandValueInt = atoi(stringText);    //converts stringText to an int
        SerialCommandValueFloat = atof(stringText);  //converts stringText to a float

        //rintln(SerialCommandValueInt);
        //Serial.println(SerialCommandValueFloat);

        if (instruction == '+') {  //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
          delay(100);              //wait to make sure all data in the Serial1 message has arived
          Serial1Flush();          //Clear any excess data in the Serial1 buffer
          return;
        }
      }
    } else {
      return;
    }
  } else {
    return;
  }

  if (!atPos1 && !atPos2 && !atPos3 && !atPos4 && !atPos5 && !atPos6 && !atPos7 && !atPos8 && !atPos9 && !atPos0 && !sentMoved) {
    Serial1.println("#s");  // not at any set pos
    //Serial.println("not at any set pos");
    sentMoved = true;
  }

  //Serial.print("Switch case: ");
  //Serial.println(instruction);
  switch (instruction) {
    case INSTRUCTION_IS_CAM_DELAY:
      {
        if (dlyPos == 49) {
          dlyPos1Time = SerialCommandValueInt;
          Serial1.print("Delay before 2nd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 50) {
          dlyPos2Time = SerialCommandValueInt;
          Serial1.print("Delay before 3rd position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 51) {
          dlyPos3Time = SerialCommandValueInt;
          Serial1.print("Delay before 4th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 52) {
          dlyPos4Time = SerialCommandValueInt;
          Serial1.print("Delay before 5th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        } else if (dlyPos == 53) {
          dlyPos5Time = SerialCommandValueInt;
          Serial1.print("Delay before 6th position set: ");
          Serial1.print(SerialCommandValueInt);
          Serial1.println("ms\n");
        }
      }
      break;
    case INSTRUCTION_IS_RUN_CAM:
      {
        Serial1.println("Run array of moves.");
        Serial1.println("#$");
        if (pos1set) {
          moveToIndex(1);
          timeElapsed = 0;
          if (pos2set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos1Time);
            Serial1.println("ms");
            previousTime = dlyPos1Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(2);
            timeElapsed = 0;
          }
          if (pos3set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos2Time);
            Serial1.println("ms");
            previousTime = dlyPos2Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(3);
            timeElapsed = 0;
          }
          if (pos4set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos3Time);
            Serial1.println("ms");
            previousTime = dlyPos3Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(4);
            timeElapsed = 0;
          }
          if (pos5set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos4Time);
            Serial1.println("ms");
            previousTime = dlyPos4Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(5);
            timeElapsed = 0;
          }
          if (pos6set) {
            Serial1.print("Delay until next move: ");
            Serial1.print(dlyPos5Time);
            Serial1.println("ms");
            previousTime = dlyPos5Time + timeElapsed;
            while (timeElapsed < previousTime) {
              delay(2);
            }
            moveToIndex(6);
            timeElapsed = 0;
          }
        }
      }
      break;
    case INSTRUCTION_DIRECT_MOVE:
      {
        //Serial.print("is pan moving?? ");
        //Serial.println(stepper_pan.isMoving);
        //Serial.print("is tilt moving?? ");
        //Serial.println(stepper_tilt.isMoving);
        //Serial.print("is slider moving?? ");
        //Serial.println(stepper_slider.isMoving);
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {  // && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
          //Serial.println("Sent moveToIndex");
          moveToIndex(SerialCommandValueInt);
        }
      }
      break;
    case INSTRUCTION_SETPOS:
      {
        editKeyframe(SerialCommandValueInt);
        /*
        //editKeyframe(SerialCommandValueInt);
        Serial.println("Starting move");
        stepper_pan.setMaxSpeed(10000);
        stepper_tilt.setMaxSpeed(10000);
        stepper_slider.setMaxSpeed(10000);

        stepper_pan.setTargetAbs(5000);
        stepper_tilt.setTargetAbs(5000);
        stepper_slider.setTargetAbs(5000);

        //multi_stepper.move(stepper_pan, stepper_tilt, stepper_slider);
        StepperGroup stepGroup({ stepper_pan, stepper_tilt, stepper_slider });
        stepGroup.move();
        Serial.println("Finished move");

        //StepperGroup ({stepper_pan, stepper_tilt, stepper_slider}).move();
        */
      }
      break;
    case INSTRUCTION_CLEAR_ARRAY:
      {
        clearKeyframes();
      }
      break;
    case INSTRUCTION_PAN_ACCEL:
      {
        pan_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_pan.setAcceleration(pan_accel);
        Serial1.println(String("Pan accel : ") + pan_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TILT_ACCEL:
      {
        tilt_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_tilt.setAcceleration(tilt_accel);
        Serial1.println(String("Tilt accel : ") + tilt_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_ACCEL:
      {
        slider_accel = (SerialCommandValueInt >= 0) ? SerialCommandValueInt : 0;
        stepper_slider.setAcceleration(slider_accel);
        Serial1.println(String("Slider accel : ") + slider_accel + String(" steps/s²"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_PAN_JOY_ACCEL:
      {
        panAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial1.println(String("Pan Joy accel factor : ") + panAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TILT_JOY_ACCEL:
      {
        tiltAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial1.println(String("Tilt Joy accel factor : ") + tiltAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SLIDER_JOY_ACCEL:
      {
        sliderAccelJoy = (SerialCommandValueFloat >= 0) ? SerialCommandValueFloat : 0;
        Serial1.println(String("Slider Joy accel factor : ") + sliderAccelJoy);
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SAVE_TO_EEPROM:
      {
        saveEEPROM();
      }
      break;
    case INSTRUCTION_DEBUG_STATUS:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          debugReport();
        }
      }
      break;
    case INSTRUCTION_POSITION_STATUS:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          positionReport();
        }
      }
      break;
    case INSTRUCTION_KEYFRAMES_STATUS:
      {
        printKeyframeElements();
      }
      break;
    case INSTRUCTION_RESET_LEDS:
      {
        doRemoteControlLEDs();
      }
      break;
    case INSTRUCTION_PAN_DEGREES:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          panDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          tiltDegrees(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          sliderMoveTo(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_PAN_DEGREES_REL:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          panDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_TILT_DEGREES_REL:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          tiltDegreesRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SLIDER_MILLIMETRES_REL:
      {
        //if (!multi_stepper.isRunning() && !step_stepperP.isRunning() && !rotate_stepperP.isRunning() && !step_stepperT.isRunning() && !rotate_stepperT.isRunning() && !step_stepperS.isRunning() && !rotate_stepperS.isRunning()) {
        if (!stepper_pan.isMoving && !stepper_tilt.isMoving && !stepper_slider.isMoving) {
          sliderMMRel(SerialCommandValueFloat);
        }
      }
      break;
    case INSTRUCTION_SET_PAN_SPEED:
      {
        pan_set_speed = SerialCommandValueFloat;
        pan_def_speed = pan_set_speed;  //  set default speeds
        stepper_pan.setMaxSpeed(panDegreesToSteps(pan_set_speed));

        tilt_set_speed = SerialCommandValueFloat;
        tilt_def_speed = tilt_set_speed;  //  set default speeds
        stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));

        if (pan_set_speed == 20) {
          Serial1.println("^@7");
          pan_accel = pan_def_accel * 4;
          tilt_accel = tilt_def_accel * 4;
        } else if (pan_set_speed == 10) {
          Serial1.println("^@5");
          pan_accel = pan_def_accel * 2;
          tilt_accel = tilt_def_accel * 2;
        } else if (pan_set_speed == 5) {
          Serial1.println("^@3");
          pan_accel = pan_def_accel;
          tilt_accel = tilt_def_accel;
        } else if (pan_set_speed == 1) {
          Serial1.println("^@1");
          pan_accel = pan_def_accel * 0.2;
          tilt_accel = tilt_def_accel * 0.2;
        }

        Serial1.println(String("Set Pan/Tilt Speed to: ") + pan_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_TILT_SPEED:
      {
        tilt_set_speed = SerialCommandValueFloat;
        tilt_def_speed = tilt_set_speed;  //  set default speeds
        stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));
        Serial1.println(String("Set Tilt Speed to: ") + tilt_set_speed + String("°/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_SET_SLIDER_SPEED:
      {
        slider_set_speed = SerialCommandValueFloat;
        slider_def_speed = slider_set_speed;  //  set default speeds
        stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));

        if (slider_set_speed == 160) {
          Serial1.println("^=7");
          slider_accel = slider_def_accel * 4;
        } else if (slider_set_speed == 120) {
          Serial1.println("^=5");
          slider_accel = slider_def_accel * 2;
        } else if (slider_set_speed == 60) {
          Serial1.println("^=3");
          slider_accel = slider_def_accel;
        } else if (slider_set_speed == 20) {
          Serial1.println("^=1");
          slider_accel = slider_def_accel * 0.3;
        }

        Serial1.println(String("Set Slider Speed to: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_IN:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = true;
        zoomOUT = false;

        Serial1.print("#I");
        Serial1.println(zoom_speed);
        Serial2.print("#I");
        Serial2.println(zoom_speed);

        Serial1.println("Zoom IN.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_ZOOM_OUT:
      {
        zoom_speed = SerialCommandValueInt;
        zoomIN = false;
        zoomOUT = true;

        Serial1.print("#i");
        Serial1.println(zoom_speed);
        Serial2.print("#i");
        Serial2.println(zoom_speed);

        Serial1.println("Zoom OUT.");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_STOP_ZOOM:
      {
        zoomIN = false;
        zoomOUT = false;

        Serial1.println("#o");
        Serial2.println("#o");
        delay(20);
        Serial1.println("#o");  // Just in case, it's important!
        Serial2.println("#o");

        Serial1.println("STOP Zooming.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_TOGGLE_RECORDING:
      {
        Serial1.println("#O");
        Serial2.println("#O");

        Serial1.println("Toggle Record.\n");
        Serial1.println("#$");
      }
      break;
    case INSTRUCTION_IS_RECORDING:
      {
        Serial1.println("#P");
        Serial2.println("#P");
      }
      break;
    case INSTRUCTION_IS_NOT_RECORDING:
      {
        Serial1.println("#p");
        Serial2.println("#p");
      }
      break;
    case INSTRUCTION_SET_ZERO_POS:
      {
        stepper_pan.setPosition(0);
        stepper_tilt.setPosition(0);
        stepper_slider.setPosition(0);
      }
      break;
    case INSTRUCTION_RESTORE_DEFAULT_SPEEDS:
      {
        pan_set_speed = pan_def_speed;
        tilt_set_speed = tilt_def_speed;
        slider_set_speed = slider_def_speed;

        Serial1.print("^=");
        Serial1.println(slider_set_speed);

        Serial1.println("#d");

        Serial1.println(String("Default Speed Restored: ") + slider_set_speed + String("mm/s.\n"));
        Serial1.println("#$");
      }
      break;
    default:
      break;  // if unrecognised charater, do nothing
  }
}
