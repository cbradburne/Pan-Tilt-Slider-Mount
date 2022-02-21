
//  readSerial - USB port

void readSerial() {

  if (Serial.available() > 0) {
    char instruction = Serial.read();
    if (instruction == '&') {                                 //
      while (Serial.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(200);
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
            Serial3.println("?M1");
          }
          break;
        case 'S': {                                           // Cam 2, Save pos 2
            Serial3.println("?M2");
          }
          break;
        case 'D': {                                           // Cam 2, Save pos 3
            Serial3.println("?M3");
          }
          break;
        case 'F': {                                           // Cam 2, Save pos 4
            Serial3.println("?M4");
          }
          break;
        case 'G': {                                           // Cam 2, Save pos 5
            Serial3.println("?M5");
          }
          break;
        case 'H': {                                           // Cam 2, Save pos 6
            Serial3.println("?M6");
          }
          break;
        case 'a': {                                           // Cam 2, Move to pos 1
            Serial3.println("?m1");
          }
          break;
        case 's': {                                           // Cam 2, Move to pos 2
            Serial3.println("?m2");
          }
          break;
        case 'd': {                                           // Cam 2, Move to pos 3
            Serial3.println("?m3");
          }
          break;
        case 'f': {                                           // Cam 2, Move to pos 4
            Serial3.println("?m4");
          }
          break;
        case 'g': {                                           // Cam 2, Move to pos 5
            Serial3.println("?m5");
          }
          break;
        case 'h': {                                           // Cam 2, Move to pos 6
            Serial3.println("?m6");
          }
          break;
        case 'Q': {                                           // Cam 3, Save pos 1
            Serial4.println("?M1");
          }
          break;
        case 'W': {                                           // Cam 3, Save pos 2
            Serial4.println("?M2");
          }
          break;
        case 'E': {                                           // Cam 3, Save pos 3
            Serial4.println("?M3");
          }
          break;
        case 'R': {                                           // Cam 3, Save pos 4
            Serial4.println("?M4");
          }
          break;
        case 'T': {                                           // Cam 3, Save pos 5
            Serial4.println("?M5");
          }
          break;
        case 'Y': {                                           // Cam 3, Save pos 6
            Serial4.println("?M6");
          }
          break;
        case 'q': {                                           // Cam 3, Move to pos 1
            Serial4.println("?m1");
          }
          break;
        case 'w': {                                           // Cam 3, Move to pos 2
            Serial4.println("?m2");
          }
          break;
        case 'e': {                                           // Cam 3, Move to pos 3
            Serial4.println("?m3");
          }
          break;
        case 'r': {                                           // Cam 3, Move to pos 4
            Serial4.println("?m4");
          }
          break;
        case 't': {                                           // Cam 3, Move to pos 5
            Serial4.println("?m5");
          }
          break;
        case 'y': {                                           // Cam 3, Move to pos 6
            Serial4.println("?m6");
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
            Serial3.println("?b");
          }
          break;
        case 'J': {                                           // Cam 2, Increase speed
            Serial3.println("?B");
          }
          break;
        case 'u': {                                           // Cam 3, Decrease speed
            Serial4.println("?b");
          }
          break;
        case 'U': {                                           // Cam 3, Increase speed
            Serial4.println("?B");
          }
          break;
        case ',': {                                           // Cam 1, Zoom out
            Serial1.println("?z6");
          }
          break;
        case '<': {                                           // Cam 1, Zoom in
            Serial1.println("?Z6");
          }
          break;
        case 'k': {                                           // Cam 2, Zoom out
            Serial3.println("?z6");
          }
          break;
        case 'K': {                                           // Cam 2, Zoom in
            Serial3.println("?Z6");
          }
          break;
        case 'i': {                                           // Cam 3, Zoom out
            Serial4.println("?z6");
          }
          break;
        case 'I': {                                           // Cam 3, Zoom in
            Serial4.println("?Z6");
          }
          break;
        case '>': {                                           // Cam 1, Zoom STOP
            Serial1.println("?N");
          }
          break;
        case 'L': {                                           // Cam 2, Zoom STOP
            Serial3.println("?N");
          }
          break;
        case 'O': {                                           // Cam 3, Zoom STOP
            Serial4.println("?N");
          }
          break;
        case '.': {                                           // Cam 1, Toggle recording
            Serial1.println("?u");
          }
          break;
        case 'l': {                                           // Cam 2, Toggle recording
            Serial3.println("?u");
          }
          break;
        case 'o': {                                           // Cam 3, Toggle recording
            Serial4.println("?u");
          }
          break;
        case '%': {                                           // Cam 1, Clear Positions
            Serial1.println("?Y");
          }
          break;
        case '^': {                                           // Cam 2, Clear Positions
            Serial3.println("?Y");
          }
          break;
        case '&': {                                           // Cam 3, Clear Positions
            Serial4.println("?Y");
          }
          break;
        case '(': {
            while (Serial.available() < 1) {                 //  Wait for 1 byte to be available.
              delayMicroseconds(200);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Report
              Serial1.println("?R");
            }
            else if (instruction == '2') {                   // Cam2, Report
              Serial3.println("?R");
            }
            else if (instruction == '3') {                   // Cam3, Report
              Serial4.println("?R");
            }
          }
          break;
        case ')': {
            while (Serial.available() < 1) {                 //  Wait for 1 byte to be available.
              delayMicroseconds(200);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Pos Report
              Serial1.println("?r");
            }
            else if (instruction == '2') {                   // Cam2, Pos Report
              Serial3.println("?r");
            }
            else if (instruction == '3') {                   // Cam3, Pos Report
              Serial4.println("?r");
            }
          }
          break;
        case '-': {
            while (Serial.available() < 1) {                 //  Wait for 1 byte to be available.
              delayMicroseconds(200);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Keyframe Report
              Serial1.println("?k");
            }
            else if (instruction == '2') {                   // Cam2, Keyframe Report
              Serial3.println("?k");
            }
            else if (instruction == '3') {                   // Cam3, Keyframe Report
              Serial4.println("?k");
            }
          }
          break;
        case '+': {
            while (Serial.available() < 2) {                 //  Wait for 1 byte to be available.
              delayMicroseconds(1);
            }
            instruction = Serial.read();
            if (instruction == '1') {                        // Cam1, Keyframe Report
              instruction = Serial.read();
              if (instruction == '1') {
                Serial1.print("?s");
                Serial1.println(speed1);
                //delay(100);
                //Serial1.print("?S");
                //Serial1.println(speed1);
              }
              else if (instruction == '2') {
                Serial1.print("?s");
                Serial1.println(speed2);
                //delay(100);
                //Serial1.print("?S");
                //Serial1.println(speed2);
              }
              else if (instruction == '3') {
                Serial1.print("?s");
                Serial1.println(speed3);
                //delay(100);
                //Serial1.print("?S");
                //Serial1.println(speed3);
              }
              else if (instruction == '4') {
                Serial1.print("?s");
                Serial1.println(speed4);
                //delay(100);
                //Serial1.print("?S");
                //Serial1.println(speed4);
              }
            }
            else if (instruction == '2') {
              instruction = Serial.read();
              if (instruction == '1') {
                Serial3.print("?s");
                Serial3.println(speed1);
                //delay(100);
                //Serial3.print("?S");
                //Serial3.println(speed1);
              }
              else if (instruction == '2') {
                Serial3.print("?s");
                Serial3.println(speed2);
                //delay(100);
                //Serial3.print("?S");
                //Serial3.println(speed2);
              }
              else if (instruction == '3') {
                Serial3.print("?s");
                Serial3.println(speed3);
                //delay(100);
                //Serial3.print("?S");
                //Serial3.println(speed3);
              }
              else if (instruction == '4') {
                Serial3.print("?s");
                Serial3.println(speed4);
                //delay(100);
                //Serial3.print("?S");
                //Serial3.println(speed4);
              }
            }
            else if (instruction == '3') {
              instruction = Serial.read();
              if (instruction == '1') {
                Serial4.print("?s");
                Serial4.println(speed1);
                //delay(100);
                //Serial4.print("?S");
                //Serial4.println(speed1);
              }
              else if (instruction == '2') {
                Serial4.print("?s");
                Serial4.println(speed2);
                //delay(100);
                //Serial4.print("?S");
                //Serial4.println(speed2);
              }
              else if (instruction == '3') {
                Serial4.print("?s");
                Serial4.println(speed3);
                //delay(100);
                //Serial4.print("?S");
                //Serial4.println(speed3);
              }
              else if (instruction == '4') {
                Serial4.print("?s");
                Serial4.println(speed4);
                //delay(100);
                //Serial4.print("?S");
                //Serial4.println(speed4);
              }
            }
          }
          break;
        case '!': {
            Serial.println("~100");
            Serial.println("~200");
            Serial.println("~300");

            Serial1.println("#0");
            //Serial3.println("#0");
            //Serial4.println("#0");

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

            doLEDrefresh = true;
          }
          break;
      }
    }
    else if (instruction == 4) {
      while (Serial.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      short ZShortPC = (Serial.read() << 8) + Serial.read();
      short XShortPC = (Serial.read() << 8) + Serial.read();
      short YShortPC = (Serial.read() << 8) + Serial.read();
      whichSerialCam = Serial.read();

      shortValsPC[0] = ZShortPC;
      shortValsPC[1] = XShortPC;
      shortValsPC[2] = YShortPC;

      sendSliderPanTiltStepSpeed(4, shortValsPC, whichSerialCam);
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
          Serial3.println(inData4);
          inData4 = "";
        }
      }
    }
    else if (instruction == '@') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData4 += received;
        if (received == '\n') {
          Serial4.println(inData4);
          inData4 = "";
        }
      }
    }
  }
}
