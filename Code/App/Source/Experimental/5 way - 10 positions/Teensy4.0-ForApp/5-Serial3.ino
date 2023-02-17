void Serial2Data() {
    if (Serial2.available()) {                                   // If anything comes in Serial2 (pins 0 & 1)
    char g = Serial2.read();
    if (g == '#') {
      while (Serial2.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(200);
      }
      char h = Serial2.read();
      if (h == 'Z') {
        Serial.println("~311");
      }
      else if (h == 'X') {
        Serial.println("~321");
      }
      else if (h == 'C') {
        Serial.println("~331");
      }
      else if (h == 'V') {
        Serial.println("~341");
      }
      else if (h == 'B') {
        Serial.println("~351");
      }
      else if (h == 'N') {
        Serial.println("~361");
      }
      else if (h == 'M') {
        Serial.println("~371");
      }
      else if (h == '<') {
        Serial.println("~381");
      }
      else if (h == '>') {
        Serial.println("~391");
      }
      else if (h == '?') {
        Serial.println("~301");
      }
      else if (h == 'A') {
        Serial.println("~312");
      }
      else if (h == 'S') {
        Serial.println("~322");
      }
      else if (h == 'D') {
        Serial.println("~332");
      }
      else if (h == 'F') {
        Serial.println("~342");
      }
      else if (h == 'G') {
        Serial.println("~352");
      }
      else if (h == 'H') {
        Serial.println("~362");
      }
      else if (h == 'J') {
        Serial.println("~372");
      }
      else if (h == 'K') {
        Serial.println("~382");
      }
      else if (h == 'L') {
        Serial.println("~392");
      }
      else if (h == ':') {
        Serial.println("~302");
      }
      else if (h == 'z') {
        Serial.println("~313");
      }
      else if (h == 'x') {
        Serial.println("~323");
      }
      else if (h == 'c') {
        Serial.println("~333");
      }
      else if (h == 'v') {
        Serial.println("~343");
      }
      else if (h == 'b') {
        Serial.println("~353");
      }
      else if (h == 'n') {
        Serial.println("~363");
      }
      else if (h == 'm') {
        Serial.println("~373");
      }
      else if (h == ',') {
        Serial.println("~383");
      }
      else if (h == '.') {
        Serial.println("~393");
      }
      else if (h == '/') {
        Serial.println("~303");
      }
      else if (h == 'p') {
        Serial.println("~314");
      }
      else if (h == 'P') {
        Serial.println("~324");
      }
      else if (h == 'a') {
        Serial.println("~300");
      }
      else if (h == 's') {
        Serial.println("~@");
      }
      else if (h == '0') {
        Serial.println("~100");
        Serial.println("~200");
        Serial.println("~300");
        Serial.println("~400");
        Serial.println("~500");
      }
    }
    else if (g == '^') {
      while (Serial2.available() < 2) {                        //  Wait for 1 byts to be available
        delayMicroseconds(200);
      }
      g = Serial2.read();
      if (g == '=') {
        s3Speed = Serial2.read();
        s3Speed -= 48;
        Serial.print("=3");
        Serial.println(s3Speed);
      }

      else if (g == '@') {
        cam3PTSpeed = Serial2.read();
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
      String readSerial2 = Serial2.readStringUntil('\n');
    }

    else if (g == 4) {
      delay(1);
      while (Serial2.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      char readSerialC3 = Serial2.read();
      readSerialC3 = Serial2.read();
      readSerialC3 = Serial2.read();
      readSerialC3 = Serial2.read();
      readSerialC3 = Serial2.read();
      readSerialC3 = Serial2.read();
    }

    else {
      inData3 = "\nCam3:\n";
      inData3 += g;
      delay(1);
      while (Serial2.available() > 0) {
        inData3 += Serial2.readStringUntil('\n');
        if (inData3 == "#$\r") {
          break;
        }
        Serial.println(inData3);
        inData3 = "";
        delay(2);
      }
    }
  }
}
