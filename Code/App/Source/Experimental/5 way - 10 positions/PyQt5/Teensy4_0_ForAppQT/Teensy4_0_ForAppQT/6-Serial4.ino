void Serial4Data() {
    if (Serial4.available()) {                                   // If anything comes in Serial4 (pins 0 & 1)
    char g = Serial4.read();
    if (g == '#') {
      while (Serial4.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(200);
      }
      char h = Serial4.read();
      if (h == 'Z') { Serial.println("~411"); }
      else if (h == 'X') { Serial.println("~421"); }
      else if (h == 'C') { Serial.println("~431"); }
      else if (h == 'V') { Serial.println("~441"); }
      else if (h == 'B') { Serial.println("~451"); }
      else if (h == 'N') { Serial.println("~461"); }
      else if (h == 'M') { Serial.println("~471"); }
      else if (h == '<') { Serial.println("~481"); }
      else if (h == '>') { Serial.println("~491"); }
      else if (h == '?') { Serial.println("~401"); }
      else if (h == 'A') { Serial.println("~412"); }
      else if (h == 'S') { Serial.println("~422"); }
      else if (h == 'D') { Serial.println("~432"); }
      else if (h == 'F') { Serial.println("~442"); }
      else if (h == 'G') { Serial.println("~452"); }
      else if (h == 'H') { Serial.println("~462"); }
      else if (h == 'J') { Serial.println("~472"); }
      else if (h == 'K') { Serial.println("~482"); }
      else if (h == 'L') { Serial.println("~492"); }
      else if (h == ':') { Serial.println("~402"); }
      else if (h == 'z') { Serial.println("~413"); }
      else if (h == 'x') { Serial.println("~423"); }
      else if (h == 'c') { Serial.println("~433"); }
      else if (h == 'v') { Serial.println("~443"); }
      else if (h == 'b') { Serial.println("~453"); }
      else if (h == 'n') { Serial.println("~463"); }
      else if (h == 'm') { Serial.println("~473"); }
      else if (h == ',') { Serial.println("~483"); }
      else if (h == '.') { Serial.println("~493"); }
      else if (h == '/') { Serial.println("~403"); }
      else if (h == 'p') { Serial.println("~414"); }
      else if (h == 'P') { Serial.println("~424"); }
      else if (h == 'a') { Serial.println("~400"); }
      else if (h == 's') { Serial.println("~&"); }
      else if (h == '0') {
        Serial.println("~100");
        Serial.println("~200");
        Serial.println("~300");
        Serial.println("~400");
        Serial.println("~500");
      }
    }
    else if (g == '^') {
      while (Serial4.available() < 2) {                        //  Wait for 1 byts to be available
        delayMicroseconds(200);
      }
      g = Serial4.read();
      if (g == '=') {
        s4Speed = Serial4.read();
        s4Speed -= 48;
        Serial.print("=4");
        Serial.println(s4Speed);
      }

      else if (g == '@') {
        cam4PTSpeed = Serial4.read();
        cam4PTSpeed -= 48;
        Serial.print("=@4");
        Serial.println(cam4PTSpeed);
      }
    }
    else if (g == 'W') { ; }
    else if (g == '\n') { ; }
    else if (g == '\r') { ; }
    else if (g == '?') { String readSerial4 = Serial4.readStringUntil('\n'); }

    else if (g == 4) {
      delay(1);
      while (Serial4.available() < 7) {                        //  Wait for 6 bytes to be available. Breaks after ~20ms if bytes are not received.
        delayMicroseconds(200);
      }
      char readSerialC4 = Serial4.read();
      readSerialC4 = Serial4.read();
      readSerialC4 = Serial4.read();
      readSerialC4 = Serial4.read();
      readSerialC4 = Serial4.read();
      readSerialC4 = Serial4.read();
    }

    else {
      inData4 = "\nCam4:\n";
      inData4 += g;
      delay(1);
      while (Serial4.available() > 0) {
        inData4 += Serial4.readStringUntil('\n');
        if (inData4 == "#$\r") {
          break;
        }
        Serial.println(inData4);
        inData4 = "";
        delay(2);
      }
    }
  }
}
