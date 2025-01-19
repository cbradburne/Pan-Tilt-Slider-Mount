/*
  Code adapted from isaac879 by Colin Bradburne.
  Big thanks to Tony McGuire for all his help testing the LANC control.
  
  https://espressif.github.io/arduino-esp32/package_esp32_index.json
  
  
  IMPORTANT!!! 
  Boards version 2.0.4 works, later versions don't work.


*/

#define CMDBUFFER_SIZE 32
#define LANCmodePin 23
#define lancPin 15
#define cmdPin 4
#define LED 2

bool DEBUG = false;

int zoomDelay = 100;

bool isAutoFocus = false;
bool isPhoto = false;
bool isRecording = false;
bool toggleFocus = false;

bool firstRun = true;

bool isSerialLANC = true;

int lancZoom = 0;

static char cmdBuffer[CMDBUFFER_SIZE] = "";
char c;

int cmdRepeatCount;
int bitDuration = 104;  //Duration of one LANC bit in microseconds.

//LANC commands byte 0 + byte 1
//Start-stop video recording
boolean REC[] = { LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH };  //18 33

//Zoom in from slowest to fastest speed
boolean ZOOM_IN_1[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW };     //28 00
boolean ZOOM_IN_2[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW };    //28 02
boolean ZOOM_IN_3[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW };    //28 04
boolean ZOOM_IN_4[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW };   //28 06
boolean ZOOM_IN_5[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW };    //28 08
boolean ZOOM_IN_6[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW };   //28 0A
boolean ZOOM_IN_7[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW };   //28 0C
boolean ZOOM_IN_8[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, LOW };  //28 0E

//Zoom out from slowest to fastest speed
boolean ZOOM_OUT_1[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, LOW };     //28 10
boolean ZOOM_OUT_2[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, HIGH, LOW };    //28 12
boolean ZOOM_OUT_3[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW, LOW };    //28 14
boolean ZOOM_OUT_4[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, HIGH, LOW };   //28 16
boolean ZOOM_OUT_5[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW };    //28 18
boolean ZOOM_OUT_6[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, HIGH, LOW };   //28 1A
boolean ZOOM_OUT_7[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, LOW, LOW };   //28 1C
boolean ZOOM_OUT_8[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH, LOW };  //28 1E

//Focus control. Camera must be switched to manual focus
boolean FOCUS_NEAR[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, HIGH, HIGH, HIGH };  //28 47
boolean FOCUS_FAR[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, HIGH, LOW, HIGH };    //28 45

boolean FOCUS_AUTO[] = { LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH };  //28 41

//Take Photo
boolean PHOTO[] = { LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW, HIGH, HIGH };  //18 2B

//boolean POWER_OFF[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,LOW,HIGH,HIGH,HIGH,HIGH,LOW}; //18 5E
//boolean POWER_ON[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,LOW,HIGH,HIGH,HIGH,LOW,LOW}; //18 5C  Doesn't work because there's no power supply from the LANC port when the camera is off
//boolean POWER_OFF2[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,LOW,HIGH,LOW,HIGH,LOW,HIGH,LOW}; //18 2A Turns the XF300 off and then on again
//boolean POWER_SAVE[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,HIGH,LOW,HIGH,HIGH,LOW,LOW}; //18 6C Didn't work

void setup() {
  pinMode(LANCmodePin, INPUT_PULLUP);

  pinMode(lancPin, INPUT);  //listens to the LANC line
  pinMode(cmdPin, OUTPUT);  //writes to the LANC line

  pinMode(LED, OUTPUT);

  digitalWrite(cmdPin, LOW);      //set LANC line to +5V
  delay(5000);                    //Wait for camera to power up completly
  bitDuration = bitDuration - 8;  //Writing to the digital port takes about 8 microseconds so only 96 microseconds are left for each bit

  isSerialLANC = digitalRead(LANCmodePin);

  Serial2.begin(38400);
  if (DEBUG) {
    Serial.begin(38400);
  } else {
    Serial.begin(9600, SERIAL_8E1);
  }
}

