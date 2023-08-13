//  Reports

void debugReport(void) {
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
    Serial1.println(String("Keyframe index: ") + (row + 1));
    Serial1.print(String("Pan   : ") + panStepsToDegrees(keyframe_array[row].panStepCount) + String("°\t"));
    Serial1.print(String("Tilt  : ") + tiltStepsToDegrees(keyframe_array[row].tiltStepCount) + String("°\t"));
    Serial1.println(String("Slider: ") + sliderStepsToMillimetres(keyframe_array[row].sliderStepCount) + String("mm\t"));
    Serial1.print(String("Pan Speed   : ") + panStepsToDegrees(keyframe_array[row].panSpeed) + String(" °/s\t"));
    Serial1.print(String("Tilt Speed  : ") + tiltStepsToDegrees(keyframe_array[row].tiltSpeed) + String(" °/s\t"));
    Serial1.println(String("Slider Speed: ") + sliderStepsToMillimetres(keyframe_array[row].sliderSpeed) + String(" mm/s"));
    Serial1.println("-");

    row++;
  } while (row < 10);

  Serial1.print("\n");
  Serial1.println("#$");
}