//  Send LED status to remote


void doRemoteControlLEDs(void) {
  if (atPos1) {
    Serial1.println("#z");
    Serial2.println("#z");
    Serial3.println("#z");
  }
  if (pos1set) {
    Serial1.println("#Z");
    Serial2.println("#Z");
    Serial3.println("#Z");
  }
  if (atPos2) {
    Serial1.println("#x");
    Serial2.println("#x");
    Serial3.println("#x");
  }
  if (pos2set) {
    Serial1.println("#X");
    Serial2.println("#X");
    Serial3.println("#X");
  }
  if (atPos3) {
    Serial1.println("#c");
    Serial2.println("#c");
    Serial3.println("#c");
  }
  if (pos3set) {
    Serial1.println("#C");
    Serial2.println("#C");
    Serial3.println("#C");
  }
  if (atPos4) {
    Serial1.println("#v");
    Serial2.println("#v");
    Serial3.println("#v");
  }
  if (pos4set) {
    Serial1.println("#V");
    Serial2.println("#V");
    Serial3.println("#V");
  }
  if (atPos5) {
    Serial1.println("#b");
    Serial2.println("#b");
    Serial3.println("#b");
  }
  if (pos5set) {
    Serial1.println("#B");
    Serial2.println("#B");
    Serial3.println("#B");
  }
  if (atPos6) {
    Serial1.println("#n");
    Serial2.println("#n");
    Serial3.println("#n");
  }
  if (pos6set) {
    Serial1.println("#N");
    Serial2.println("#N");
    Serial3.println("#N");
  }
  if (atPos7) {
    Serial1.println("#m");
    Serial2.println("#m");
    Serial3.println("#m");
  }
  if (pos7set) {
    Serial1.println("#M");
    Serial2.println("#M");
    Serial3.println("#M");
  }
  if (atPos8) {
    Serial1.println("#,");
    Serial2.println("#,");
    Serial3.println("#,");
  }
  if (pos8set) {
    Serial1.println("#<");
    Serial2.println("#<");
    Serial3.println("#<");
  }
  if (atPos9) {
    Serial1.println("#.");
    Serial2.println("#.");
    Serial3.println("#.");
  }
  if (pos9set) {
    Serial1.println("#>");
    Serial2.println("#>");
    Serial3.println("#>");
  }
  if (atPos0) {
    Serial1.println("#/");
    Serial2.println("#/");
    Serial3.println("#/");
  }
  if (pos0set) {
    Serial1.println("#?");
    Serial2.println("#?");
    Serial3.println("#?");
  }
  if (slider_set_speed == slider_max_speed) {
    Serial1.println("^=7");
    Serial2.println("^=7");
    Serial3.println("^=7");
  }
  else {
    LEDsliderSpeed = 7 - ((7 / ((slider_max_speed - slider_min_speed) / ((slider_max_speed - slider_min_speed) - (slider_set_speed - slider_min_speed)) )));
    Serial1.print("^=");
    Serial1.println(LEDsliderSpeed);
    Serial2.print("^=");
    Serial2.println(LEDsliderSpeed);
    Serial3.print("^=");
    Serial3.println(LEDsliderSpeed);
  }
  if (pan_set_speed == 20) {
    Serial1.println("^@7");
    Serial2.println("^@7");
    Serial3.println("^@7");
  }
  else if (pan_set_speed == 10) {
    Serial1.println("^@5");
    Serial2.println("^@5");
    Serial3.println("^@5");
  }
  else if (pan_set_speed == 5) {
    Serial1.println("^@3");
    Serial2.println("^@3");
    Serial3.println("^@3");
  }
  else if (pan_set_speed == 1) {
    Serial1.println("^@1");
    Serial2.println("^@1");
    Serial3.println("^@1");
  }
}
