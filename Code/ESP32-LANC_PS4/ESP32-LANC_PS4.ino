/*
  Code adapted from isaac879 by Colin Bradburne.

  Big thanks to Tony McGuire for all his help testing the LANC control.

  To use a PS4 DualShock controller with the Pan-Tilt-Mount in stand-alone mode, this is what you’ll need.

  ESP32 Dev Kit board - like this one https://www.amazon.co.uk/gp/product/B071JR9WS9
  DualShock 4 controller

  install ESP32 boards into Arduino IDE, follow this guide:
  https://www.hackster.io/abdularbi17/how-to-install-esp32-board-in-arduino-ide-1cd571

  NOTE: Thanks to YouTuber kingjust627, it's been noted that ESP32 DevKitC is incompatible with the code.
  The PS4-ESP library is from https://github.com/AzSaSiN/PS4-esp32 this library works with ESP32 boards library 2.0.4+

  You'll need to get your DualShock4's Bluetooth MAC Address.
  To get the MAC address use the program "SixaxisPairTool", https://dancingpixelstudios.com/sixaxis-controller/sixaxispairtool/.
  I've included the file as thier website seems to be down at the moment.

  I was able to use it on a Mac via a virtual machine running Windows 10 on Parallels Deskptop.
  Make sure you connect your DualShock4 to your computer via USB and not by BlueTooth.

  Wiring:

  -

  Note: When programming either board, you must disconnect the link between TX and RX.
  Also, when programming the ESP32 via Arduino IDE, and the IDE says "Connecting", press and hold the "BOOT" button on the ESP32 until the upload starts.

  When trying to connect your DualShock4 to your ESP32, press the PS button and if it doesn't connect keep trying, it can be a little temperamental :)

  Pan & Tilt                                        -       Right Stick
  Slider                                            -       L2 & R2 (Left and Right)

  Increase Slider Speed                             -       R1
  Decrease Slider Speed                             -       L1

  Set Slider to Max Speed                           -       R1 + R3
  Set Slider to Min Speed                           -       L1 + L3

  Move to Pos 1                                     -       D-Pad UP
  Move to Pos 2                                     -       D-Pad LEFT
  Move to Pos 3                                     -       D-Pad RIGHT
  Move to Pos 4                                     -       D-Pad DOWN

  -                                                 -       Triangle
  -                                                 -       Circle
  -                                                 -       Cross
  Set Pos                                           -       Square (+ D-Pad)

  Clear Array                                       -       Share Button

  LANC Commands:
    Record Toggle                                   -       TouchPad Button
    Auto Focus Toggle                               -       Option Button
    Photo                                           -       PS Button

  Zoom:
    Zoom OUT                                        -       Left Stick Down
    Zoom IN                                         -       Left Stick Up

*/

#include <PS4Controller.h>

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

  PS4connect();
}

void PS4connect() {
  PS4.begin("e8:9e:b4:a9:3b:74");                             // **** insert your DualShock4 MAC address here ****
}

