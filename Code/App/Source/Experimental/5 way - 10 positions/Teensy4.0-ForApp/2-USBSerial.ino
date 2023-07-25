void USBSerialData() {
  if (Serial.available()) {  // If anything comes in Serial (USB),
    char instruction = Serial.read();
    if (instruction == '&') {
      while (Serial.available() < 1) {  //  Wait for 1 byte to be available.
        delayMicroseconds(1);
      }
      instruction = Serial.read();
      if (instruction == '1' || instruction == '2' || instruction == '3' || instruction == '4' || instruction == '5') {
        char camNumInst = instruction;
        while (Serial.available() < 1) {  //  Wait for 1 byte to be available.
          delayMicroseconds(1);
        }
        instruction = Serial.read();
        switch (instruction) {
          case 'Z':  // Save pos 1
            {
              if (camNumInst == '1') {
                Serial1.println("?M1");
              } else if (camNumInst == '2') {
                Serial3.println("?M1");
              } else if (camNumInst == '3') {
                Serial2.println("?M1");
              } else if (camNumInst == '4') {
                Serial4.println("?M1");
              } else if (camNumInst == '5') {
                Serial5.println("?M1");
              }
            }
            break;
          case 'X':  // Save pos 2
            {
              if (camNumInst == '1') {
                Serial1.println("?M2");
              } else if (camNumInst == '2') {
                Serial3.println("?M2");
              } else if (camNumInst == '3') {
                Serial2.println("?M2");
              } else if (camNumInst == '4') {
                Serial4.println("?M2");
              } else if (camNumInst == '5') {
                Serial5.println("?M2");
              }
            }
            break;
          case 'C':  // Save pos 3
            {
              if (camNumInst == '1') {
                Serial1.println("?M3");
              } else if (camNumInst == '2') {
                Serial3.println("?M3");
              } else if (camNumInst == '3') {
                Serial2.println("?M3");
              } else if (camNumInst == '4') {
                Serial4.println("?M3");
              } else if (camNumInst == '5') {
                Serial5.println("?M3");
              }
            }
            break;
          case 'V':  // Save pos 4
            {
              if (camNumInst == '1') {
                Serial1.println("?M4");
              } else if (camNumInst == '2') {
                Serial3.println("?M4");
              } else if (camNumInst == '3') {
                Serial2.println("?M4");
              } else if (camNumInst == '4') {
                Serial4.println("?M4");
              } else if (camNumInst == '5') {
                Serial5.println("?M4");
              }
            }
            break;
          case 'B':  // Save pos 5
            {
              if (camNumInst == '1') {
                Serial1.println("?M5");
              } else if (camNumInst == '2') {
                Serial3.println("?M5");
              } else if (camNumInst == '3') {
                Serial2.println("?M5");
              } else if (camNumInst == '4') {
                Serial4.println("?M5");
              } else if (camNumInst == '5') {
                Serial5.println("?M5");
              }
            }
            break;
          case 'N':  // Save pos 6
            {
              if (camNumInst == '1') {
                Serial1.println("?M6");
              } else if (camNumInst == '2') {
                Serial3.println("?M6");
              } else if (camNumInst == '3') {
                Serial2.println("?M6");
              } else if (camNumInst == '4') {
                Serial4.println("?M6");
              } else if (camNumInst == '5') {
                Serial5.println("?M6");
              }
            }
            break;
          case 'M':  // Save pos 7
            {
              if (camNumInst == '1') {
                Serial1.println("?M7");
              } else if (camNumInst == '2') {
                Serial3.println("?M7");
              } else if (camNumInst == '3') {
                Serial2.println("?M7");
              } else if (camNumInst == '4') {
                Serial4.println("?M7");
              } else if (camNumInst == '5') {
                Serial5.println("?M7");
              }
            }
            break;
          case '<':  // Save pos 8
            {
              if (camNumInst == '1') {
                Serial1.println("?M8");
              } else if (camNumInst == '2') {
                Serial3.println("?M8");
              } else if (camNumInst == '3') {
                Serial2.println("?M8");
              } else if (camNumInst == '4') {
                Serial4.println("?M8");
              } else if (camNumInst == '5') {
                Serial5.println("?M8");
              }
            }
            break;
          case '>':  // Save pos 9
            {
              if (camNumInst == '1') {
                Serial1.println("?M9");
              } else if (camNumInst == '2') {
                Serial3.println("?M9");
              } else if (camNumInst == '3') {
                Serial2.println("?M9");
              } else if (camNumInst == '4') {
                Serial4.println("?M9");
              } else if (camNumInst == '5') {
                Serial5.println("?M9");
              }
            }
            break;
          case '?':  // Save pos 10
            {
              if (camNumInst == '1') {
                Serial1.println("?M10");
              } else if (camNumInst == '2') {
                Serial3.println("?M10");
              } else if (camNumInst == '3') {
                Serial2.println("?M10");
              } else if (camNumInst == '4') {
                Serial4.println("?M10");
              } else if (camNumInst == '5') {
                Serial5.println("?M10");
              }
            }
            break;
          case 'z':  // Move to pos 1
            {
              if (camNumInst == '1') {
                Serial1.println("?m1");
              } else if (camNumInst == '2') {
                Serial3.println("?m1");
              } else if (camNumInst == '3') {
                Serial2.println("?m1");
              } else if (camNumInst == '4') {
                Serial4.println("?m1");
              } else if (camNumInst == '5') {
                Serial5.println("?m1");
              }
            }
            break;
          case 'x':  // Move to pos 2
            {
              if (camNumInst == '1') {
                Serial1.println("?m2");
              } else if (camNumInst == '2') {
                Serial3.println("?m2");
              } else if (camNumInst == '3') {
                Serial2.println("?m2");
              } else if (camNumInst == '4') {
                Serial4.println("?m2");
              } else if (camNumInst == '5') {
                Serial5.println("?m2");
              }
            }
            break;
          case 'c':  // Move to pos 3
            {
              if (camNumInst == '1') {
                Serial1.println("?m3");
              } else if (camNumInst == '2') {
                Serial3.println("?m3");
              } else if (camNumInst == '3') {
                Serial2.println("?m3");
              } else if (camNumInst == '4') {
                Serial4.println("?m3");
              } else if (camNumInst == '5') {
                Serial5.println("?m3");
              }
            }
            break;
          case 'v':  // Move to pos 4
            {
              if (camNumInst == '1') {
                Serial1.println("?m4");
              } else if (camNumInst == '2') {
                Serial3.println("?m4");
              } else if (camNumInst == '3') {
                Serial2.println("?m4");
              } else if (camNumInst == '4') {
                Serial4.println("?m4");
              } else if (camNumInst == '5') {
                Serial5.println("?m4");
              }
            }
            break;
          case 'b':  // Move to pos 5
            {
              if (camNumInst == '1') {
                Serial1.println("?m5");
              } else if (camNumInst == '2') {
                Serial3.println("?m5");
              } else if (camNumInst == '3') {
                Serial2.println("?m5");
              } else if (camNumInst == '4') {
                Serial4.println("?m5");
              } else if (camNumInst == '5') {
                Serial5.println("?m5");
              }
            }
            break;
          case 'n':  // Move to pos 6
            {
              if (camNumInst == '1') {
                Serial1.println("?m6");
              } else if (camNumInst == '2') {
                Serial3.println("?m6");
              } else if (camNumInst == '3') {
                Serial2.println("?m6");
              } else if (camNumInst == '4') {
                Serial4.println("?m6");
              } else if (camNumInst == '5') {
                Serial5.println("?m6");
              }
            }
            break;
          case 'm':  // Move to pos 7
            {
              if (camNumInst == '1') {
                Serial1.println("?m7");
              } else if (camNumInst == '2') {
                Serial3.println("?m7");
              } else if (camNumInst == '3') {
                Serial2.println("?m7");
              } else if (camNumInst == '4') {
                Serial4.println("?m7");
              } else if (camNumInst == '5') {
                Serial5.println("?m7");
              }
            }
            break;
          case ',':  // Move to pos 8
            {
              if (camNumInst == '1') {
                Serial1.println("?m8");
              } else if (camNumInst == '2') {
                Serial3.println("?m8");
              } else if (camNumInst == '3') {
                Serial2.println("?m8");
              } else if (camNumInst == '4') {
                Serial4.println("?m8");
              } else if (camNumInst == '5') {
                Serial5.println("?m8");
              }
            }
            break;
          case '.':  // Move to pos 9
            {
              if (camNumInst == '1') {
                Serial1.println("?m9");
              } else if (camNumInst == '2') {
                Serial3.println("?m9");
              } else if (camNumInst == '3') {
                Serial2.println("?m9");
              } else if (camNumInst == '4') {
                Serial4.println("?m9");
              } else if (camNumInst == '5') {
                Serial5.println("?m9");
              }
            }
            break;
          case '/':  // Move to pos 10
            {
              if (camNumInst == '1') {
                Serial1.println("?m10");
              } else if (camNumInst == '2') {
                Serial3.println("?m10");
              } else if (camNumInst == '3') {
                Serial2.println("?m10");
              } else if (camNumInst == '4') {
                Serial4.println("?m10");
              } else if (camNumInst == '5') {
                Serial5.println("?m10");
              }
            }
            break;
          case 'w':  // Decrease speed
            {
              if (camNumInst == '1') {
                Serial1.println("?b");
              } else if (camNumInst == '2') {
                Serial3.println("?b");
              } else if (camNumInst == '3') {
                Serial2.println("?b");
              } else if (camNumInst == '4') {
                Serial4.println("?b");
              } else if (camNumInst == '5') {
                Serial5.println("?b");
              }
            }
            break;
          case 'W':  // Increase speed
            {
              if (camNumInst == '1') {
                Serial1.println("?B");
              } else if (camNumInst == '2') {
                Serial3.println("?B");
              } else if (camNumInst == '3') {
                Serial2.println("?B");
              } else if (camNumInst == '4') {
                Serial4.println("?B");
              } else if (camNumInst == '5') {
                Serial5.println("?B");
              }
            }
            break;
          case 'a':  // Zoom out
            {
              if (camNumInst == '1') {
                Serial1.println("?z1");
              } else if (camNumInst == '2') {
                Serial3.println("?z1");
              } else if (camNumInst == '3') {
                Serial2.println("?z1");
              } else if (camNumInst == '4') {
                Serial4.println("?z1");
              } else if (camNumInst == '5') {
                Serial5.println("?z1");
              }
            }
            break;
          case 'A':  // Zoom in
            {
              if (camNumInst == '1') {
                Serial1.println("?Z1");
              } else if (camNumInst == '2') {
                Serial3.println("?Z1");
              } else if (camNumInst == '3') {
                Serial2.println("?Z1");
              } else if (camNumInst == '4') {
                Serial4.println("?Z1");
              } else if (camNumInst == '5') {
                Serial5.println("?Z1");
              }
            }
            break;
          case 'q':  // Zoom STOP
            {
              if (camNumInst == '1') {
                Serial1.println("?N");
              } else if (camNumInst == '2') {
                Serial3.println("?N");
              } else if (camNumInst == '3') {
                Serial2.println("?N");
              } else if (camNumInst == '4') {
                Serial4.println("?N");
              } else if (camNumInst == '5') {
                Serial5.println("?N");
              }
            }
            break;
          case 'd':  // Toggle recording
            {
              if (camNumInst == '1') {
                Serial1.println("?u");
              } else if (camNumInst == '2') {
                Serial3.println("?u");
              } else if (camNumInst == '3') {
                Serial2.println("?u");
              } else if (camNumInst == '4') {
                Serial4.println("?u");
              } else if (camNumInst == '5') {
                Serial5.println("?u");
              }
            }
            break;
          case 'D':
            {  // Cam 1, Clear Positions
              if (camNumInst == '1') {
                Serial1.println("?Y");
              } else if (camNumInst == '2') {
                Serial3.println("?Y");
              } else if (camNumInst == '3') {
                Serial2.println("?Y");
              } else if (camNumInst == '4') {
                Serial4.println("?Y");
              } else if (camNumInst == '5') {
                Serial5.println("?Y");
              }
            }
            break;
          case 'r':
            {  // Report
              if (camNumInst == '1') {
                Serial1.println("?r");
              } else if (camNumInst == '2') {
                Serial3.println("?r");
              } else if (camNumInst == '3') {
                Serial2.println("?r");
              } else if (camNumInst == '4') {
                Serial4.println("?r");
              } else if (camNumInst == '5') {
                Serial5.println("?r");
              }
            }
            break;
          case 'R':
            {  // Position Report
              if (camNumInst == '1') {
                Serial1.println("?R");
              } else if (camNumInst == '2') {
                Serial3.println("?R");
              } else if (camNumInst == '3') {
                Serial2.println("?R");
              } else if (camNumInst == '4') {
                Serial4.println("?R");
              } else if (camNumInst == '5') {
                Serial5.println("?R");
              }
            }
            break;
          case 'k':
            {  // Keyframe Report
              if (camNumInst == '1') {
                Serial1.println("?k");
              } else if (camNumInst == '2') {
                Serial3.println("?k");
              } else if (camNumInst == '3') {
                Serial2.println("?k");
              } else if (camNumInst == '4') {
                Serial4.println("?k");
              } else if (camNumInst == '5') {
                Serial5.println("?k");
              }
            }
            break;
          case 's':
            {
              while (Serial.available() < 1) {  //  Wait for 1 byte to be available.
                delayMicroseconds(1);
              }
              instruction = Serial.read();
              if (instruction == '1') {
                if (camNumInst == '1') {
                  Serial1.print("?s");
                  Serial1.println(speed1);
                } else if (camNumInst == '2') {
                  Serial3.print("?s");
                  Serial3.println(speed1);
                } else if (camNumInst == '3') {
                  Serial2.print("?s");
                  Serial2.println(speed1);
                } else if (camNumInst == '4') {
                  Serial4.print("?s");
                  Serial4.println(speed1);
                } else if (camNumInst == '5') {
                  Serial5.print("?s");
                  Serial5.println(speed1);
                }
              } else if (instruction == '2') {
                if (camNumInst == '1') {
                  Serial1.print("?s");
                  Serial1.println(speed2);
                } else if (camNumInst == '2') {
                  Serial3.print("?s");
                  Serial3.println(speed2);
                } else if (camNumInst == '3') {
                  Serial2.print("?s");
                  Serial2.println(speed2);
                } else if (camNumInst == '4') {
                  Serial4.print("?s");
                  Serial4.println(speed2);
                } else if (camNumInst == '5') {
                  Serial5.print("?s");
                  Serial5.println(speed2);
                }
              } else if (instruction == '3') {
                if (camNumInst == '1') {
                  Serial1.print("?s");
                  Serial1.println(speed3);
                } else if (camNumInst == '2') {
                  Serial3.print("?s");
                  Serial3.println(speed3);
                } else if (camNumInst == '3') {
                  Serial2.print("?s");
                  Serial2.println(speed3);
                } else if (camNumInst == '4') {
                  Serial4.print("?s");
                  Serial4.println(speed3);
                } else if (camNumInst == '5') {
                  Serial5.print("?s");
                  Serial5.println(speed3);
                }
              } else if (instruction == '4') {
                if (camNumInst == '1') {
                  Serial1.print("?s");
                  Serial1.println(speed4);
                } else if (camNumInst == '2') {
                  Serial3.print("?s");
                  Serial3.println(speed4);
                } else if (camNumInst == '3') {
                  Serial2.print("?s");
                  Serial2.println(speed4);
                } else if (camNumInst == '4') {
                  Serial4.print("?s");
                  Serial4.println(speed4);
                } else if (camNumInst == '5') {
                  Serial5.print("?s");
                  Serial5.println(speed4);
                }
              }
            }
        }
      } else if (instruction == '!') {
        resetLEDs = true;
      }
    } else if (instruction == 4) {
      delay(1);
      while (Serial.available() < 7) {  //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
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
    } else if (instruction == '?') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData6 += received;
        if (received == '\n') {
          Serial1.println(inData6);
          inData6 = "";
        }
      }
    } else if (instruction == '!') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData6 += received;
        if (received == '\n') {
          Serial3.println(inData6);
          inData6 = "";
        }
      }
    } else if (instruction == '@') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData6 += received;
        if (received == '\n') {
          Serial2.println(inData6);
          inData6 = "";
        }
      }
    } else if (instruction == '&') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData6 += received;
        if (received == '\n') {
          Serial4.println(inData6);
          inData6 = "";
        }
      }
    } else if (instruction == '*') {
      while (Serial.available() > 0) {
        char received = Serial.read();
        inData6 += received;
        if (received == '\n') {
          Serial5.println(inData6);
          inData6 = "";
        }
      }
    }
  }
}