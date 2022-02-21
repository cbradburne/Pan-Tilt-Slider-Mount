/*
  Code adapted from isaac879 by Colin Bradburne.

  Big thanks to Tony McGuire for all his help testing the LANC control.

*/


#define INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED 4
#define INPUT_DEADZONE 40
#define CMDBUFFER_SIZE 32
#define LANCmodePin 23
#define lancPin 15
#define cmdPin 4
#define LED 2

bool DEBUG = false;

bool buttonState;
bool lastButtonState = HIGH;
bool reading = HIGH;
bool isZooming = false;
bool isAutoFocus = false;
bool isPhoto = false;
bool isRecording = false;

unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

int rN = 0;                   // Normal colours (when connected)
int gN = 0;
int bN = 255;

int rS = 0;                   // Colours when 'Set Keyframe' complete
int gS = 255;
int bS = 0;

int rC = 255;                 // Colours when 'Clear All Keyframes' complete
int gC = 255;
int bC = 0;

int rT = 150;                 // Colours when 'Tangent' complete
int gT = 150;
int bT = 0;

int rL = 0;                   // Colours when LANC Handshake complete
int gL = 255;
int bL = 0;

int rR = 255;                 // Colours when LANC Recording
int gR = 0;
int bR = 0;

float in_min = -128;          // PS4 DualShock analogue stick Far Left
float in_max = 128;           // PS4 DualShock analogue stick Far Right
float out_min = -255;
float out_max = 255;

short shortVals[3] = {0, 0, 0};
short LXShort = 0;
short RXShort = 0;
short RYShort = 0;
short oldShortVal0 = 0;
short oldShortVal1 = 0;
short oldShortVal2 = 0;

bool isManualMove = false;
unsigned long previousMillisMoveCheck = 0;
unsigned long currentMillisMoveCheck = 0;
long moveCheckInterval = 300;

bool buttonUP = false;
bool buttonDOWN = false;
bool buttonLEFT = false;
bool buttonRIGHT = false;

bool buttonTRI = false;
bool buttonCIR = false;
bool buttonCRO = false;
bool buttonSQU = false;

bool buttonL1 = false;
bool buttonR1 = false;
bool buttonL2 = false;
bool buttonR2 = false;
bool buttonL3 = false;
bool buttonR3 = false;

bool l1andl3 = false;
bool r1andr3 = false;

bool setUP = false;
bool setLEFT = false;
bool setRIGHT = false;
bool setDOWN = false;

bool buttonSH = false;
bool buttonOP = false;
bool buttonPS = false;
bool buttonTP = false;

bool firstRun = true;

bool isSerialLANC = true;

int LYmapped = 0;
int zoomCase = 8;
int oldLY = 0;
int lancZoom = 0;

long previousMillis = 0;
long currentMillis;
const int LED_Interval = 250;
char instruction = '0';

static char cmdBuffer[CMDBUFFER_SIZE] = "";
char c;

int cmdRepeatCount;
int bitDuration = 104; //Duration of one LANC bit in microseconds.

//LANC commands byte 0 + byte 1
//Start-stop video recording
boolean REC[] = {LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH}; //18 33

//Zoom in from slowest to fastest speed
boolean ZOOM_IN_1[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};    //28 00
boolean ZOOM_IN_2[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW};   //28 02
boolean ZOOM_IN_3[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW};   //28 04
boolean ZOOM_IN_4[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW};  //28 06
boolean ZOOM_IN_5[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW};   //28 08
boolean ZOOM_IN_6[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW};  //28 0A
boolean ZOOM_IN_7[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW};  //28 0C
boolean ZOOM_IN_8[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, LOW}; //28 0E

//Zoom out from slowest to fastest speed
boolean ZOOM_OUT_1[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, LOW};    //28 10
boolean ZOOM_OUT_2[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, HIGH, LOW};   //28 12
boolean ZOOM_OUT_3[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW, LOW};   //28 14
boolean ZOOM_OUT_4[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, HIGH, LOW};  //28 16
boolean ZOOM_OUT_5[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW};   //28 18
boolean ZOOM_OUT_6[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, HIGH, LOW};  //28 1A
boolean ZOOM_OUT_7[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, LOW, LOW};  //28 1C
boolean ZOOM_OUT_8[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH, LOW}; //28 1E

