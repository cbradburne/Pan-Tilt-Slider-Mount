// Serial Manual Moves

void panDegrees(float panAngle) {

  Serial1.println("#s");        //  Clear external "At Pos" LEDs
  Serial1.println("#s");
  Serial1.println(String("Current Pan Position   : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial1.println(String("Target  Pan Position   : ") + panAngle + String("°"));
  Serial1.println("-");
  Serial1.println("#$");

  stepper_pan.setTargetAbs(panDegreesToSteps(panAngle));
  step_stepperP.move(stepper_pan);

  sentMoved = false;

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
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void panDegreesRel(float panAngle) {

  Serial1.println("#s");        //  Clear external "At Pos" LEDs
  Serial1.println("#s");
  Serial1.println(String("Current Pan Position   : ") + panStepsToDegrees(stepper_pan.getPosition()) + String("°"));
  Serial1.println(String("Relative Pan Position  : ") + (panStepsToDegrees(stepper_pan.getPosition()) + panAngle) + String("°"));
  Serial1.println("-");
  Serial1.println("#$");

  stepper_pan.setTargetRel(panDegreesToSteps(panAngle));
  step_stepperP.move(stepper_pan);

  sentMoved = false;

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
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void tiltDegrees(float tiltAngle) {

  Serial1.println("#s");        //  Clear external "At Pos" LEDs
  Serial1.println("#s");
  Serial1.println(String("Current Tilt Position  : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial1.println(String("Relative Tilt Position : ") + tiltAngle + String("°"));
  Serial1.println("-");
  Serial1.println("#$");

  stepper_tilt.setTargetAbs(tiltDegreesToSteps(tiltAngle));
  step_stepperT.move(stepper_tilt);

  sentMoved = false;

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
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void tiltDegreesRel(float tiltAngle) {

  Serial1.println("#s");        //  Clear external "At Pos" LEDs
  Serial1.println("#s");
  Serial1.println(String("Current Tilt Position  : ") + tiltStepsToDegrees(stepper_tilt.getPosition()) + String("°"));
  Serial1.println(String("Target  Tilt Position  : ") + (tiltStepsToDegrees(stepper_tilt.getPosition()) + tiltAngle) + String("°"));
  Serial1.println("-");
  Serial1.println("#$");

  stepper_tilt.setTargetRel(tiltDegreesToSteps(tiltAngle));
  step_stepperT.move(stepper_tilt);

  sentMoved = false;

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
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void sliderMoveTo(float mm) {
  if (withSlider) {
    Serial1.println("#s");        //  Clear external "At Pos" LEDs
    Serial1.println("#s");
    Serial1.println(String("Current Slider Position: ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String(" mm"));
    Serial1.println(String("Target Slider Position : ") + mm + String(" mm"));
    Serial1.println("-");
    Serial1.println("#$");

    stepper_slider.setTargetAbs(sliderMillimetresToSteps(mm));
    step_stepperS.move(stepper_slider);

    sentMoved = false;

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
  }
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void sliderMMRel(float mm) {
  if (withSlider) {
    Serial1.println("#s");        //  Clear external "At Pos" LEDs
    Serial1.println("#s");
    Serial1.println(String("Current Slider Position: ") + sliderStepsToMillimetres(stepper_slider.getPosition()) + String(" mm"));
    Serial1.println(String("Target Slider Position : ") + (sliderStepsToMillimetres(stepper_slider.getPosition()) + mm) + String(" mm"));
    Serial1.println("-");
    Serial1.println("#$");

    stepper_slider.setTargetRel(sliderMillimetresToSteps(mm));
    step_stepperS.move(stepper_slider);

    sentMoved = false;

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
  }
}