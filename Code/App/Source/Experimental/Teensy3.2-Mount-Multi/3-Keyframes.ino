//  Keyframes - Moveto, Edit & Clear


void editKeyframe(int keyframeEdit) {
  keyframe_array[(keyframeEdit - 1)].panStepCount = stepper_pan.getPosition();
  keyframe_array[(keyframeEdit - 1)].tiltStepCount = stepper_tilt.getPosition();
  keyframe_array[(keyframeEdit - 1)].sliderStepCount = stepper_slider.getPosition();
  keyframe_array[(keyframeEdit - 1)].panSpeed = panDegreesToSteps(pan_set_speed);
  keyframe_array[(keyframeEdit - 1)].tiltSpeed = tiltDegreesToSteps(tilt_set_speed);
  keyframe_array[(keyframeEdit - 1)].sliderSpeed = sliderMillimetresToSteps(slider_set_speed);
  keyframe_array[(keyframeEdit - 1)].isRecorded = 1;

  if (keyframeEdit == 1) {
    pos1set = true;
    atPos1 = true;
    Serial1.println("#z");
    Serial1.println("#Z");
    Serial2.println("#z");
    Serial2.println("#Z");
    Serial3.println("#z");
    Serial3.println("#Z");
  }
  else if (keyframeEdit == 2) {
    pos2set = true;
    atPos2 = true;
    Serial1.println("#x");
    Serial1.println("#X");
    Serial2.println("#x");
    Serial2.println("#X");
    Serial3.println("#x");
    Serial3.println("#X");
  }
  else if (keyframeEdit == 3) {
    pos3set = true;
    atPos3 = true;
    Serial1.println("#c");
    Serial1.println("#C");
    Serial2.println("#c");
    Serial2.println("#C");
    Serial3.println("#c");
    Serial3.println("#C");
  }
  else if (keyframeEdit == 4) {
    pos4set = true;
    atPos4 = true;
    Serial1.println("#v");
    Serial1.println("#V");
    Serial2.println("#v");
    Serial2.println("#V");
    Serial3.println("#v");
    Serial3.println("#V");
  }
  else if (keyframeEdit == 5) {
    pos5set = true;
    atPos5 = true;
    Serial1.println("#b");
    Serial1.println("#B");
    Serial2.println("#b");
    Serial2.println("#B");
    Serial3.println("#b");
    Serial3.println("#B");
  }
  else if (keyframeEdit == 6) {
    pos6set = true;
    atPos6 = true;
    Serial1.println("#n");
    Serial1.println("#N");
    Serial2.println("#n");
    Serial2.println("#N");
    Serial3.println("#n");
    Serial3.println("#N");
  }

  Serial.println(String("Edited index: ") + keyframeEdit);
  Serial.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));

  Serial1.println(String("Edited index: ") + keyframeEdit);
  Serial1.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial1.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial1.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));
  Serial1.println("#$");

  sentMoved = false;
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void clearKeyframes(void) {
  //keyframe_array[0].isRecorded = 0;
  //keyframe_array[1].isRecorded = 0;
  //keyframe_array[2].isRecorded = 0;
  //keyframe_array[3].isRecorded = 0;
  //keyframe_array[4].isRecorded = 0;
  //keyframe_array[5].isRecorded = 0;

  for (int i = 0; i < 6; i++) {
    keyframe_array[i].panStepCount = 0;
    keyframe_array[i].tiltStepCount = 0;
    keyframe_array[i].sliderStepCount = 0;
    keyframe_array[i].panSpeed = 0;
    keyframe_array[i].tiltSpeed = 0;
    keyframe_array[i].sliderSpeed = 0;
    keyframe_array[i].isRecorded = 0;
    keyframe_array[i].runDelay = 0;
    keyframe_array[i].runAccel = 0;
  }

  pos1set = false;
  pos2set = false;
  pos3set = false;
  pos4set = false;
  pos5set = false;
  pos6set = false;

  atPos1 = false;
  atPos2 = false;
  atPos3 = false;
  atPos4 = false;
  atPos5 = false;
  atPos6 = false;

  Serial1.println("#a");
  Serial2.println("#a");
  Serial3.println("#a");

  Serial.println("Positions Cleared.\n");
  Serial1.println("Positions Cleared.\n");
  Serial1.println("#$");
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void moveToIndex(int index) {
  if (keyframe_array[index - 1].isRecorded == 0) {
    Serial.println(String("Keyframe ") + index + String(" doesn't exist.\n"));
    return;
  }

  if (index == 1) {
    Serial1.println("#A");
    Serial2.println("#A");
    Serial3.println("#A");
  }
  else if (index == 2) {
    Serial1.println("#S");
    Serial2.println("#S");
    Serial3.println("#S");
  }
  else if (index == 3) {
    Serial1.println("#D");
    Serial2.println("#D");
    Serial3.println("#D");
  }
  else if (index == 4) {
    Serial1.println("#F");
    Serial2.println("#F");
    Serial3.println("#F");
  }
  else if (index == 5) {
    Serial1.println("#G");
    Serial2.println("#G");
    Serial3.println("#G");
  }
  else if (index == 6) {
    Serial1.println("#H");
    Serial2.println("#H");
    Serial3.println("#H");
  }

  Serial.println(String("Moving to Index: ") + index);
  Serial.println(String("Pan   : ") + panStepsToDegrees(keyframe_array[index - 1].panStepCount) + String("°"));
  Serial.println(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[index - 1].tiltStepCount) + String("°"));
  Serial.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[index - 1].sliderStepCount) + String("mm\n"));

  Serial.println(String("Pan    Steps : ") + keyframe_array[index - 1].panStepCount);
  Serial.println(String("Tilt   Steps : ") + keyframe_array[index - 1].tiltStepCount);
  Serial.println(String("Slider Steps : ") + keyframe_array[index - 1].sliderStepCount);

  if (useKeyframeSpeeds) {
    Serial.println(String("Pan    Speed : ") + keyframe_array[index - 1].panSpeed + String("°"));
    Serial.println(String("Tilt   Speed : ") + keyframe_array[index - 1].tiltSpeed + String("°"));
    Serial.println(String("Slider Speed : ") + keyframe_array[index - 1].sliderSpeed + String("mm"));
  }

  Serial1.println(String("Moving to Index: ") + index);
  Serial1.println(String("Pan   : ") + panStepsToDegrees(keyframe_array[index - 1].panStepCount) + String("°"));
  Serial1.println(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[index - 1].tiltStepCount) + String("°"));
  Serial1.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[index - 1].sliderStepCount) + String("mm"));
  Serial1.println("#$");

  /*                                                         KEEP: Old version for use with stock TeensyStep
    float thisDistance = 0.0;
    float thisTime = 0.0;
    float longestTime = 0.0;
    float fastestSpeed = 0.0;
    float thisSpeed = 0.0;

    thisDistance = keyframe_array[index-1].panStepCount - stepper_pan.getPosition();
    thisTime = abs(thisDistance) / keyframe_array[index-1].panSpeed;
    if (thisTime > longestTime) longestTime = thisTime;

    thisDistance = keyframe_array[index-1].tiltStepCount - stepper_tilt.getPosition();
    thisTime = abs(thisDistance) / keyframe_array[index-1].tiltSpeed;
    if (thisTime > longestTime) longestTime = thisTime;

    thisDistance = keyframe_array[index-1].sliderStepCount - stepper_slider.getPosition();
    thisTime = abs(thisDistance) / keyframe_array[index-1].sliderSpeed;
    if (thisTime > longestTime) longestTime = thisTime;

    if (longestTime > 0.0) {
      thisDistance = keyframe_array[index-1].panStepCount - stepper_pan.getPosition();
      thisSpeed = abs(thisDistance / longestTime);
      if (thisSpeed > fastestSpeed) fastestSpeed = thisSpeed;

      thisDistance = keyframe_array[index-1].tiltStepCount - stepper_tilt.getPosition();
      thisSpeed = abs(thisDistance / longestTime);
      if (thisSpeed > fastestSpeed) fastestSpeed = thisSpeed;

      thisDistance = keyframe_array[index-1].sliderStepCount - stepper_slider.getPosition();
      thisSpeed = abs(thisDistance / longestTime);
      if (thisSpeed > fastestSpeed) fastestSpeed = thisSpeed;
    }

    stepper_pan.setMaxSpeed(fastestSpeed);
    stepper_tilt.setMaxSpeed(fastestSpeed);
    stepper_slider.setMaxSpeed(fastestSpeed);
  */
  if (useKeyframeSpeeds) {
    stepper_pan.setMaxSpeed(keyframe_array[index - 1].panSpeed);
    stepper_tilt.setMaxSpeed(keyframe_array[index - 1].tiltSpeed);
    stepper_slider.setMaxSpeed(keyframe_array[index - 1].sliderSpeed);
  }

  stepper_pan.setTargetAbs(keyframe_array[index - 1].panStepCount);
  stepper_tilt.setTargetAbs(keyframe_array[index - 1].tiltStepCount);
  stepper_slider.setTargetAbs(keyframe_array[index - 1].sliderStepCount);

  multi_stepper.move(stepper_pan, stepper_tilt, stepper_slider);

  if (index == 1) {
    atIndex = "#z";
    atPos1 = true;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
  }
  else if (index == 2) {
    atIndex = "#x";
    atPos2 = true;
    atPos1 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
  }
  else if (index == 3) {
    atIndex = "#c";
    atPos3 = true;
    atPos1 = false;
    atPos2 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
  }
  else if (index == 4) {
    atIndex = "#v";
    atPos4 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos5 = false;
    atPos6 = false;
  }
  else if (index == 5) {
    atIndex = "#b";
    atPos5 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos6 = false;
  }
  else if (index == 6) {
    atIndex = "#n";
    atPos6 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
  }

  delay(100);     // delay for serial read

  Serial1.println(atIndex);
  Serial2.println(atIndex);
  Serial3.println(atIndex);

  Serial.println(String("At index: ") + index + String("\n"));
  Serial1.println(String("At index: ") + index + String("\n"));
  Serial1.println("#$");

  if (useKeyframeSpeeds) {
    stepper_pan.setMaxSpeed(panDegreesToSteps(pan_set_speed));
    stepper_tilt.setMaxSpeed(tiltDegreesToSteps(tilt_set_speed));
    stepper_slider.setMaxSpeed(sliderMillimetresToSteps(slider_set_speed));
  }

  sentMoved = false;
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void PIDmove() {
  pid();

  if (retargetTimer > targetTimer) {
    retargetTimer = 0;
    if (pos1set && counter == 1) {
      //Serial1.println("#s");
      Serial1.println("#A");
      Serial1.println("Start PID moves");

      /*
        stepper_pan
        .setMaxSpeed(keyframe_array[0].panSpeed)
        .setAcceleration(keyframe_array[0].runAccel);

        stepper_tilt
        .setMaxSpeed(keyframe_array[0].tiltSpeed)
        .setAcceleration(keyframe_array[0].runAccel);

        stepper_slider
        .setMaxSpeed(keyframe_array[0].sliderSpeed)
        .setAcceleration(keyframe_array[0].runAccel);

        targetP = keyframe_array[0].panStepCount;
        targetT = keyframe_array[0].tiltStepCount;
        targetS = keyframe_array[0].sliderStepCount;

        targetTimer = keyframe_array[0].runDelay;
        counter++;
      */

      stepper_pan.setTargetAbs(keyframe_array[0].panStepCount);
      stepper_tilt.setTargetAbs(keyframe_array[0].tiltStepCount);
      stepper_slider.setTargetAbs(keyframe_array[0].sliderStepCount);
      multi_stepper.move(stepper_pan, stepper_tilt, stepper_slider);
      Serial1.println("#$");
      Serial1.println("#z");
      targetTimer = 0;
      counter++;
      delay(100);
    }
    else if (!pos1set && counter == 1) {
      if (!isLastRunMove) {
        Serial1.println("Last Move1");
        isLastRunMove = true;
      }
    }

    else if (pos2set && counter == 2) {
      Serial1.println("#z");
      delay(500);
      Serial1.println("#S");
      Serial1.println("PIDmove 1 -> 2");

      rotate_stepperP.rotateAsync(stepper_pan);
      rotate_stepperP.overrideSpeed(0);         // start with stopped

      rotate_stepperT.rotateAsync(stepper_tilt);
      rotate_stepperT.overrideSpeed(0);

      rotate_stepperS.rotateAsync(stepper_slider);
      rotate_stepperS.overrideSpeed(0);

      stepper_pan
      .setMaxSpeed(keyframe_array[1].panSpeed)
      .setAcceleration(keyframe_array[1].runAccel);

      stepper_tilt
      .setMaxSpeed(keyframe_array[1].tiltSpeed)
      .setAcceleration(keyframe_array[1].runAccel);

      stepper_slider
      .setMaxSpeed(keyframe_array[1].sliderSpeed)
      .setAcceleration(keyframe_array[1].runAccel);

      Serial1.println(String("SPD- ") + keyframe_array[1].panSpeed + String("  /  ACC- ") + keyframe_array[1].runAccel + String("  /  DLY- ") + keyframe_array[1].runDelay);

      targetP = keyframe_array[1].panStepCount;
      targetT = keyframe_array[1].tiltStepCount;
      targetS = keyframe_array[1].sliderStepCount;

      targetTimer = keyframe_array[1].runDelay;
      counter++;
    }
    else if (!pos2set && counter == 2) {
      if (!isLastRunMove) {
        Serial1.println("Last Move2");
        isLastRunMove = true;
      }
    }

    else if (pos3set && counter == 3) {
      Serial1.println("#x");
      //Serial1.println("#s");
      Serial1.println("#D");
      Serial1.println("PIDmove 2 -> 3");

      stepper_pan
      .setMaxSpeed(keyframe_array[2].panSpeed)
      .setAcceleration(keyframe_array[2].runAccel);

      stepper_tilt
      .setMaxSpeed(keyframe_array[2].tiltSpeed)
      .setAcceleration(keyframe_array[2].runAccel);

      stepper_slider
      .setMaxSpeed(keyframe_array[2].sliderSpeed)
      .setAcceleration(keyframe_array[2].runAccel);

      Serial1.println(String("SPD- ") + keyframe_array[2].panSpeed + String("  /  ACC- ") + keyframe_array[2].runAccel + String("  /  DLY- ") + keyframe_array[2].runDelay);

      targetP = keyframe_array[2].panStepCount;
      targetT = keyframe_array[2].tiltStepCount;
      targetS = keyframe_array[2].sliderStepCount;

      targetTimer = keyframe_array[2].runDelay;
      counter++;
    }
    else if (!pos3set && counter == 3) {
      if (!isLastRunMove) {
        Serial1.println("Last Move");
        isLastRunMove = true;
      }
    }

    else if (pos4set && counter == 4) {
      Serial1.println("#c");
      //Serial1.println("#s");
      Serial1.println("#F");
      Serial1.println("PIDmove 3 -> 4");

      stepper_pan
      .setMaxSpeed(keyframe_array[3].panSpeed)
      .setAcceleration(keyframe_array[3].runAccel);

      stepper_tilt
      .setMaxSpeed(keyframe_array[3].tiltSpeed)
      .setAcceleration(keyframe_array[3].runAccel);

      stepper_slider
      .setMaxSpeed(keyframe_array[3].sliderSpeed)
      .setAcceleration(keyframe_array[3].runAccel);

      Serial1.println(String("SPD- ") + keyframe_array[3].panSpeed + String("  /  ACC- ") + keyframe_array[3].runAccel + String("  /  DLY- ") + keyframe_array[3].runDelay);

      targetP = keyframe_array[3].panStepCount;
      targetT = keyframe_array[3].tiltStepCount;
      targetS = keyframe_array[3].sliderStepCount;

      targetTimer = keyframe_array[3].runDelay;
      counter++;
    }
    else if (!pos4set && counter == 4) {
      if (!isLastRunMove) {
        Serial1.println("Last Move");
        isLastRunMove = true;
      }
    }

    else if (pos5set && counter == 5) {
      Serial1.println("#v");
      //Serial1.println("#s");
      Serial1.println("#G");
      Serial1.println("PIDmove 4 -> 5");

      stepper_pan
      .setMaxSpeed(keyframe_array[4].panSpeed)
      .setAcceleration(keyframe_array[4].runAccel);

      stepper_tilt
      .setMaxSpeed(keyframe_array[4].tiltSpeed)
      .setAcceleration(keyframe_array[4].runAccel);

      stepper_slider
      .setMaxSpeed(keyframe_array[4].sliderSpeed)
      .setAcceleration(keyframe_array[4].runAccel);

      Serial1.println(String("SPD- ") + keyframe_array[4].panSpeed + String("  /  ACC- ") + keyframe_array[4].runAccel + String("  /  DLY- ") + keyframe_array[4].runDelay);

      targetP = keyframe_array[4].panStepCount;
      targetT = keyframe_array[4].tiltStepCount;
      targetS = keyframe_array[4].sliderStepCount;

      targetTimer = keyframe_array[4].runDelay;
      counter++;
    }
    else if (!pos5set && counter == 5) {
      if (!isLastRunMove) {
        Serial1.println("Last Move");
        isLastRunMove = true;
      }
    }

    else if (pos6set && counter == 6) {
      Serial1.println("#b");
      //Serial1.println("#s");
      Serial1.println("#H");
      Serial1.println("PIDmove 5 -> 6");

      stepper_pan
      .setMaxSpeed(keyframe_array[5].panSpeed)
      .setAcceleration(keyframe_array[5].runAccel);

      stepper_tilt
      .setMaxSpeed(keyframe_array[5].tiltSpeed)
      .setAcceleration(keyframe_array[5].runAccel);

      stepper_slider
      .setMaxSpeed(keyframe_array[5].sliderSpeed)
      .setAcceleration(keyframe_array[5].runAccel);

      Serial1.println(String("SPD- ") + keyframe_array[5].panSpeed + String("  /  ACC- ") + keyframe_array[5].runAccel + String("  /  DLY- ") + keyframe_array[5].runDelay);

      targetP = keyframe_array[5].panStepCount;
      targetT = keyframe_array[5].tiltStepCount;
      targetS = keyframe_array[5].sliderStepCount;

      targetTimer = keyframe_array[5].runDelay;
      //counter++;
    }
    else if (!pos6set && counter == 6) {
      if (!isLastRunMove) {
        Serial1.println("Last Move");
        isLastRunMove = true;
      }
    }
  }
}