//Focus control. Camera must be switched to manual focus
boolean FOCUS_NEAR[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, HIGH, HIGH, HIGH}; //28 47
boolean FOCUS_FAR[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, HIGH, LOW, HIGH};   //28 45

boolean FOCUS_AUTO[] = {LOW, LOW, HIGH, LOW, HIGH, LOW, LOW, LOW, LOW, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH}; //28 41

//Take Photo
boolean PHOTO[] = {LOW, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW, LOW, LOW, HIGH, LOW, HIGH, LOW, HIGH, HIGH}; //18 2B

//boolean POWER_OFF[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,LOW,HIGH,HIGH,HIGH,HIGH,LOW}; //18 5E
//boolean POWER_ON[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,LOW,HIGH,HIGH,HIGH,LOW,LOW}; //18 5C  Doesn't work because there's no power supply from the LANC port when the camera is off
//boolean POWER_OFF2[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,LOW,HIGH,LOW,HIGH,LOW,HIGH,LOW}; //18 2A Turns the XF300 off and then on again
//boolean POWER_SAVE[] = {LOW,LOW,LOW,HIGH,HIGH,LOW,LOW,LOW,   LOW,HIGH,HIGH,LOW,HIGH,HIGH,LOW,LOW}; //18 6C Didn't work

void setup()
{
  pinMode(LANCmodePin, INPUT_PULLUP);

  pinMode(lancPin, INPUT); //listens to the LANC line
  pinMode(cmdPin, OUTPUT); //writes to the LANC line

  pinMode(LED, OUTPUT);

  digitalWrite(cmdPin, LOW);     //set LANC line to +5V
  delay(5000);                   //Wait for camera to power up completly
  bitDuration = bitDuration - 8; //Writing to the digital port takes about 8 microseconds so only 96 microseconds are left for each bit

  isSerialLANC = digitalRead(LANCmodePin);


  //digitalWrite(LED, HIGH);

  /*
    if (isSerialLANC) {
      digitalWrite(LED, HIGH);
    }
    else {
      digitalWrite(LED, LOW);
    }
  */
  Serial2.begin(38400);
  if ( DEBUG ) {
    Serial.begin(38400);
  }
  else {
    Serial.begin(9600, SERIAL_8E1);
  }
}

