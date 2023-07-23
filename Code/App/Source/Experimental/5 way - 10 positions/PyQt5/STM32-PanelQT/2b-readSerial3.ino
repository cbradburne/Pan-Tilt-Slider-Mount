
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

void readSerial3() {
  if (Serial3.available() > 0) {
    char e = Serial3.read();
    if (e == '#') {
      while (Serial3.available() < 2) {                        //  Wait until 2 bytes available
        delayMicroseconds(200);
      }
      e = Serial3.read();
      //char eLoss = Serial3.read();
      switch (e) {
        case 'Z': {                                           // Save pos 1
            cam2pos1set = true;
            displayCommand = 211;
          }
          break;
        case 'X': {                                           // Save pos 2
            cam2pos2set = true;
            displayCommand = 221;
          }
          break;
        case 'C': {                                           // Save pos 3
            cam2pos3set = true;
            displayCommand = 231;
          }
          break;
        case 'V': {                                           // Save pos 4
            cam2pos4set = true;
            displayCommand = 241;
          }
          break;
        case 'B': {                                           // Save pos 5
            cam2pos5set = true;
            displayCommand = 251;
          }
          break;
        case 'N': {                                           // Save pos 6
            cam2pos6set = true;
            displayCommand = 261;
          }
          break;
        case 'A': {                                           // Moving to pos 1
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos1run = true;
            displayCommand = 212;
          }
          break;
        case 'S': {                                           // Moving to pos 2
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos2run = true;
            displayCommand = 222;
          }
          break;
        case 'D': {                                           // Moving to pos 3
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos3run = true;
            displayCommand = 232;
          }
          break;
        case 'F': {                                           // Moving to pos 4
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos4run = true;
            displayCommand = 242;
          }
          break;
        case 'G': {                                           // Moving to pos 5
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos5run = true;
            displayCommand = 252;
          }
          break;
        case 'H': {                                           // Moving to pos 6
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            cam2pos6run = true;
            displayCommand = 262;
          }
          break;
        case 'z': {                                           // At pos 1 post move to (run)
            cam2pos1run = false;
            cam2atPos1 = true;
            displayCommand = 213;
          }
          break;
        case 'x': {                                           // At pos 2
            cam2pos2run = false;
            cam2atPos2 = true;
            displayCommand = 223;
          }
          break;
        case 'c': {                                           // At pos 3
            cam2pos3run = false;
            cam2atPos3 = true;
            displayCommand = 233;
          }
          break;
        case 'v': {                                           // At pos 4
            cam2pos4run = false;
            cam2atPos4 = true;
            displayCommand = 243;
          }
          break;
        case 'b': {                                           // At pos 5
            cam2pos5run = false;
            cam2atPos5 = true;
            displayCommand = 253;
          }
          break;
        case 'n': {                                           // At pos 6
            cam2pos6run = false;
            cam2atPos6 = true;
            displayCommand = 263;
          }
          break;
        case 'a': {                                           // CLEAR ALL POSITIONS
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
            displayCommand = 200;
          }
          break;
        case 's': {                                           // Not at any stored position
            cam2atPos1 = false;
            cam2atPos2 = false;
            cam2atPos3 = false;
            cam2atPos4 = false;
            cam2atPos5 = false;
            cam2atPos6 = false;
            //displayUpadte = true;
            Serial.println("~!");
          }
          break;
        case 'd': {                                           // Default Speed Restored
            displayCommand = 001;
          }
          break;
        case 'I': {                                           // Zoom In
            zoomIN = true;
            zoomOUT = false;
            zoom_speed = Serial3.read();
            //Serial3.print(zoom_speed);
            zoom_speed -= 48;
            displayCommand = 215;
          }
          break;
        case 'i': {                                           // Zoom Out
            zoomIN = false;
            zoomOUT = true;
            zoom_speed = Serial3.read();
            zoom_speed -= 48;
            displayCommand = 225;
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
            displayCommand = 214;
          }
          break;
        case 'P': {                                           // Is Recording
            isRecording = true;
            displayCommand = 224;
          }
          break;
      }
    }
    else if (e == '^') {
      while (Serial3.available() < 2) {                        //  Wait until 2 bytes available
        delayMicroseconds(200);
      }
      e = Serial3.read();
      if (e == '=') {
        s2Speed = Serial3.read();
        s2Speed -= 48;
        Serial.print("=2");
        Serial.println(s2Speed);
      }

      else if (e == '@') {
        cam2PTSpeed = Serial3.read();
        cam2PTSpeed -= 48;
        Serial.print("=@2");
        Serial.println(cam2PTSpeed);
      }
    }
    else if (e == 'W') {
      ;
    }
    else if (e == '\n') {
      ;
    }
    else if (e == '\r') {
      ;
    }
    else if (e == '?') {
      String readSerial = Serial3.readStringUntil('\n');
    }

    else if (e == '!') {
      String readSerial = Serial3.readStringUntil('\n');
    }

    else if (e == '@') {
      String readSerial = Serial3.readStringUntil('\n');
    }

    else if (e == 4) {
      String readSerial = Serial3.readStringUntil('\n');
    }

    else {
      inData2 = "\nCam2:\n";
      inData2 += e;
      while (Serial3.available() > 0) {
        inData2 += Serial3.readStringUntil('\n');
        Serial.println(inData2);
        inData2 = "";
        delay(2);
      }
    }
  }
}