void pid() {
  if (millis() - lastTick >= PID_Interval)
  {
    if (!panEnd) {
      deltaP = (targetP - stepper_pan.getPosition()) * (P / PID_Interval);        // This implements a simple P regulator (can be extended to a PID if necessary)
      factorP = std::max(-1.0f, std::min(1.0f, deltaP));                          // limit to -1.0..1.0
      rotate_stepperP.overrideSpeed(factorP);                                           // set new speed
    }
    if (!tiltEnd) {
      deltaT = (targetT - stepper_tilt.getPosition()) * (P / PID_Interval);
      factorT = std::max(-1.0f, std::min(1.0f, deltaT));
      rotate_stepperT.overrideSpeed(factorT);
    }
    if (!sliderEnd) {
      deltaS = (targetS - stepper_slider.getPosition()) * (P / PID_Interval);
      factorS = std::max(-1.0f, std::min(1.0f, deltaS));
      rotate_stepperS.overrideSpeed(factorS);
    }
    lastTick = millis();
  }
  if (stepper_pan.getPosition() == targetP && isLastRunMove && !panEnd) {
    Serial1.println("Pan @ End");
    panEnd = true;
    rotate_stepperP.stopAsync();
  }
  if (stepper_tilt.getPosition() == targetT && isLastRunMove && !tiltEnd) {
    Serial1.println("Tilt @ End");
    tiltEnd = true;
    rotate_stepperT.stopAsync();
  }
  if (stepper_slider.getPosition() == targetS && isLastRunMove && !sliderEnd) {
    Serial1.println("Slider @ End");
    sliderEnd = true;
    rotate_stepperS.stopAsync();
  }
  if (((factorP < 0.01 && factorP > -0.01) && (factorT < 0.01 && factorT > -0.01) && (factorS < 0.01 && factorS > -0.01) && isLastRunMove) || (panEnd && tiltEnd && sliderEnd && isLastRunMove)) {
    runCamLoop = false;
    int runIndex = counter - 1;

    if (runIndex == 1) {
      atIndex = "#z";
      atPos1 = true;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;
      Serial1.println(atIndex);
    }
    else if (runIndex == 2) {
      atIndex = "#x";
      atPos2 = true;
      atPos1 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;
      Serial1.println(atIndex);
    }
    else if (runIndex == 3) {
      atIndex = "#c";
      atPos3 = true;
      atPos1 = false;
      atPos2 = false;
      atPos4 = false;
      atPos5 = false;
      atPos6 = false;
      Serial1.println(atIndex);
    }
    else if (runIndex == 4) {
      atIndex = "#v";
      atPos4 = true;
      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos5 = false;
      atPos6 = false;
      Serial1.println(atIndex);
    }
    else if (runIndex == 5) {
      atIndex = "#b";
      atPos5 = true;
      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos6 = false;
      Serial1.println(atIndex);
    }
    else if (runIndex == 6) {
      atIndex = "#n";
      atPos6 = true;
      atPos1 = false;
      atPos2 = false;
      atPos3 = false;
      atPos4 = false;
      atPos5 = false;
      Serial1.println(atIndex);
    }
    //delay(100);     // delay for serial read

    rotate_stepperP.stopAsync();
    rotate_stepperT.stopAsync();
    rotate_stepperS.stopAsync();

    delay(100);

    Serial1.println(atIndex);
    //delay(10);

    stepper_pan
    .setMaxSpeed(panDegreesToSteps(pan_set_speed))
    .setAcceleration(pan_accel);
    stepper_tilt
    .setMaxSpeed(tiltDegreesToSteps(tilt_set_speed))
    .setAcceleration(tilt_accel);
    stepper_slider
    .setMaxSpeed(sliderMillimetresToSteps(slider_set_speed))
    .setAcceleration(slider_accel);


    Serial1.println("Array of moves finished");
    Serial1.println(String("At index: ") + runIndex + String("\n"));

    Serial1.println("#$");

    panEnd = false;
    tiltEnd = false;
    sliderEnd = false;
  }
}