void loop() {
  if (Serial2.available()) {
    char c = Serial2.read();
    if (c == '#') {
      while (Serial2.available() < 1) {                         //  Wait for 1 byte to be available.
        delayMicroseconds(1);
      }
      c = Serial2.read();
      if (c == 'W') {
        if (isRecording) {
          Serial2.println("?G");                                // IS RECORDING
        }
        else {
          Serial2.println("?g");                                // IS NOT RECORDING
        }
      }

      if (c == 'O') {                                           // Toggle recording status
        if (isSerialLANC) {
          Serial.print("#7100*");
        }
        else {
          lancCommand(REC);
        }
      }

      if (c == 'o' && isZooming) {                              // Stop Zooming
        if (isSerialLANC) {
          Serial.print("#7590*");
        }
        else {
          lancZoom = 0;
        }
        isZooming = false;
      }

      if (c == 'I' && !isZooming) {
        while (Serial2.available() < 1) {                       //  Wait for 1 byte to be available.
          delayMicroseconds(1);
        }
        c = Serial2.read();
        if (c == '1') {
          if (isSerialLANC) {
            Serial.print("#7410*");
          }
          else {
            lancZoom = 1;
            //lancCommand(ZOOM_IN_1);
          }
        }
        else if (c == '2') {
          if (isSerialLANC) {
            Serial.print("#7420*");
          }
          else {
            lancZoom = 2;
            //lancCommand(ZOOM_IN_2);
          }
        }
        else if (c == '3') {
          if (isSerialLANC) {
            Serial.print("#7430*");
          }
          else {
            lancZoom = 3;
            //lancCommand(ZOOM_IN_3);
          }
        }
        else if (c == '4') {
          if (isSerialLANC) {
            Serial.print("#7440*");
          }
          else {
            lancZoom = 4;
            //lancCommand(ZOOM_IN_4);
          }
        }
        else if (c == '5') {
          if (isSerialLANC) {
            Serial.print("#7450*");
          }
          else {
            lancZoom = 5;
            //lancCommand(ZOOM_IN_5);
          }
        }
        else if (c == '6') {
          if (isSerialLANC) {
            Serial.print("#7460*");
          }
          else {
            lancZoom = 6;
            //lancCommand(ZOOM_IN_6);
          }
        }
        else if (c == '7') {
          if (isSerialLANC) {
            Serial.print("#7470*");
          }
          else {
            lancZoom = 7;
            //lancCommand(ZOOM_IN_7);
          }
        }
        else if (c == '8') {
          if (isSerialLANC) {
            Serial.print("#7480*");
          }
          else {
            lancZoom = 8;
            //lancCommand(ZOOM_IN_8);
          }
        }
        isZooming = true;
      }
      else if (c == 'i' && !isZooming) {
        while (Serial2.available() < 1) {                        //  Wait for 1 byte to be available.
          delayMicroseconds(1);
        }
        c = Serial2.read();
        if (c == '1') {
          if (isSerialLANC) {
            Serial.print("#7510*");
          }
          else {
            lancZoom = 11;
            //lancCommand(ZOOM_OUT_1);
          }
        }
        else if (c == '2') {
          if (isSerialLANC) {
            Serial.print("#7520*");
          }
          else {
            lancZoom = 12;
            //lancCommand(ZOOM_OUT_2);
          }
        }
        else if (c == '3') {
          if (isSerialLANC) {
            lancZoom = 13;
            Serial.print("#7530*");
          }
          else {
            //lancCommand(ZOOM_OUT_3);
          }
        }
        else if (c == '4') {
          if (isSerialLANC) {
            Serial.print("#7540*");
          }
          else {
            lancZoom = 14;
            //lancCommand(ZOOM_OUT_4);
          }
        }
        else if (c == '5') {
          if (isSerialLANC) {
            Serial.print("#7550*");
          }
          else {
            lancZoom = 15;
            //lancCommand(ZOOM_OUT_5);
          }
        }
        else if (c == '6') {
          if (isSerialLANC) {
            Serial.print("#7560*");
          }
          else {
            lancZoom = 16;
            //lancCommand(ZOOM_OUT_6);
          }
        }
        else if (c == '7') {
          if (isSerialLANC) {
            Serial.print("#7570*");
          }
          else {
            lancZoom = 17;
            //lancCommand(ZOOM_OUT_7);
          }
        }
        else if (c == '8') {
          if (isSerialLANC) {
            Serial.print("#7580*");
          }
          else {
            lancZoom = 18;
            //lancCommand(ZOOM_OUT_8);
          }
        }
        isZooming = true;
      }
    }
  }

  if (isSerialLANC) {
    doLANC();
  }

  if (!isSerialLANC && lancZoom > 0) {
    if (lancZoom == 1) {
      lancCommand(ZOOM_IN_1);
    }
    else if (lancZoom == 2) {
      lancCommand(ZOOM_IN_2);
    }
    else if (lancZoom == 3) {
      lancCommand(ZOOM_IN_3);
    }
    else if (lancZoom == 4) {
      lancCommand(ZOOM_IN_4);
    }
    else if (lancZoom == 5) {
      lancCommand(ZOOM_IN_5);
    }
    else if (lancZoom == 6) {
      lancCommand(ZOOM_IN_6);
    }
    else if (lancZoom == 7) {
      lancCommand(ZOOM_IN_7);
    }
    else if (lancZoom == 8) {
      lancCommand(ZOOM_IN_8);
    }
    else if (lancZoom == 11) {
      lancCommand(ZOOM_OUT_1);
    }
    else if (lancZoom == 12) {
      lancCommand(ZOOM_OUT_2);
    }
    else if (lancZoom == 13) {
      lancCommand(ZOOM_OUT_3);
    }
    else if (lancZoom == 14) {
      lancCommand(ZOOM_OUT_4);
    }
    else if (lancZoom == 15) {
      lancCommand(ZOOM_OUT_5);
    }
    else if (lancZoom == 16) {
      lancCommand(ZOOM_OUT_6);
    }
    else if (lancZoom == 17) {
      lancCommand(ZOOM_OUT_7);
    }
    else if (lancZoom == 18) {
      lancCommand(ZOOM_OUT_8);
    }
  }
}

