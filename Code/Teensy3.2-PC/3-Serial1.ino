void Serial1Data() {
  if (Serial1.available()) {                                   // If anything comes in Serial1 (pins 0 & 1)
    char c = Serial1.read();
    if (c == '#') {
      while (Serial1.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(200);
      }
      char d = Serial1.read();
      if (d == 'Z') {
        Serial.println("~111");
      }
      else if (d == 'X') {
        Serial.println("~121");
      }
      else if (d == 'C') {
        Serial.println("~131");
      }
      else if (d == 'V') {
        Serial.println("~141");
      }
      else if (d == 'B') {
        Serial.println("~151");
      }
      else if (d == 'N') {
        Serial.println("~161");
      }
      else if (d == 'A') {
        Serial.println("~112");
      }
      else if (d == 'S') {
        Serial.println("~122");
      }
      else if (d == 'D') {
        Serial.println("~132");
      }
      else if (d == 'F') {
        Serial.println("~142");
      }
      else if (d == 'G') {
        Serial.println("~152");
      }
      else if (d == 'H') {
        Serial.println("~162");
      }
      else if (d == 'z') {
        Serial.println("~113");
      }
      else if (d == 'x') {
        Serial.println("~123");
      }
      else if (d == 'c') {
        Serial.println("~133");
      }
      else if (d == 'v') {
        Serial.println("~143");
      }
      else if (d == 'b') {
        Serial.println("~153");
      }
      else if (d == 'n') {
        Serial.println("~163");
      }
      else if (d == 'p') {
        Serial.println("~114");
      }
      else if (d == 'P') {
        Serial.println("~124");
      }
      else if (d == 'a') {
        Serial.println("~100");
      }
      else if (d == 's') {
        Serial.println("~?");
      }
      else if (d == '0') {
        Serial.println("~100");
        Serial.println("~200");
        Serial.println("~300");
      }
    }
    else if (c == '^') {
      while (Serial1.available() < 2) {                        //  Wait for 1 byts to be available
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
      String readSerial1 = Serial1.readStringUntil('\n');
    }

    else if (c == 4) {
      //String readSerial1 = Serial1.readStringUntil('\n');
      delay(1);
      while (Serial1.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      char readSerialC1 = Serial1.read();
      readSerialC1 = Serial1.read();
      readSerialC1 = Serial1.read();
      readSerialC1 = Serial1.read();
      readSerialC1 = Serial1.read();
      readSerialC1 = Serial1.read();
    }

    else {
      inData1 = "\nCam1:\n";
      inData1 += c;
      delay(1);
      while (Serial1.available() > 0) {
        inData1 += Serial1.readStringUntil('\n');
        Serial.println(inData1);
        inData1 = "";
        delay(2);
      }
    }
  }
}
