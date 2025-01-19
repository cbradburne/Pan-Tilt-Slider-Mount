/*
  Code adapted from isaac879 by Colin Bradburne.
  Big thanks to Tony McGuire for all his help testing the LANC control.
  
  https://espressif.github.io/arduino-esp32/package_esp32_index.json
  
  
  IMPORTANT!!! 
  Boards version 2.0.4 works, later versions don't work.

  
*/

#define CMDBUFFER_SIZE 32
#define LANCmodePin 23
#define LED 2

bool DEBUG = false;
bool isSerialLANC = true;

static char cmdBuffer[CMDBUFFER_SIZE] = "";
char c;

void setup() {
  pinMode(LANCmodePin, INPUT_PULLUP);
  pinMode(LED, OUTPUT);

  delay(5000);  //Wait for camera to power up completly

  isSerialLANC = digitalRead(LANCmodePin);

  Serial2.begin(38400);
  if (DEBUG) {
    Serial.begin(38400);
  } else {
    Serial.begin(9600, SERIAL_8E1);
  }
}

void loop() {
  if (isSerialLANC) {
    if (Serial2.available()) {
      char c = Serial2.read();
      if (c == '#') {
        while (Serial2.available() < 1) { delayMicroseconds(1); }     //  Wait for 1 byte to be available.

        c = Serial2.read();
        if (c == 'o') Serial.print("#7590*");                         //  Send Stop Zooming

        // ZOOM Send
        else if (c == 'I') {
          while (Serial2.available() < 1) { delayMicroseconds(1); }   //  Wait for 1 byte to be available.

          c = Serial2.read();
          if (c == '1') Serial.print("#7410*");                       //  Send Zoom IN
          else if (c == '2') Serial.print("#7420*");
          else if (c == '3') Serial.print("#7430*");
          else if (c == '4') Serial.print("#7440*");
          else if (c == '5') Serial.print("#7450*");
          else if (c == '6') Serial.print("#7460*");
          else if (c == '7') Serial.print("#7470*");
          else if (c == '8') Serial.print("#7480*");

        } else if (c == 'i') {
          while (Serial2.available() < 1) { delayMicroseconds(1); }   //  Wait for 1 byte to be available.

          c = Serial2.read();
          if (c == '1') Serial.print("#7510*");                       //  Send Zoom OUT
          else if (c == '2') Serial.print("#7520*");
          else if (c == '3') Serial.print("#7530*");
          else if (c == '4') Serial.print("#7540*");
          else if (c == '5') Serial.print("#7550*");
          else if (c == '6') Serial.print("#7560*");
          else if (c == '7') Serial.print("#7570*");
          else if (c == '8') Serial.print("#7580*");
        }
      }
    }
    doLANC();
  }
}

void doLANC() {
  while (Serial.available()) {
    c = processCharInput(cmdBuffer, Serial.read());

    if (strcmp("%000*", cmdBuffer) == 0) {                            //  Handshake
      Serial.print("&00080*");
      digitalWrite(LED, HIGH);
      cmdBuffer[0] = 0;
    }

    else if (strcmp("$74100*", cmdBuffer) == 0) cmdBuffer[0] = 0;     //  Received Zoom IN
    else if (strcmp("$74200*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74300*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74400*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74500*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74600*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74700*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$74800*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75100*", cmdBuffer) == 0) cmdBuffer[0] = 0;     //  Received Zoom OUT
    else if (strcmp("$75200*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75300*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75400*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75500*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75600*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75700*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75800*", cmdBuffer) == 0) cmdBuffer[0] = 0;
    else if (strcmp("$75900*", cmdBuffer) == 0) cmdBuffer[0] = 0;     //  Received Zoom STOP
  }
}

char processCharInput(char* cmdBuffer, const char c) {
  if (c >= 32 && c <= 126) {
    if (strlen(cmdBuffer) < CMDBUFFER_SIZE) {
      strncat(cmdBuffer, &c, 1);
    } else {
      cmdBuffer[0] = 0;
    }
  } else if ((c == 8 || c == 127) && cmdBuffer[0] != 0) {
    cmdBuffer[strlen(cmdBuffer) - 1] = 0;
  }
  return c;
}