void sendSliderPanTiltStepSpeed(int command, short * arr) {
  byte data[7];                                     // Data array to send

  data[0] = command;
  data[1] = (arr[0] >> 8);                          // Gets the most significant byte
  data[2] = (arr[0] & 0xFF);                        // Gets the second most significant byte
  data[3] = (arr[1] >> 8);
  data[4] = (arr[1] & 0xFF);
  data[5] = (arr[2] >> 8);
  data[6] = (arr[2] & 0xFF);                        // Gets the least significant byte

  if ( DEBUG ) {
    Serial.print(data[0], HEX);
    Serial.print(data[1], HEX);
    Serial.print(data[2], HEX);
    Serial.print(data[3], HEX);
    Serial.print(data[4], HEX);
    Serial.print(data[5], HEX);
    Serial.println(data[6], HEX);
  }
  else {
    Serial2.write(data, sizeof(data));               // Send the command and the 6 bytes of data
    Serial2.print("\n");
  }
}

void sendCharArray(char *array) {
  int i = 0;
  while (array[i] != 0)
    Serial2.write((uint8_t)array[i++]);
}


void doLANC() {
  while (Serial.available())
  {
    c = processCharInput(cmdBuffer, Serial.read());

    if (strcmp("%000*", cmdBuffer) == 0)                                              //  Handshake
    {
      Serial.print("&00080*");
      digitalWrite(LED, HIGH);
      cmdBuffer[0] = 0;
    }
    else if (strcmp("$71000*", cmdBuffer) == 0)                                       //  Recording pt1
    {
      Serial.print("#7110*");
      cmdBuffer[0] = 0;
    }
    else if (strcmp("$71100*", cmdBuffer) == 0) cmdBuffer[0] = 0;                     //  Recording pt2

    else if (strcmp("%7610*", cmdBuffer) == 0)
    {
      Serial.print("&76100*");
      delay(200);
      Serial2.println("?G");
      isRecording = true;
      cmdBuffer[0] = 0;
    }
    else if (strcmp("%7600*", cmdBuffer) == 0)
    {
      Serial.print("&76000*");
      delay(200);
      Serial2.println("?g");
      isRecording = false;
      cmdBuffer[0] = 0;
    }
    else if (strcmp("$73000*", cmdBuffer) == 0) cmdBuffer[0] = 0;               //  Photo Pressed

    else if (strcmp("$73100*", cmdBuffer) == 0)                                 //  Photo Released
    {
      isPhoto = false;
      cmdBuffer[0] = 0;
    }
    else if (strcmp("$72000*", cmdBuffer) == 0) cmdBuffer[0] = 0;               //  Auto Focus ON

    else if (strcmp("$72100*", cmdBuffer) == 0) cmdBuffer[0] = 0;               //  Auto Focus OFF

    else if (strcmp("$74100*", cmdBuffer) == 0) cmdBuffer[0] = 0;               //  Zoom IN

    else if (strcmp("$74200*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74300*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74400*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74500*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74600*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74700*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$74800*", cmdBuffer) == 0) cmdBuffer[0] = 0;

    else if (strcmp("$75100*", cmdBuffer) == 0) cmdBuffer[0] = 0;               //  Zoom OUT

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

char processCharInput(char* cmdBuffer, const char c)
{
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

void lancCommand(boolean lancBit[])
{
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
