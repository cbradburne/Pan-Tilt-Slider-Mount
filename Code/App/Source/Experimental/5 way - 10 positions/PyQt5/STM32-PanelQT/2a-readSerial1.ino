
//  --  Read Serial

/*

  Z   Set pos
  X
  C
  V
  B
  N

  A   Run to pos
  S
  D
  F
  G
  H

  z   At pos, post run
  x
  c
  v
  b
  n

  a   Clear all saved positions
  s   Change any LEDs from "set pos" to "away from pos"

  $   End on Trans

  ------

  q   Slider speed
  w
  e
  r
  t
  y
  u

  Q   Pan speed
  W
  E
  R
  T
  Y
  U

  1   Tilt speed
  2
  3
  4
  5
  6
  7

  I   Zoom in
  i   Zoom out

  o   Zoom STOP

  O   Toggle recording
  P   Is Recording
  p   Is NOT Recording

  ------

  ^   LEDsliderSpeed

*/

void readSerial1() {
  if (Serial1.available() > 0) {
    char c = Serial1.read();
    if (c == '#') {
      while (Serial1.available() < 2) {                        //  Wait until 2 bytes available
        delayMicroseconds(200);
      }
      c = Serial1.read();
      //char closs = Serial1.read();
      switch (c) {
        case 'Z': {                                           // Save pos 1
            cam1pos1set = true;
            displayCommand = 111;
          }
          break;
        case 'X': {                                           // Save pos 2
            cam1pos2set = true;
            displayCommand = 121;
          }
          break;
        case 'C': {                                           // Save pos 3
            cam1pos3set = true;
            displayCommand = 131;
          }
          break;
        case 'V': {                                           // Save pos 4
            cam1pos4set = true;
            displayCommand = 141;
          }
          break;
        case 'B': {                                           // Save pos 5
            cam1pos5set = true;
            displayCommand = 151;
          }
          break;
        case 'N': {                                           // Save pos 6
            cam1pos6set = true;
            displayCommand = 161;
          }
          break;
        case 'A': {                                           // Moving to pos 1
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos1run = true;
            displayCommand = 112;
          }
          break;
        case 'S': {                                           // Moving to pos 2
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos2run = true;
            displayCommand = 122;
          }
          break;
        case 'D': {                                           // Moving to pos 3
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos3run = true;
            displayCommand = 132;
          }
          break;
        case 'F': {                                           // Moving to pos 4
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos4run = true;
            displayCommand = 142;
          }
          break;
        case 'G': {                                           // Moving to pos 5
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos5run = true;
            displayCommand = 152;
          }
          break;
        case 'H': {                                           // Moving to pos 6
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            cam1pos6run = true;
            displayCommand = 162;
          }
          break;
        case 'z': {                                           // At pos 1 post move to (run)
            cam1pos1run = false;
            cam1atPos1 = true;
            displayCommand = 113;
          }
          break;
        case 'x': {                                           // At pos 2
            cam1pos2run = false;
            cam1atPos2 = true;
            displayCommand = 123;
          }
          break;
        case 'c': {                                           // At pos 3
            cam1pos3run = false;
            cam1atPos3 = true;
            displayCommand = 133;
          }
          break;
        case 'v': {                                           // At pos 4
            cam1pos4run = false;
            cam1atPos4 = true;
            displayCommand = 143;
          }
          break;
        case 'b': {                                           // At pos 5
            cam1pos5run = false;
            cam1atPos5 = true;
            displayCommand = 153;
          }
          break;
        case 'n': {                                           // At pos 6
            cam1pos6run = false;
            cam1atPos6 = true;
            displayCommand = 163;
          }
          break;
        case 'a': {                                           // CLEAR ALL POSITIONS
            cam1pos1run = false;
            cam1pos1set = false;
            cam1atPos1 = false;
            cam1pos2run = false;
            cam1pos2set = false;
            cam1atPos2 = false;
            cam1pos3run = false;
            cam1pos3set = false;
            cam1atPos3 = false;
            cam1pos4run = false;
            cam1pos4set = false;
            cam1atPos4 = false;
            cam1pos5run = false;
            cam1pos5set = false;
            cam1atPos5 = false;
            cam1pos6run = false;
            cam1pos6set = false;
            cam1atPos6 = false;
            displayCommand = 100;
          }
          break;
        case 's': {                                           // Not at any stored position
            cam1atPos1 = false;
            cam1atPos2 = false;
            cam1atPos3 = false;
            cam1atPos4 = false;
            cam1atPos5 = false;
            cam1atPos6 = false;
            //displayUpadte = true;
            Serial.println("~?");
          }
          break;
        case 'd': {                                           // Default Speed Restored
            displayCommand = 001;
          }
          break;
        case 'I': {                                           // Zoom In
            zoomIN = true;
            zoomOUT = false;
            zoom_speed = Serial1.read();
            zoom_speed -= 48;
            displayCommand = 115;
          }
          break;
        case 'i': {                                           // Zoom Out
            zoomIN = false;
            zoomOUT = true;
            zoom_speed = Serial1.read();
            zoom_speed -= 48;
            displayCommand = 125;
          }
          break;
        case 'o': {                                           // Zoom Stop
            zoomIN = false;
            zoomOUT = false;
            zoom_speed = 0;
            displayCommand = 000;
          }
          break;
        case 'p': {                                           // Is NOT Recording
            isRecording = false;
            displayCommand = 114;
          }
          break;
        case 'P': {                                           // Is Recording
            isRecording = true;
            displayCommand = 124;
          }
          break;
        case '0': {                                           // Reset LEDs sent by other
            Serial.println("~100");
            Serial.println("~200");
            Serial.println("~300");

            cam1pos1run = false;
            cam1pos1set = false;
            cam1atPos1 = false;
            cam1pos2run = false;
            cam1pos2set = false;
            cam1atPos2 = false;
            cam1pos3run = false;
            cam1pos3set = false;
            cam1atPos3 = false;
            cam1pos4run = false;
            cam1pos4set = false;
            cam1atPos4 = false;
            cam1pos5run = false;
            cam1pos5set = false;
            cam1atPos5 = false;
            cam1pos6run = false;
            cam1pos6set = false;
            cam1atPos6 = false;

            cam2pos1run = false;
            cam2pos1set = false;
            cam2atPos1 = false;
            cam2pos2run = false;
            cam2pos2set = false;
            cam2atPos2 = false;
            cam2pos3run = false;
            cam2pos3set = false;
            cam2atPos3 = false;
            cam2pos4run = false;
            cam2pos4set = false;
            cam2atPos4 = false;
            cam2pos5run = false;
            cam2pos5set = false;
            cam2atPos5 = false;
            cam2pos6run = false;
            cam2pos6set = false;
            cam2atPos6 = false;

            cam3pos1run = false;
            cam3pos1set = false;
            cam3atPos1 = false;
            cam3pos2run = false;
            cam3pos2set = false;
            cam3atPos2 = false;
            cam3pos3run = false;
            cam3pos3set = false;
            cam3atPos3 = false;
            cam3pos4run = false;
            cam3pos4set = false;
            cam3atPos4 = false;
            cam3pos5run = false;
            cam3pos5set = false;
            cam3atPos5 = false;
            cam3pos6run = false;
            cam3pos6set = false;
            cam3atPos6 = false;
          }
          break;
      }
    }
    else if (c == '^') {
      while (Serial1.available() < 2) {                        //  Wait for 2 bytes to be available
        delayMicroseconds(200);
      }
      c = Serial1.read();
      if (c == '=') {
        s1Speed = Serial1.read();
        s1Speed -= 48;
        Serial.print("=1");
        Serial.println(s1Speed);
      }

      else if (c == '@') {
        cam1PTSpeed = Serial1.read();
        cam1PTSpeed -= 48;
        Serial.print("=@1");
        Serial.println(cam1PTSpeed);
      }
    }
    else if (c == 'W') {
      ;
    }
    else if (c == '\n') {
      ;
    }
    else if (c == '\r') {
      ;
    }
    else if (c == '?') {
      String readSerial = Serial1.readStringUntil('\n');
    }

    else if (c == '!') {
      String readSerial = Serial1.readStringUntil('\n');
    }

    else if (c == '@') {
      String readSerial = Serial1.readStringUntil('\n');
    }

    else if (c == 4) {
      String readSerial = Serial1.readStringUntil('\n');
    }

    else {
      inData1 = "\nCam1:\n";
      inData1 += c;
      while (Serial1.available() > 0) {
        inData1 += Serial1.readStringUntil('\n');
        Serial.println(inData1);
        inData1 = "";
        delay(2);
      }
    }
  }
}
