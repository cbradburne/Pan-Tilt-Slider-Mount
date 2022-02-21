
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

void readSerial4() {
  if (Serial4.available() > 0) {
    char g = Serial4.read();
    if (g == '#') {
      while (Serial4.available() < 2) {                        //  Wait until 2 bytes available
        delayMicroseconds(200);
      }
      g = Serial4.read();
      //char gLoss = Serial4.read();
      switch (g) {
        case 'Z': {                                           // Save pos 1
            cam3pos1set = true;
            displayCommand = 311;
          }
          break;
        case 'X': {                                           // Save pos 2
            cam3pos2set = true;
            displayCommand = 321;
          }
          break;
        case 'C': {                                           // Save pos 3
            cam3pos3set = true;
            displayCommand = 331;
          }
          break;
        case 'V': {                                           // Save pos 4
            cam3pos4set = true;
            displayCommand = 341;
          }
          break;
        case 'B': {                                           // Save pos 5
            cam3pos5set = true;
            displayCommand = 351;
          }
          break;
        case 'N': {                                           // Save pos 6
            cam3pos6set = true;
            displayCommand = 361;
          }
          break;
        case 'A': {                                           // Moving to pos 1
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos1run = true;
            displayCommand = 312;
          }
          break;
        case 'S': {                                           // Moving to pos 2
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos2run = true;
            displayCommand = 322;
          }
          break;
        case 'D': {                                           // Moving to pos 3
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos3run = true;
            displayCommand = 332;
          }
          break;
        case 'F': {                                           // Moving to pos 4
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos4run = true;
            displayCommand = 342;
          }
          break;
        case 'G': {                                           // Moving to pos 5
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos5run = true;
            displayCommand = 352;
          }
          break;
        case 'H': {                                           // Moving to pos 6
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            cam3pos6run = true;
            displayCommand = 362;
          }
          break;
        case 'z': {                                           // At pos 1 post move to (run)
            cam3pos1run = false;
            cam3atPos1 = true;
            displayCommand = 313;
          }
          break;
        case 'x': {                                           // At pos 2
            cam3pos2run = false;
            cam3atPos2 = true;
            displayCommand = 323;
          }
          break;
        case 'c': {                                           // At pos 3
            cam3pos3run = false;
            cam3atPos3 = true;
            displayCommand = 333;
          }
          break;
        case 'v': {                                           // At pos 4
            cam3pos4run = false;
            cam3atPos4 = true;
            displayCommand = 343;
          }
          break;
        case 'b': {                                           // At pos 5
            cam3pos5run = false;
            cam3atPos5 = true;
            displayCommand = 353;
          }
          break;
        case 'n': {                                           // At pos 6
            cam3pos6run = false;
            cam3atPos6 = true;
            displayCommand = 363;
          }
          break;
        case 'a': {                                           // CLEAR ALL POSITIONS
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
            displayCommand = 300;
          }
          break;
        case 's': {                                           // Not at any stored position
            cam3atPos1 = false;
            cam3atPos2 = false;
            cam3atPos3 = false;
            cam3atPos4 = false;
            cam3atPos5 = false;
            cam3atPos6 = false;
            //displayUpadte = true;
            Serial.println("~@");
          }
          break;
        case 'd': {                                           // Default Speed Restored
            displayCommand = 001;
          }
          break;
        case 'I': {                                           // Zoom In
            zoomIN = true;
            zoomOUT = false;
            zoom_speed = Serial4.read();
            //Serial3.print(zoom_speed);
            zoom_speed -= 48;
            displayCommand = 315;
          }
          break;
        case 'i': {                                           // Zoom Out
            zoomIN = false;
            zoomOUT = true;
            zoom_speed = Serial4.read();
            //Serial3.print(zoom_speed);
            zoom_speed -= 48;
            displayCommand = 325;
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
            displayCommand = 314;
          }
          break;
        case 'P': {                                           // Is Recording
            isRecording = true;
            displayCommand = 324;
          }
          break;
      }
    }
    else if (g == '^') {
      while (Serial4.available() < 2) {                        //  Wait until 2 bytes available
        delayMicroseconds(200);
      }
      g = Serial4.read();
      if (g == '=') {
        s3Speed = Serial4.read();
        s3Speed -= 48;
        Serial.print("=3");
        Serial.println(s3Speed);
      }

      else if (g == '@') {
        cam3PTSpeed = Serial4.read();
        cam3PTSpeed -= 48;
        Serial.print("=@3");
        Serial.println(cam3PTSpeed);
      }
    }
    else if (g == 'W') {
      ;
    }
    else if (g == '\n') {
      ;
    }
    else if (g == '\r') {
      ;
    }
    else if (g == '?') {
      String readSerial = Serial4.readStringUntil('\n');
    }

    else if (g == '!') {
      String readSerial = Serial4.readStringUntil('\n');
    }

    else if (g == '@') {
      String readSerial = Serial4.readStringUntil('\n');
    }

    else if (g == 4) {
      String readSerial = Serial4.readStringUntil('\n');
    }

    else {
      inData3 = "\nCam3:\n";
      inData3 += g;
      while (Serial4.available() > 0) {
        inData3 += Serial4.readStringUntil('\n');
        Serial.println(inData3);
        inData3 = "";
        delay(2);
      }
    }
  }
}
