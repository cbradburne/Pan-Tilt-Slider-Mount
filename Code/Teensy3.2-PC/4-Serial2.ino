void Serial2Data() {
    if (Serial2.available()) {                                   // If anything comes in Serial2 (pins 0 & 1)
    char e = Serial2.read();
    if (e == '#') {
      while (Serial2.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(200);
      }
      char f = Serial2.read();
      if (f == 'Z') {
        Serial.println("~211");
      }
      else if (f == 'X') {
        Serial.println("~221");
      }
      else if (f == 'C') {
        Serial.println("~231");
      }
      else if (f == 'V') {
        Serial.println("~241");
      }
      else if (f == 'B') {
        Serial.println("~251");
      }
      else if (f == 'N') {
        Serial.println("~261");
      }
      else if (f == 'A') {
        Serial.println("~212");
      }
      else if (f == 'S') {
        Serial.println("~222");
      }
      else if (f == 'D') {
        Serial.println("~232");
      }
      else if (f == 'F') {
        Serial.println("~242");
      }
      else if (f == 'G') {
        Serial.println("~252");
      }
      else if (f == 'H') {
        Serial.println("~262");
      }
      else if (f == 'z') {
        Serial.println("~213");
      }
      else if (f == 'x') {
        Serial.println("~223");
      }
      else if (f == 'c') {
        Serial.println("~233");
      }
      else if (f == 'v') {
        Serial.println("~243");
      }
      else if (f == 'b') {
        Serial.println("~253");
      }
      else if (f == 'n') {
        Serial.println("~263");
      }
      else if (f == 'p') {
        Serial.println("~214");
      }
      else if (f == 'P') {
        Serial.println("~224");
      }
      else if (f == 'a') {
        Serial.println("~200");
      }
      else if (f == 's') {
        Serial.println("~!");
      }
      else if (f == '0') {
        Serial.println("~100");
        Serial.println("~200");
        Serial.println("~300");
      }
    }
    else if (e == '^') {
      while (Serial2.available() < 2) {                        //  Wait for 1 byts to be available
        delayMicroseconds(200);
      }
      e = Serial2.read();
      if (e == '=') {
        s2Speed = Serial2.read();
        s2Speed -= 48;
        Serial.print("=2");
        Serial.println(s2Speed);
      }

      else if (e == '@') {
        cam2PTSpeed = Serial2.read();
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
      String readSerial2 = Serial2.readStringUntil('\n');
    }

    else if (e == 4) {
      //String readSerial2 = Serial2.readStringUntil('\n');
      delay(1);
      while (Serial2.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      char readSerialC2 = Serial2.read();
      readSerialC2 = Serial2.read();
      readSerialC2 = Serial2.read();
      readSerialC2 = Serial2.read();
      readSerialC2 = Serial2.read();
      readSerialC2 = Serial2.read();
    }

    else {
      inData2 = "\nCam2:\n";
      inData2 += e;
      delay(1);
      while (Serial2.available() > 0) {
        inData2 += Serial2.readStringUntil('\n');
        Serial.println(inData2);
        inData2 = "";
        delay(2);
      }
    }
  }
}