void loop() {
  if (Serial2.available()) {
    char c = Serial2.read();
    if (c == '#') {
      while (Serial2.available() < 1) {  //  Wait for 1 byte to be available.
        delayMicroseconds(1);
      }
      c = Serial2.read();
      if (c == 'W') {
        if (isRecording) { Serial2.println("?G"); }       // IS RECORDING
        else {
          Serial2.println("?g");
        }
      }

      if (c == 'O') {                                     // Toggle recording status
        if (isSerialLANC) {
          Serial.print("#7100*");
        } else {
          lancCommand(REC);
        }
      }

      if (c == 'o') {                                     // Stop Zooming
        if (isSerialLANC) {
          Serial.print("#7590*");
        } else {
          lancZoom = 0;
        }
      }

      if (c == 'F') {                                     // Auto-Focus ON
        if (isSerialLANC) {
          if (toggleFocus == false) {
            //toggleFocus = true;
            Serial.print("#7200*");
          }
          else {
            //toggleFocus = false;
            Serial.print("#7210*");
          }
        } else {
          lancZoom = 0;
        }
      }

      //if (c == 'f') {                                     // Auto-Focus OFF
      //  if (isSerialLANC) {
      //    Serial.print("#7210*");
      //  } else {
      //    lancZoom = 0;
      //  }
      //}
      

      if (c == 'I') {
        while (Serial2.available() < 1) {                 //  Wait for 1 byte to be available.
          delayMicroseconds(1);
        }
        c = Serial2.read();
        if (c == '1') {
          if (isSerialLANC) {
            Serial.print("#7410*");
          } else {
            lancZoom = 1;
          }
        } else if (c == '2') {
          if (isSerialLANC) {
            Serial.print("#7420*");
          } else {
            lancZoom = 2;
          }
        } else if (c == '3') {
          if (isSerialLANC) {
            Serial.print("#7430*");
          } else {
            lancZoom = 3;
          }
        } else if (c == '4') {
          if (isSerialLANC) {
            Serial.print("#7440*");
          } else {
            lancZoom = 4;
          }
        } else if (c == '5') {
          if (isSerialLANC) {
            Serial.print("#7450*");
          } else {
            lancZoom = 5;
          }
        } else if (c == '6') {
          if (isSerialLANC) {
            Serial.print("#7460*");
          } else {
            lancZoom = 6;
          }
        } else if (c == '7') {
          if (isSerialLANC) {
            Serial.print("#7470*");
          } else {
            lancZoom = 7;
          }
        } else if (c == '8') {
          if (isSerialLANC) {
            Serial.print("#7480*");
          } else {
            lancZoom = 8;
          }
        }
      } else if (c == 'i') {
        while (Serial2.available() < 1) { delayMicroseconds(1); }  //  Wait for 1 byte to be available.

        c = Serial2.read();
        if (c == '1') {
          if (isSerialLANC) {
            Serial.print("#7510*");
          } else {
            lancZoom = 11;
          }
        } else if (c == '2') {
          if (isSerialLANC) {
            Serial.print("#7520*");
          } else {
            lancZoom = 12;
          }
        } else if (c == '3') {
          if (isSerialLANC) {
            Serial.print("#7530*");
          } else {
            lancZoom = 13;
          }
        } else if (c == '4') {
          if (isSerialLANC) {
            Serial.print("#7540*");
          } else {
            lancZoom = 14;
          }
        } else if (c == '5') {
          if (isSerialLANC) {
            Serial.print("#7550*");
          } else {
            lancZoom = 15;
          }
        } else if (c == '6') {
          if (isSerialLANC) {
            Serial.print("#7560*");
          } else {
            lancZoom = 16;
          }
        } else if (c == '7') {
          if (isSerialLANC) {
            Serial.print("#7570*");
          } else {
            lancZoom = 17;
          }
        } else if (c == '8') {
          if (isSerialLANC) {
            Serial.print("#7580*");
          } else {
            lancZoom = 18;
          }
        }
      }
    }
  }

  if (isSerialLANC) {
    doLANC();
  }

  if (!isSerialLANC && lancZoom > 0) {
    if (lancZoom == 1) {
      lancCommand(ZOOM_IN_1);
    } else if (lancZoom == 2) {
      lancCommand(ZOOM_IN_2);
    } else if (lancZoom == 3) {
      lancCommand(ZOOM_IN_3);
    } else if (lancZoom == 4) {
      lancCommand(ZOOM_IN_4);
    } else if (lancZoom == 5) {
      lancCommand(ZOOM_IN_5);
    } else if (lancZoom == 6) {
      lancCommand(ZOOM_IN_6);
    } else if (lancZoom == 7) {
      lancCommand(ZOOM_IN_7);
    } else if (lancZoom == 8) {
      lancCommand(ZOOM_IN_8);
    } else if (lancZoom == 11) {
      lancCommand(ZOOM_OUT_1);
    } else if (lancZoom == 12) {
      lancCommand(ZOOM_OUT_2);
    } else if (lancZoom == 13) {
      lancCommand(ZOOM_OUT_3);
    } else if (lancZoom == 14) {
      lancCommand(ZOOM_OUT_4);
    } else if (lancZoom == 15) {
      lancCommand(ZOOM_OUT_5);
    } else if (lancZoom == 16) {
      lancCommand(ZOOM_OUT_6);
    } else if (lancZoom == 17) {
      lancCommand(ZOOM_OUT_7);
    } else if (lancZoom == 18) {
      lancCommand(ZOOM_OUT_8);
    }
  }
}

