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
    //Serial2.println("#z");
    //Serial2.println("#Z");
    //Serial3.println("#z");
    //Serial3.println("#Z");
  }
  else if (keyframeEdit == 2) {
    pos2set = true;
    atPos2 = true;
    Serial1.println("#x");
    Serial1.println("#X");
    //Serial2.println("#x");
    //Serial2.println("#X");
    //Serial3.println("#x");
    //Serial3.println("#X");
  }
  else if (keyframeEdit == 3) {
    pos3set = true;
    atPos3 = true;
    Serial1.println("#c");
    Serial1.println("#C");
    //Serial2.println("#c");
    //Serial2.println("#C");
    //Serial3.println("#c");
    //Serial3.println("#C");
  }
  else if (keyframeEdit == 4) {
    pos4set = true;
    atPos4 = true;
    Serial1.println("#v");
    Serial1.println("#V");
    //Serial2.println("#v");
    //Serial2.println("#V");
    //Serial3.println("#v");
    //Serial3.println("#V");
  }
  else if (keyframeEdit == 5) {
    pos5set = true;
    atPos5 = true;
    Serial1.println("#b");
    Serial1.println("#B");
    //Serial2.println("#b");
    //Serial2.println("#B");
    //Serial3.println("#b");
    //Serial3.println("#B");
  }
  else if (keyframeEdit == 6) {
    pos6set = true;
    atPos6 = true;
    Serial1.println("#n");
    Serial1.println("#N");
    //Serial2.println("#n");
    //Serial2.println("#N");
    //Serial3.println("#n");
    //Serial3.println("#N");
  }
  else if (keyframeEdit == 7) {
    pos7set = true;
    atPos7 = true;
    Serial1.println("#m");
    Serial1.println("#M");
    //Serial2.println("#m");
    //Serial2.println("#M");
    //Serial3.println("#m");
    //Serial3.println("#M");
  }
  else if (keyframeEdit == 8) {
    pos8set = true;
    atPos8 = true;
    Serial1.println("#,");
    Serial1.println("#<");
    //Serial2.println("#,");
    //Serial2.println("#<");
    //Serial3.println("#,");
    //Serial3.println("#<");
  }
  else if (keyframeEdit == 9) {
    pos9set = true;
    atPos9 = true;
    Serial1.println("#.");
    Serial1.println("#>");
    //Serial2.println("#.");
    //Serial2.println("#>");
    //Serial3.println("#.");
    //Serial3.println("#>");
  }
  else if (keyframeEdit == 10) {
    pos0set = true;
    atPos0 = true;
    Serial1.println("#/");
    Serial1.println("#?");
    //Serial2.println("#/");
    //Serial2.println("#?");
    //Serial3.println("#/");
    //Serial3.println("#?");
  }

  //Serial.println(String("Edited index: ") + keyframeEdit);
  //Serial.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  //Serial.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  //Serial.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));

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

  for (int i = 0; i < 10; i++) {
    keyframe_array[i].panStepCount = 0;
    keyframe_array[i].tiltStepCount = 0;
    keyframe_array[i].sliderStepCount = 0;
    keyframe_array[i].panSpeed = 0;
    keyframe_array[i].tiltSpeed = 0;
    keyframe_array[i].sliderSpeed = 0;
    keyframe_array[i].isRecorded = 0;
  }

  pos1set = false;
  pos2set = false;
  pos3set = false;
  pos4set = false;
  pos5set = false;
  pos6set = false;
  pos7set = false;
  pos8set = false;
  pos9set = false;
  pos0set = false;

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

  Serial1.println("#a");
  //Serial2.println("#a");
  //Serial3.println("#a");

  //Serial.println("Positions Cleared.\n");
  Serial1.println("Positions Cleared.\n");
  Serial1.println("#$");
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void moveToIndex(int index) {
  if (keyframe_array[index - 1].isRecorded == 0) {
    //Serial.println(String("Keyframe ") + index + String(" doesn't exist.\n"));
    return;
  }

  if (index == 1) {
    Serial1.println("#A");
    //Serial2.println("#A");
    //Serial3.println("#A");
  }
  else if (index == 2) {
    Serial1.println("#S");
    //Serial2.println("#S");
    //Serial3.println("#S");
  }
  else if (index == 3) {
    Serial1.println("#D");
    //Serial2.println("#D");
    //Serial3.println("#D");
  }
  else if (index == 4) {
    Serial1.println("#F");
    //Serial2.println("#F");
    //Serial3.println("#F");
  }
  else if (index == 5) {
    Serial1.println("#G");
    //Serial2.println("#G");
    //Serial3.println("#G");
  }
  else if (index == 6) {
    Serial1.println("#H");
    //Serial2.println("#H");
    //Serial3.println("#H");
  }
  else if (index == 7) {
    Serial1.println("#J");
    //Serial2.println("#J");
    //Serial3.println("#J");
  }
  else if (index == 8) {
    Serial1.println("#K");
    //Serial2.println("#K");
    //Serial3.println("#K");
  }
  else if (index == 9) {
    Serial1.println("#L");
    //Serial2.println("#L");
    //Serial3.println("#L");
  }
  else if (index == 10) {
    Serial1.println("#:");
    //Serial2.println("#:");
    //Serial3.println("#:");
  }

  //Serial.println(String("Moving to Index: ") + index);
  //Serial.println(String("Pan   : ") + panStepsToDegrees(keyframe_array[index - 1].panStepCount) + String("°"));
  //Serial.println(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[index - 1].tiltStepCount) + String("°"));
  //Serial.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[index - 1].sliderStepCount) + String("mm\n"));

  //Serial.println(String("Pan    Steps : ") + keyframe_array[index - 1].panStepCount);
  //Serial.println(String("Tilt   Steps : ") + keyframe_array[index - 1].tiltStepCount);
  //Serial.println(String("Slider Steps : ") + keyframe_array[index - 1].sliderStepCount);
  
  //if (useKeyframeSpeeds) {
    //Serial.println(String("Pan    Speed : ") + keyframe_array[index - 1].panSpeed + String("°"));
    //Serial.println(String("Tilt   Speed : ") + keyframe_array[index - 1].tiltSpeed + String("°"));
    //Serial.println(String("Slider Speed : ") + keyframe_array[index - 1].sliderSpeed + String("mm"));
  //}

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

  //SerialFlush(); 
  Serial1Flush(); 
  //Serial2Flush(); 
  //Serial3Flush(); 

  if (index == 1) {
    atIndex = "#z";
    atPos1 = true;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 2) {
    atIndex = "#x";
    atPos2 = true;
    atPos1 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 3) {
    atIndex = "#c";
    atPos3 = true;
    atPos1 = false;
    atPos2 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 4) {
    atIndex = "#v";
    atPos4 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 5) {
    atIndex = "#b";
    atPos5 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 6) {
    atIndex = "#n";
    atPos6 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 7) {
    atIndex = "#m";
    atPos7 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos8 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 8) {
    atIndex = "#,";
    atPos8 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos9 = false;
    atPos0 = false;
  }
  else if (index == 9) {
    atIndex = "#.";
    atPos9 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos0 = false;
  }
  else if (index == 10) {
    atIndex = "#/";
    atPos0 = true;
    atPos1 = false;
    atPos2 = false;
    atPos3 = false;
    atPos4 = false;
    atPos5 = false;
    atPos6 = false;
    atPos7 = false;
    atPos8 = false;
    atPos9 = false;
  }

  delay(100);     // delay for serial read

  Serial1.println(atIndex);
  //Serial2.println(atIndex);
  //Serial3.println(atIndex);

  //Serial.println(String("At index: ") + index + String("\n"));
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