void loop() {
  //while (Serial.available() > 0) {
  //  Serial2.write(Serial.read());
  //}

  if (Serial2.available()) {
    char c = Serial2.read();
    if (c == '#') {
      while (Serial2.available() < 1) {                        //  Wait for 1 byte to be available.
        delayMicroseconds(1);
      }
      c = Serial2.read();
      if (c == 'W') {
        if (isRecording) {
          //sendCharArray((char *)"?G");   // IS RECORDING TO ALL
          Serial2.println("?G");
        }
        else {
          //sendCharArray((char *)"?g");   // IS NOT RECORDING TO ALL
          Serial2.println("?g");
        }
      }

      if (c == 'O') {                                // Toggle recording status
        if (isSerialLANC) {
          Serial.print("#7100*");
        }
        else {
          lancCommand(REC);
        }
      }

      if (c == 'o' && isZooming) {                                // Stop Zooming
        if (isSerialLANC) {
          Serial.print("#7590*");
        }
        else {
          lancZoom = 0;
        }
        isZooming = false;
      }

      if (c == 'I' && !isZooming) {
        while (Serial2.available() < 1) {                        //  Wait for 1 byte to be available.
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

  /*
    if (!PS4.isConnected()) {
      currentMillis = millis();
      if (currentMillis - previousMillis > LED_Interval)
      {
        previousMillis = currentMillis;
        digitalWrite(LED, !(digitalRead(LED)));
      }
    }
  */
  if (isSerialLANC) {
    doLANC();
  }
  
  if (PS4.isConnected()) {
    if (firstRun) {
      firstRun1();
    }
    else {

      float RX = (PS4.data.analog.stick.rx);            // Get right analog stick X value
      float RY = (PS4.data.analog.stick.ry);            // Get right analog stick Y value

      float L2 = (PS4.data.analog.button.l2);
      float R2 = (PS4.data.analog.button.r2);

      //RX = ((RX - in_min) * (out_max - out_min) / ((in_max - in_min) + out_min));       // Note: "map" alternative

      RX = map(RX, in_min, in_max, out_min, out_max);
      RY = map(RY, in_min, in_max, out_min, out_max);

      L2 = map(L2, 0, 255, 0, out_min);
      R2 = map(R2, 0, 255, 0, out_max);
      float Z2 = L2 + R2;

      float magnitudeRX = sqrt(RX * RX);                // Get magnitude of Right stick movement to test for DeadZone
      float magnitudeRY = sqrt(RY * RY);                // Get magnitude of Right stick movement to test for DeadZone

      float magnitudeZ2 = sqrt(Z2 * Z2);

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (magnitudeRX > INPUT_DEADZONE) {                                   // check if the controller is outside of the axis dead zone
        if (RX > 0) {
          RXShort = map(RX, INPUT_DEADZONE, out_max, 0, out_max);
        }
        else if (RX < 0) {
          RXShort = map(RX, -INPUT_DEADZONE, out_min, 0, out_min);
        }
      }
      else {
        RXShort = 0;                                                        // if in DeadZone, send 0, Don't move
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (magnitudeRY > INPUT_DEADZONE) {
        if (RY > 0) {
          RYShort = map(RY, INPUT_DEADZONE, out_max, 0, out_max);
        }
        else if (RY < 0) {
          RYShort = map(RY, -INPUT_DEADZONE, out_min, 0, out_min);
        }
      }
      else {
        RYShort = 0;
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (magnitudeZ2 > INPUT_DEADZONE) {
        if (Z2 > 0) {
          LXShort = map(Z2, INPUT_DEADZONE, out_max, 0, out_max);
        }
        else if (Z2 < 0) {
          LXShort = map(Z2, -INPUT_DEADZONE, out_min, 0, out_min);
        }
      }
      else {
        LXShort = 0;
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      shortVals[0] = LXShort;
      shortVals[1] = RXShort;
      shortVals[2] = RYShort;

      if ((shortVals[0] == oldShortVal0 && shortVals[1] == oldShortVal1 && shortVals[2] == oldShortVal2) && ((oldShortVal0 + oldShortVal1 + oldShortVal2) != 0)) {
        unsigned long currentMillisMoveCheck = millis();
        if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval) {
          previousMillisMoveCheck = currentMillisMoveCheck;
          sendSliderPanTiltStepSpeed(4, shortVals);
        }
      }
      else if (shortVals[0] != oldShortVal0 || shortVals[1] != oldShortVal1 || shortVals[2] != oldShortVal2) {   // IF input has changed
        sendSliderPanTiltStepSpeed(4, shortVals);                     // Send the combned values

        oldShortVal0 = shortVals[0];      // Store as old values SLIDER
        oldShortVal1 = shortVals[1];      // Store as old values PAN
        oldShortVal2 = shortVals[2];      // Store as old values TILT

        delay(20);
        previousMillisMoveCheck = millis();
      }

      /*
            if (shortVals[0] != oldShortVal0 || shortVals[1] != oldShortVal1 || shortVals[2] != oldShortVal2) {   // IF input has changed
              sendSliderPanTiltStepSpeed(INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED, shortVals);                     // Send the combned values

              oldShortVal0 = shortVals[0];      // Store as old values
              oldShortVal1 = shortVals[1];      // Store as old values
              oldShortVal2 = shortVals[2];      // Store as old values

              delay(20);
            }
      */
      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if ( PS4.data.button.up && !buttonUP && !PS4.data.button.square ) {           // Up - Move to Pos 1
        //sendCharArray((char *)"m1");
        Serial2.println("?m1");
        buttonUP = true;
      }
      if ( PS4.data.button.left && !buttonLEFT && !PS4.data.button.square ) {       // Left - Move to Pos 2
        //sendCharArray((char *)"m2");
        Serial2.println("?m2");
        buttonLEFT = true;
      }
      if ( PS4.data.button.right && !buttonRIGHT && !PS4.data.button.square ) {     // Right - Move to Pos 3
        //sendCharArray((char *)"m3");
        Serial2.println("?m3");
        buttonRIGHT = true;
      }
      if ( PS4.data.button.down && !buttonDOWN && !PS4.data.button.square ) {       // Down - Move to Pos 4
        //sendCharArray((char *)"m4");
        Serial2.println("?m4");
        buttonDOWN = true;
      }

      if ( PS4.data.button.triangle && !buttonTRI) {    // Triangle - Execute moves array
        //sendCharArray((char *)";1");
        buttonTRI = true;
      }
      if ( PS4.data.button.circle && !buttonCIR) {      // Circle - Edit current position
        //sendCharArray((char *)"E");
        buttonCIR = true;
      }
      if ( PS4.data.button.cross && !buttonCRO) {       // Cross - Save current position as new keyframe
        //sendCharArray((char *)"#");
        buttonCRO = true;
      }
      if ( PS4.data.button.square && !buttonSQU) {      // Square -
        //sendCharArray((char *)"C");
        buttonSQU = true;
      }


      if ( PS4.data.button.square && PS4.data.button.up && !setUP) {          // Set Pos 1
        //sendCharArray((char *)"?M1");
        Serial2.println("?M1");
        setUP = true;
      }
      if ( PS4.data.button.square && PS4.data.button.left && !setLEFT) {      // Set Pos 2
        //sendCharArray((char *)"?M2");
        Serial2.println("?M2");
        setLEFT = true;
      }
      if ( PS4.data.button.square && PS4.data.button.right && !setRIGHT) {       // Set Pos 3
        //sendCharArray((char *)"?M3");
        Serial2.println("?M3");
        setRIGHT = true;
      }
      if ( PS4.data.button.square && PS4.data.button.down && !setDOWN) {        // Set Pos 4
        //sendCharArray((char *)"?M4");
        Serial2.println("?M4");
        setDOWN = true;
      }


      if ( PS4.data.button.l1 && !buttonL1) {                                       // L1 - decrease slider speed
        //sendCharArray((char *)"?b");
        Serial2.println("?b");
        buttonL1 = true;
      }
      if ( PS4.data.button.r1 && !buttonR1) {                                       // R1 - increase slider speed
        //sendCharArray((char *)"?B");
        Serial2.println("?B");
        buttonR1 = true;
      }
      if ( PS4.data.button.l1 && PS4.data.button.l3 && !l1andl3) {                  // Set Xspeed to minXspeed
        //sendCharArray((char *)"?c");
        Serial2.println("?c");
        l1andl3 = true;
      }
      if ( PS4.data.button.r1 && PS4.data.button.r3 && !r1andr3) {                  // Set Xspeed to maxXspeed
        //sendCharArray((char *)"?C");
        Serial2.println("?C");
        r1andr3 = true;
      }

      if ( PS4.data.button.share && !buttonSH) {                                    // Share - Clear Array
        //sendCharArray((char *)"?Y");
        buttonSH = true;
      }
      if ( PS4.data.button.options && !buttonOP) {                                  // Option - Auto Focus
        if (isAutoFocus) {
          if (isSerialLANC) {
            Serial.print("#7210*");
          }
          else {
            lancCommand(FOCUS_AUTO);
          }
          isAutoFocus = false;
        }
        else if (!isAutoFocus) {
          if (isSerialLANC) {
            Serial.print("#7200*");
          }
          else {
            lancCommand(FOCUS_AUTO);
          }
          isAutoFocus = true;
        }
        buttonOP = true;
      }

      if ( PS4.data.button.ps && !buttonPS) {                                       // PS Button - Photo
        if ( DEBUG ) {
          Serial.println("PS Button");
        }
        if (isSerialLANC) {
          Serial.print("#7300*");
          delay(100);
          Serial.print("#7310*");
        }
        else {
          lancCommand(PHOTO);
        }
        buttonPS = true;
      }
      if ( PS4.data.button.touchpad  && !buttonTP) {                                // TouchPad Button - Record
        if ( DEBUG ) {
          Serial.println("Touch Pad Button");
        }
        if (isSerialLANC) {
          Serial.print("#7100*");
        }
        else {
          lancCommand(REC);
        }
        buttonTP = true;
      }

      int LY = (PS4.data.analog.stick.ly);                                          // Zoom
      float magnitudeLY = sqrt(LY * LY);

      if (magnitudeLY > INPUT_DEADZONE) {
        if (LY > 0) {
          LYmapped = map(LY, INPUT_DEADZONE, 127, 8, 16);
        }
        else if (LY < 0) {
          LYmapped = map(LY, -INPUT_DEADZONE, -128, 8, 0);
        }
      }
      else {
        LYmapped = 8;
      }

      if (LYmapped != zoomCase) {
        if ( DEBUG ) {
          Serial.print("LYmapped - ");
          Serial.println(LYmapped);
          zoomCase = LYmapped;
        }

        if (LYmapped == 0) {
          if (isSerialLANC) {
            Serial.print("#7580*");
          }
          else {
            lancZoom = 18;
          }
          isZooming = true;
          zoomCase = 0;
        }
        else if (LYmapped == 1) {
          if (isSerialLANC) {
            Serial.print("#7570*");
          }
          else {
            lancZoom = 17;
          }
          isZooming = true;
          zoomCase = 1;
        }
        else if (LYmapped == 2) {
          if (isSerialLANC) {
            Serial.print("#7560*");
          }
          else {
            lancZoom = 16;
          }
          isZooming = true;
          zoomCase = 2;
        }
        else if (LYmapped == 3) {
          if (isSerialLANC) {
            Serial.print("#7550*");
          }
          else {
          }
          isZooming = true;
          zoomCase = 3;
        }
        else if (LYmapped == 4) {
          if (isSerialLANC) {
            Serial.print("#7540*");
          }
          else {
            lancZoom = 14;
          }
          isZooming = true;
          zoomCase = 4;
        }
        else if (LYmapped == 5) {
          if (isSerialLANC) {
            Serial.print("#7530*");
          }
          else {
            lancZoom = 13;
          }
          isZooming = true;
          zoomCase = 5;
        }
        else if (LYmapped == 6) {
          if (isSerialLANC) {
            Serial.print("#7520*");
          }
          else {
            lancZoom = 12;
          }
          isZooming = true;
          zoomCase = 6;
        }
        else if (LYmapped == 7) {
          if (isSerialLANC) {
            Serial.print("#7510*");
          }
          else {
            lancZoom = 11;
          }
          isZooming = true;
          zoomCase = 7;
        }
        else if (LYmapped == 8) {                                                   // Stop Zooming
          if (isSerialLANC) {
            Serial.print("#7590*");
          }
          else {
            lancZoom = 0;
          }
          isZooming = false;
          zoomCase = 8;
        }
        else if (LYmapped == 9) {
          if (isSerialLANC) {
            Serial.print("#7410*");
          }
          else {
            lancZoom = 1;
          }
          isZooming = true;
          zoomCase = 9;
        }
        else if (LYmapped == 10) {
          if (isSerialLANC) {
            Serial.print("#7420*");
          }
          else {
            lancZoom = 2;
          }
          isZooming = true;
          zoomCase = 10;
        }
        else if (LYmapped == 11) {
          if (isSerialLANC) {
            Serial.print("#7430*");
          }
          else {
            lancZoom = 3;
          }
          isZooming = true;
          zoomCase = 11;
        }
        else if (LYmapped == 12) {
          if (isSerialLANC) {
            Serial.print("#7440*");
          }
          else {
            lancZoom = 4;
          }
          isZooming = true;
          zoomCase = 12;
        }
        else if (LYmapped == 13) {
          if (isSerialLANC) {
            Serial.print("#7450*");
          }
          else {
            lancZoom = 5;
          }
          isZooming = true;
          zoomCase = 13;
        }
        else if (LYmapped == 14) {
          if (isSerialLANC) {
            Serial.print("#7460*");
          }
          else {
            lancZoom = 6;
          }
          isZooming = true;
          zoomCase = 14;
        }
        else if (LYmapped == 15) {
          if (isSerialLANC) {
            Serial.print("#7470*");
          }
          else {
            lancZoom = 7;
          }
          isZooming = true;
          zoomCase = 15;
        }
        else if (LYmapped == 16) {
          if (isSerialLANC) {
            Serial.print("#7480*");
          }
          else {
            lancZoom = 8;
          }
          isZooming = true;
          zoomCase = 16;
        }
      }
    }

    if ( !PS4.data.button.up && buttonUP)                                           // Button Release flags
      buttonUP = false;
    if ( !PS4.data.button.down && buttonDOWN)
      buttonDOWN = false;
    if ( !PS4.data.button.left && buttonLEFT)
      buttonLEFT = false;
    if ( !PS4.data.button.right && buttonRIGHT)
      buttonRIGHT = false;

    if ( !PS4.data.button.triangle && buttonTRI)
      buttonTRI = false;
    if ( !PS4.data.button.circle && buttonCIR)
      buttonCIR = false;
    if ( !PS4.data.button.cross && buttonCRO)
      buttonCRO = false;
    if ( !PS4.data.button.square && buttonSQU)
      buttonSQU = false;

    if ( !PS4.data.button.l1 && buttonL1)
      buttonL1 = false;
    if ( !PS4.data.button.r1 && buttonR1)
      buttonR1 = false;

    if ( !PS4.data.button.share && buttonSH)
      buttonSH = false;
    if ( !PS4.data.button.options && buttonOP)
      buttonOP = false;

    if ( !PS4.data.button.l1 && !PS4.data.button.l3 && l1andl3)
      l1andl3 = false;
    if ( !PS4.data.button.r1 && !PS4.data.button.r3 && r1andr3)
      r1andr3 = false;

    if ( !PS4.data.button.up && !PS4.data.button.square && setUP)
      setUP = false;
    if ( !PS4.data.button.left && !PS4.data.button.square && setLEFT)
      setLEFT = false;
    if ( !PS4.data.button.right && !PS4.data.button.square && setRIGHT)
      setRIGHT = false;
    if ( !PS4.data.button.down && !PS4.data.button.square && setDOWN)
      setDOWN = false;

    if ( !PS4.data.button.ps && buttonPS)
      buttonPS = false;
    if ( !PS4.data.button.touchpad && buttonTP)
      buttonTP = false;
    if ( !PS4.data.button.l2 && buttonL2)
      buttonL2 = false;
    if ( !PS4.data.button.r2 && buttonR2)
      buttonR2 = false;
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

void firstRun1() {
  digitalWrite(LED, LOW);
  firstRun = false;
  PS4.setLed(255, 0, 0);
  PS4.sendToController();
  delay(100);
  PS4.setLed(0, 0, 0);
  PS4.sendToController();
  delay(100);
  PS4.setLed(255, 0, 0);
  PS4.sendToController();
  delay(100);
  PS4.setLed(0, 0, 0);
  PS4.sendToController();
  delay(100);
  PS4.setLed(rN, gN, bN);
  PS4.sendToController();
  delay(300);
}

void doLANC() {
  while (Serial.available())
  {
    c = processCharInput(cmdBuffer, Serial.read());

    if (strcmp("%000*", cmdBuffer) == 0)                                              //  Handshake
    {
      Serial.print("&00080*");
      PS4.setLed(rL, gL, bL);
      PS4.sendToController();
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
      PS4.setLed(rR, gR, bR);
      PS4.sendToController();
      //sendCharArray((char *)"G");
      delay(200);
      Serial2.println("?G");
      isRecording = true;
      cmdBuffer[0] = 0;
    }
    else if (strcmp("%7600*", cmdBuffer) == 0)
    {
      Serial.print("&76000*");
      PS4.setLed(rL, gL, bL);
      PS4.sendToController();
      //sendCharArray((char *)"g");
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