void sendCharArray(char* array) {
  int i = 0;
  while (array[i] != 0)
    Serial2.write((uint8_t)array[i++]);
}


void doLANC() {
  while (Serial.available()) {
    c = processCharInput(cmdBuffer, Serial.read());

    if (strcmp("%000*", cmdBuffer) == 0) {                                            //  Handshake
      Serial.print("&00080*");
      digitalWrite(LED, HIGH);
      cmdBuffer[0] = 0;
    } 
    else if (strcmp("$71000*", cmdBuffer) == 0) {                                     //  Recording pt1
      Serial.print("#7110*");
      cmdBuffer[0] = 0;
    } 
    else if (strcmp("$71100*", cmdBuffer) == 0) cmdBuffer[0] = 0;                     //  Recording pt2

    else if (strcmp("%7610*", cmdBuffer) == 0) {
      Serial.print("&76100*");
      delay(200);
      Serial2.println("?G");
      isRecording = true;
      cmdBuffer[0] = 0;
    } 
    else if (strcmp("%7600*", cmdBuffer) == 0) {
      Serial.print("&76000*");
      delay(200);
      Serial2.println("?g");
      isRecording = false;
      cmdBuffer[0] = 0;
    } 
    else if (strcmp("$73000*", cmdBuffer) == 0) cmdBuffer[0] = 0;         //  Photo Pressed

    else if (strcmp("$73100*", cmdBuffer) == 0)                           //  Photo Released
    {
      isPhoto = false;
      cmdBuffer[0] = 0;
    } else if (strcmp("$72000*", cmdBuffer) == 0) {                       //  Auto Focus ON
      toggleFocus = true;
      Serial2.println("?I");
      cmdBuffer[0] = 0;

    } else if (strcmp("$72100*", cmdBuffer) == 0) {                       //  Auto Focus OFF
      toggleFocus = false;
      Serial2.println("?i");
      cmdBuffer[0] = 0;
      
    } else if (strcmp("$74100*", cmdBuffer) == 0) cmdBuffer[0] = 0;       //  Zoom IN

    else if (strcmp("$74200*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74300*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74400*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74500*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74600*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74700*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74800*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75100*", cmdBuffer) == 0) cmdBuffer[0] = 0;         //  Zoom OUT

    else if (strcmp("$75200*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75300*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75400*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75500*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75600*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75700*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75800*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75900*", cmdBuffer) == 0) cmdBuffer[0] = 0;
  }
}

char processCharInput(char* cmdBuffer, const char c) {
  if (c >= 32 && c <= 126) {
    if (strlen(cmdBuffer) < CMDBUFFER_SIZE) {
      strncat(cmdBuffer, &c, 1);
    } 
    else {
      cmdBuffer[0] = 0;
    }
  } 
  else if ((c == 8 || c == 127) && cmdBuffer[0] != 0) {
    cmdBuffer[strlen(cmdBuffer) - 1] = 0;
  }
  return c;
}

void lancCommand(boolean lancBit[]) {
  cmdRepeatCount = 0;
  while (cmdRepeatCount < 5) {
    while (pulseIn(lancPin, HIGH) < 5000) {
    }
    delayMicroseconds(bitDuration);

    for (int i = 7; i > -1; i--) {
      digitalWrite(cmdPin, lancBit[i]);
      delayMicroseconds(bitDuration);
    }

    digitalWrite(cmdPin, LOW);
    delayMicroseconds(10);

    while (digitalRead(lancPin)) {
    }
    delayMicroseconds(bitDuration);

    for (int i = 15; i > 7; i--) {
      digitalWrite(cmdPin, lancBit[i]);
      delayMicroseconds(bitDuration);
    }

    digitalWrite(cmdPin, LOW);
    cmdRepeatCount++;
  }
}
