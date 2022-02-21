//  Reports


void debugReport(void) {

  Serial.println("Debug Report:");
  Serial.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));
  Serial.println(String("Pan steps         : ") + panDegreesToSteps(pan_set_speed) + String(" steps/s"));
  Serial.println(String("Tilt steps        : ") + tiltDegreesToSteps(tilt_set_speed) + String(" steps/s"));
  Serial.println(String("Slider steps      : ") + sliderMillimetresToSteps(slider_set_speed) + String(" steps/s\n"));
  Serial.println(String("Pan set speed     : ") + pan_set_speed + String("°/s"));
  Serial.println(String("Tilt set speed    : ") + tilt_set_speed + String("°/s"));
  Serial.println(String("Slider set speed  : ") + slider_set_speed + String("mm/s\n"));
  Serial.println(String("Pan Accel         : ") + pan_accel + String(" steps/s²"));
  Serial.println(String("Tilt Accel        : ") + tilt_accel + String(" steps/s²"));
  Serial.println(String("Slider Accel      : ") + slider_accel + String(" steps/s²\n"));
  Serial.println(String("Pan Joy Accel Factor    : ") + panAccelJoy);
  Serial.println(String("Tilt Joy Accel Factor   : ") + tiltAccelJoy);
  Serial.println(String("Slider Joy Accel Factor : ") + sliderAccelJoy + String("\n"));

  Serial1.println("Debug Report:");
  Serial1.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial1.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial1.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));
  Serial1.println(String("Pan steps         : ") + panDegreesToSteps(pan_set_speed) + String(" steps/s"));
  Serial1.println(String("Tilt steps        : ") + tiltDegreesToSteps(tilt_set_speed) + String(" steps/s"));
  Serial1.println(String("Slider steps      : ") + sliderMillimetresToSteps(slider_set_speed) + String(" steps/s\n"));
  Serial1.println(String("Pan set speed     : ") + pan_set_speed + String("°/s"));
  Serial1.println(String("Tilt set speed    : ") + tilt_set_speed + String("°/s"));
  Serial1.println(String("Slider set speed  : ") + slider_set_speed + String("mm/s\n"));
  Serial1.println(String("Pan Accel         : ") + pan_accel + String(" steps/s²"));
  Serial1.println(String("Tilt Accel        : ") + tilt_accel + String(" steps/s²"));
  Serial1.println(String("Slider Accel      : ") + slider_accel + String(" steps/s²\n"));
  Serial1.println(String("Pan Joy Accel Factor    : ") + panAccelJoy);
  Serial1.println(String("Tilt Joy Accel Factor   : ") + tiltAccelJoy);
  Serial1.println(String("Slider Joy Accel Factor : ") + sliderAccelJoy + String("\n"));

  printEEPROM();
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void positionReport(void) {
  Serial.println("Position Report:");
  Serial.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));

  Serial1.println("Position Report:");
  Serial1.println(String("Pan angle         : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial1.println(String("Tilt angle        : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial1.println(String("Slider position   : ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String("mm\n"));
  Serial1.println("#$");
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void printKeyframeElements(void) {
  int row = 0;
  do {
    /*
    Serial.println(String("Keyframe index: ") + (row + 1));
    Serial.print(String("Pan   : ") + panStepsToDegrees(keyframe_array[row].panStepCount) + String("°\t"));
    Serial.print(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[row].tiltStepCount) + String("°\t"));
    Serial.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[row].sliderStepCount) + String("mm\t"));
    Serial.print(String("Pan Speed   : ") + panStepsToDegrees(keyframe_array[row].panSpeed) + String(" °/s\t"));
    Serial.print(String("Tilt Speed  : ") + tiltStepsToDegrees(keyframe_array[row].tiltSpeed) + String(" °/s\t"));
    Serial.println(String("Slider Speed: ") + sliderStepsToMillimetres(keyframe_array[row].sliderSpeed) + String(" mm/s"));
    Serial.println("-");
    */

    Serial1.println(String("Keyframe index: ") + (row + 1));
    Serial1.print(String("Pan   : ") + panStepsToDegrees(keyframe_array[row].panStepCount) + String("°\t"));
    Serial1.print(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[row].tiltStepCount) + String("°\t"));
    Serial1.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[row].sliderStepCount) + String("mm\t"));
    Serial1.print(String("Pan Speed   : ") + panStepsToDegrees(keyframe_array[row].panSpeed) + String(" °/s\t"));
    Serial1.print(String("Tilt Speed  : ") + tiltStepsToDegrees(keyframe_array[row].tiltSpeed) + String(" °/s\t"));
    Serial1.println(String("Slider Speed: ") + sliderStepsToMillimetres(keyframe_array[row].sliderSpeed) + String(" mm/s"));
    Serial1.println("-");

    row++;
  } while (row < 6);

  Serial.print("\n");
  Serial1.print("\n");
  Serial1.println("#$");
}
