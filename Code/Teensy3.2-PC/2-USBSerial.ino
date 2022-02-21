void USBSerialData() {
  if (Serial.available()) {                                   // If anything comes in Serial (USB),
    char instruction = Serial.read();
    if (instruction == '&') {
      while (Serial.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(1);
      }
      instruction = Serial.read();
      switch (instruction) {
        case 'Z': {                                           // Cam 1, Save pos 1
            Serial1.println("?M1");
          }
          break;
        case 'X': {                                           // Cam 1, Save pos 2
            Serial1.println("?M2");
          }
          break;
        case 'C': {                                           // Cam 1, Save pos 3
            Serial1.println("?M3");
          }
          break;
        case 'V': {                                           // Cam 1, Save pos 4
            Serial1.println("?M4");
          }
          break;
        case 'B': {                                           // Cam 1, Save pos 5
            Serial1.println("?M5");
          }
          break;
        case 'N': {                                           // Cam 1, Save pos 6
            Serial1.println("?M6");
          }
          break;
        case 'z': {                                           // Cam 1, Move to pos 1
            Serial1.println("?m1");
          }
          break;
        case 'x': {                                           // Cam 1, Move to pos 2
            Serial1.println("?m2");
          }
          break;
        case 'c': {                                           // Cam 1, Move to pos 3
            Serial1.println("?m3");
          }
          break;
        case 'v': {                                           // Cam 1, Move to pos 4
            Serial1.println("?m4");
          }
          break;
        case 'b': {                                           // Cam 1, Move to pos 5
            Serial1.println("?m5");
          }
          break;
        case 'n': {                                           // Cam 1, Move to pos 6
            Serial1.println("?m6");
          }
          break;
        case 'A': {                                           // Cam 2, Save pos 1
            Serial2.println("?M1");
          }
          break;
        case 'S': {                                           // Cam 2, Save pos 2
            Serial2.println("?M2");
          }
          break;
        case 'D': {                                           // Cam 2, Save pos 3
            Serial2.println("?M3");
          }
          break;
        case 'F': {                                           // Cam 2, Save pos 4
            Serial2.println("?M4");
          }
          break;
        case 'G': {                                           // Cam 2, Save pos 5
            Serial2.println("?M5");
          }
          break;
        case 'H': {                                           // Cam 2, Save pos 6
            Serial2.println("?M6");
          }
          break;
        case 'a': {                                           // Cam 2, Move to pos 1
            Serial2.println("?m1");
          }
          break;
        case 's': {                                           // Cam 2, Move to pos 2
            Serial2.println("?m2");
          }
          break;
        case 'd': {                                           // Cam 2, Move to pos 3
            Serial2.println("?m3");
          }
          break;
        case 'f': {                                           // Cam 2, Move to pos 4
            Serial2.println("?m4");
          }
          break;
        case 'g': {                                           // Cam 2, Move to pos 5
            Serial2.println("?m5");
          }
          break;
        case 'h': {                                           // Cam 2, Move to pos 6
            Serial2.println("?m6");
          }
          break;
        case 'Q': {                                           // Cam 3, Save pos 1
            Serial3.println("?M1");
          }
          break;
        case 'W': {                                           // Cam 3, Save pos 2
            Serial3.println("?M2");
          }
          break;
        case 'E': {                                           // Cam 3, Save pos 3
            Serial3.println("?M3");
          }
          break;
        case 'R': {                                           // Cam 3, Save pos 4
            Serial3.println("?M4");
          }
          break;
        case 'T': {                                           // Cam 3, Save pos 5
            Serial3.println("?M5");
          }
          break;
        case 'Y': {                                           // Cam 3, Save pos 6
            Serial3.println("?M6");
          }
          break;
        case 'q': {                                           // Cam 3, Move to pos 1
            Serial3.println("?m1");
          }
          break;
        case 'w': {                                           // Cam 3, Move to pos 2
            Serial3.println("?m2");
          }
          break;
        case 'e': {                                           // Cam 3, Move to pos 3
            Serial3.println("?m3");
          }
          break;
        case 'r': {                                           // Cam 3, Move to pos 4
            Serial3.println("?m4");
          }
          break;
        case 't': {                                           // Cam 3, Move to pos 5
            Serial3.println("?m5");
          }
          break;
        case 'y': {                                           // Cam 3, Move to pos 6
            Serial3.println("?m6");
          }
          break;
        case 'm': {                                           // Cam 1, Decrease speed
            Serial1.println("?b");
          }
          break;
        case 'M': {                                           // Cam 1, Increase speed
            Serial1.println("?B");
          }
          break;
        case 'j': {                                           // Cam 2, Decrease speed
            Serial2.println("?b");
          }
          break;
        case 'J': {                                           // Cam 2, Increase speed
            Serial2.println("?B");
          }
          break;
        case 'u': {                                           // Cam 3, Decrease speed
            Serial3.println("?b");
          }
          break;
        case 'U': {                                           // Cam 3, Increase speed
            Serial3.println("?B");
          }
          break;
        case ',': {                                           // Cam 1, Zoom out
            Serial1.println("?z1");
          }
          break;
        case '<': {                                           // Cam 1, Zoom in
            Serial1.println("?Z1");
          }
          break;
        case 'k': {                                           // Cam 2, Zoom out
            Serial2.println("?z1");
          }
          break;
        case 'K': {                                           // Cam 2, Zoom in
            Serial2.println("?Z1");
          }
          break;
        case 'i': {                                           // Cam 3, Zoom out
            Serial3.println("?z1");
          }
          break;
        case 'I': {                                           // Cam 3, Zoom in
            Serial3.println("?Z1");
          }
          break;
        case '>': {                                           // Cam 1, Zoom STOP
            Serial1.println("?N");
          }
          break;
        case 'L': {                                           // Cam 2, Zoom STOP
            Serial2.println("?N");
          }
          break;
        case 'O': {                                           // Cam 3, Zoom STOP
            Serial3.println("?N");
          }
          break;
        case '.': {                                           // Cam 1, Toggle recording
            Serial1.println("?u");
          }
          break;
        case 'l': {                                           // Cam 2, Toggle recording
            Serial2.println("?u");
          }
          break;
        case 'o': {                                           // Cam 3, Toggle recording
            Serial3.println("?u");
          }
          break;
        case '%': {                                           // Cam 1, Clear Positions
            Serial1.println("?Y");
          }
          break;
        case '^': {                                           // Cam 2, Clear Positions
            Serial2.println("?Y");
          }
          break;
        case '&': {                                           // Cam 3, Clear Positions
            Serial3.println("?Y");
          }
          break;
        case '(': {
            while (Serial.available() < 1) {                        //  Wait for 1 byte to be available.
              delayMicroseconds(1);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Report
              Serial1.println("?R");
            }
            else if (instruction == '2') {                   // Cam2, Report
              Serial2.println("?R");
            }
            else if (instruction == '3') {                   // Cam3, Report
              Serial3.println("?R");
            }
          }
          break;
        case ')': {
            while (Serial.available() < 1) {                        //  Wait for 1 byte to be available.
              delayMicroseconds(1);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Pos Report
              Serial1.println("?r");
            }
            else if (instruction == '2') {                   // Cam2, Pos Report
              Serial2.println("?r");
            }
            else if (instruction == '3') {                   // Cam3, Pos Report
              Serial3.println("?r");
            }
          }
          break;
        case '-': {
            while (Serial.available() < 1) {                        //  Wait for 1 byte to be available.
              delayMicroseconds(1);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Keyframe Report
              Serial1.println("?k");
            }
            else if (instruction == '2') {                   // Cam2, Keyframe Report
              Serial2.println("?k");
            }
            else if (instruction == '3') {                   // Cam3, Keyframe Report
              Serial3.println("?k");
            }
          }
          break;
        case '+': {
            while (Serial.available() < 2) {                        //  Wait for 1 byte to be available.
              delayMicroseconds(1);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Keyframe Report
              instruction = Serial.read();
              if (instruction == '1') {
                Serial1.print("?s");
                Serial1.println(speed1);
                //delay(500);
                //Serial1.print("?S");
                //Serial1.println(speed1);
              }
              else if (instruction == '2') {
                Serial1.print("?s");
                Serial1.println(speed2);
                //delay(500);
                //Serial1.print("?S");
                //Serial1.println(speed2);
              }
              else if (instruction == '3') {
                Serial1.print("?s");
                Serial1.println(speed3);
                //delay(500);
                //Serial1.print("?S");
                //Serial1.println(speed3);
              }
              else if (instruction == '4') {
                Serial1.print("?s");
                Serial1.println(speed4);
                //delay(500);
                //Serial1.print("?S");
                //Serial1.println(speed4);
              }
            }
            else if (instruction == '2') {
              instruction = Serial.read();
              if (instruction == '1') {
                Serial2.print("?s");
                Serial2.println(speed1);
                //delay(500);
                //Serial2.print("?S");
                //Serial2.println(speed1);
              }
              else if (instruction == '2') {
                Serial2.print("?s");
                Serial2.println(speed2);
                //delay(500);
                //Serial2.print("?S");
                //Serial2.println(speed2);
              }
              else if (instruction == '3') {
                Serial2.print("?s");
                Serial2.println(speed3);
                //delay(500);
                //Serial2.print("?S");
                //Serial2.println(speed3);
              }
              else if (instruction == '4') {
                Serial2.print("?s");
                Serial2.println(speed4);
                //delay(500);
                //Serial2.print("?S");
                //Serial2.println(speed4);
              }
            }
            else if (instruction == '3') {
              instruction = Serial.read();
              if (instruction == '1') {
                Serial3.print("?s");
                Serial3.println(speed1);
                //delay(500);
                //Serial3.print("?S");
                //Serial3.println(speed1);
              }
              else if (instruction == '2') {
                Serial3.print("?s");
                Serial3.println(speed2);
                //delay(500);
                //Serial3.print("?S");
                //Serial3.println(speed2);
              }
              else if (instruction == '3') {
                Serial3.print("?s");
                Serial3.println(speed3);
                //delay(500);
                //Serial3.print("?S");
                //Serial3.println(speed3);
              }
              else if (instruction == '4') {
                Serial3.print("?s");
                Serial3.println(speed4);
                //delay(500);
                //Serial3.print("?S");
                //Serial3.println(speed4);
              }
            }
          }
          break;
        case '!': {
            resetLEDs = true;
          }
          break;
      }
    }
    else if (instruction == 4) {
      delay(1);
      while (Serial.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      short ZShortPC = (Serial.read() << 8) + Serial.read();
      short XShortPC = (Serial.read() << 8) + Serial.read();
      short YShortPC = (Serial.read() << 8) + Serial.read();

      whichSerialCam = Serial.read();

      shortVals[0] = ZShortPC;
      shortVals[1] = XShortPC;
      shortVals[2] = YShortPC;

      sendSliderPanTiltStepSpeed(4, shortVals, whichSerialCam);
    }
    else if (instruction == '?') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData4 += received;
        if (received == '\n') {
          Serial1.println(inData4);
          inData4 = "";
        }
      }
    }
    else if (instruction == '!') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData4 += received;
        if (received == '\n') {
          Serial2.println(inData4);
          inData4 = "";
        }
      }
    }
    else if (instruction == '@') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData4 += received;
        if (received == '\n') {
          Serial3.println(inData4);
          inData4 = "";
        }
      }
    }
  }
}
