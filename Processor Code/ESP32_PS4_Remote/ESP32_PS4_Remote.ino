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

#define INPUT_DEADZONE 30
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

short shortVals[4] = {0, 0, 0, 0};
short LXShort = 0;
short RXShort = 0;
short RYShort = 0;
short LYShort = 0;
short oldShortVal0 = 0;
short oldShortVal1 = 0;
short oldShortVal2 = 0;
short oldShortVal3 = 0;

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

char c;

void setup()
{
  pinMode(LED, OUTPUT);
  delay(5000);
  Serial.begin(38400);
  if ( DEBUG ) {
    Serial.begin(38400);
  }
  PS4connect();
}

void PS4connect() {
  PS4.begin("84:2f:57:24:06:65");
}

void loop() {
  if (!PS4.isConnected()) {
    ;
  }
  
  if (PS4.isConnected()) {
    if (firstRun) {
      firstRun1();
    } else {
      if (Serial.available() > 0) {
        instruction = Serial.read();
        if (instruction == '#') {
          c = Serial.read();
          if ((c='Z') || (c='X') || (c='C') || (c='V') || (c='B') || (c='N') || (c='M') || (c='<') || (c='>') || (c='?')) {
            PS4.setLed(0, 255, 0);
            PS4.sendToController();
          } else if ((c='A') || (c='S') || (c='D') || (c='F') || (c='G') || (c='H') || (c='J') || (c='K') || (c='L') || (c=':')) {
            PS4.setLed(255, 255, 0);
            PS4.sendToController();
          } else if ((c='z') || (c='x') || (c='c') || (c='v') || (c='b') || (c='n') || (c='m') || (c=',') || (c='.') || (c='/')) {
            PS4.setLed(0, 255, 0);
            PS4.sendToController();
          } else if (c='s') {
            PS4.setLed(255, 0, 0);
            PS4.sendToController();
          }
        }
      }

      float RX = (PS4.data.analog.stick.rx);            // Get right analog stick X value
      float RY = (PS4.data.analog.stick.ry);            // Get right analog stick Y value
      float LY = (PS4.data.analog.stick.ly);            // Get Left analog stick Y value

      float L2 = (PS4.data.analog.button.l2);
      float R2 = (PS4.data.analog.button.r2);

      RX = map(RX, in_min, in_max, out_min, out_max);
      RY = map(RY, in_min, in_max, out_min, out_max);
      LY = map(LY, in_min, in_max, out_min, out_max);

      L2 = map(L2, 0, 255, 0, out_min);
      R2 = map(R2, 0, 255, 0, out_max);
      float Z2 = L2 + R2;


      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (RX > INPUT_DEADZONE) {                                   // check if the controller is outside of the axis dead zone
        RXShort = map(RX, INPUT_DEADZONE, out_max, 0, out_max);
      }
      else if (RX < -INPUT_DEADZONE) {
        RXShort = map(RX, -INPUT_DEADZONE, out_min, 0, out_min);
      }
      else {
        RXShort = 0;                                                        // if in DeadZone, send 0, Don't move
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (RY > INPUT_DEADZONE) {
        RYShort = map(RY, INPUT_DEADZONE, out_max, 0, out_max);
      }
      else if (RY < -INPUT_DEADZONE) {
        RYShort = map(RY, -INPUT_DEADZONE, out_min, 0, out_min);
      }
      else {
        RYShort = 0;
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (LY > INPUT_DEADZONE) {
        LYShort = map(LY, INPUT_DEADZONE, out_max, 0, out_max);
      }
      else if (LY < -INPUT_DEADZONE) {
        LYShort = map(LY, -INPUT_DEADZONE, out_min, 0, out_min);
      }
      else {
        LYShort = 0;
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if (Z2 > INPUT_DEADZONE) {
        LXShort = map(Z2, INPUT_DEADZONE, out_max, 0, out_max);
      }
      else if (Z2 < -INPUT_DEADZONE) {
        LXShort = map(Z2, -INPUT_DEADZONE, out_min, 0, out_min);
      }
      else {
        LXShort = 0;
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      shortVals[0] = LXShort;
      shortVals[1] = RXShort;
      shortVals[2] = RYShort;
      shortVals[3] = LYShort;

      if ((shortVals[0] == oldShortVal0 && shortVals[1] == oldShortVal1 && shortVals[2] == oldShortVal2 && shortVals[3] == oldShortVal3) && ((oldShortVal0 + oldShortVal1 + oldShortVal2 + oldShortVal3) != 0)) {
        unsigned long currentMillisMoveCheck = millis();
        if (currentMillisMoveCheck - previousMillisMoveCheck > moveCheckInterval) {
          previousMillisMoveCheck = currentMillisMoveCheck;
          sendSliderPanTiltStepSpeed(4, shortVals);
        }
      }
      else if (shortVals[0] != oldShortVal0 || shortVals[1] != oldShortVal1 || shortVals[2] != oldShortVal2 || shortVals[3] != oldShortVal3) {   // IF input has changed
        sendSliderPanTiltStepSpeed(4, shortVals);                     // Send the combned values

        oldShortVal0 = shortVals[0];      // Store as old values SLIDER
        oldShortVal1 = shortVals[1];      // Store as old values PAN
        oldShortVal2 = shortVals[2];      // Store as old values TILT
        oldShortVal3 = shortVals[3];      // Store as old values ZOOM

        previousMillisMoveCheck = millis();
      }

      /*------------------------------------------------------------------------------------------------------------------------------------------------------*/

      if ( PS4.data.button.up && !buttonUP && !PS4.data.button.square ) {           // Up - Move to Pos 1
        Serial.println("?m1");
        buttonUP = true;
      }
      if ( PS4.data.button.left && !buttonLEFT && !PS4.data.button.square ) {       // Left - Move to Pos 2
        Serial.println("?m2");
        buttonLEFT = true;
      }
      if ( PS4.data.button.right && !buttonRIGHT && !PS4.data.button.square ) {     // Right - Move to Pos 3
        Serial.println("?m3");
        buttonRIGHT = true;
      }
      if ( PS4.data.button.down && !buttonDOWN && !PS4.data.button.square ) {       // Down - Move to Pos 4
        Serial.println("?m4");
        buttonDOWN = true;
      }

      if ( PS4.data.button.triangle && !buttonTRI) {    // Triangle - Execute moves array
        buttonTRI = true;
      }
      if ( PS4.data.button.circle && !buttonCIR) {      // Circle - Edit current position
        buttonCIR = true;
      }
      if ( PS4.data.button.cross && !buttonCRO) {       // Cross - Save current position as new keyframe
        buttonCRO = true;
      }
      if ( PS4.data.button.square && !buttonSQU) {      // Square -
        buttonSQU = true;
      }


      if ( PS4.data.button.square && PS4.data.button.up && !setUP) {          // Set Pos 1
        Serial.println("?M1");
        setUP = true;
      }
      if ( PS4.data.button.square && PS4.data.button.left && !setLEFT) {      // Set Pos 2
        Serial.println("?M2");
        setLEFT = true;
      }
      if ( PS4.data.button.square && PS4.data.button.right && !setRIGHT) {       // Set Pos 3
        Serial.println("?M3");
        setRIGHT = true;
      }
      if ( PS4.data.button.square && PS4.data.button.down && !setDOWN) {        // Set Pos 4
        Serial.println("?M4");
        setDOWN = true;
      }


      if ( PS4.data.button.l1 && !buttonL1) {                                       // L1 - decrease speed
        Serial.println("?o");
        buttonL1 = true;
      }
      if ( PS4.data.button.r1 && !buttonR1) {                                       // R1 - increase speed
        Serial.println("?O");
        buttonR1 = true;
      }
      if ( PS4.data.button.l1 && PS4.data.button.l3 && !l1andl3) {                  //
        l1andl3 = true;
      }
      if ( PS4.data.button.r1 && PS4.data.button.r3 && !r1andr3) {                  //
        r1andr3 = true;
      }

      if ( PS4.data.button.share && !buttonSH) {                                    // Share - Clear Array
        buttonSH = true;
      }
      if ( PS4.data.button.options && !buttonOP) {                                  // Option - Auto Focus
        buttonOP = true;
      }

      if ( PS4.data.button.ps && !buttonPS) {                                       // PS Button - Photo
        if ( DEBUG ) {
          Serial.println("PS Button");
        }
        buttonPS = true;
      }
      if ( PS4.data.button.touchpad  && !buttonTP) {                                // TouchPad Button - Record
        if ( DEBUG ) {
          Serial.println("Touch Pad Button");
        }
        buttonTP = true;
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
}

void sendSliderPanTiltStepSpeed(int command, short * arr) {
  byte data[9];                                     // Data array to send

  data[0] = command;
  data[1] = (arr[0] >> 8);                          // Gets the most significant byte
  data[2] = (arr[0] & 0xFF);                        // Gets the second most significant byte
  data[3] = (arr[1] >> 8);
  data[4] = (arr[1] & 0xFF);
  data[5] = (arr[2] >> 8);
  data[6] = (arr[2] & 0xFF);
  data[7] = (arr[3] >> 8);
  data[8] = (arr[3] & 0xFF);                        // Gets the least significant byte

  if ( DEBUG ) {
    Serial.print(data[0], HEX);
    Serial.print(data[1], HEX);
    Serial.print(data[2], HEX);
    Serial.print(data[3], HEX);
    Serial.print(data[4], HEX);
    Serial.print(data[5], HEX);
    Serial.print(data[6], HEX);
    Serial.print(data[7], HEX);
    Serial.println(data[8], HEX);
  }
  else {
    Serial.write(data, sizeof(data));               // Send the command and the 9 bytes of data
    Serial.print("\n");
  }
}

void sendCharArray(char *array) {
  int i = 0;
  while (array[i] != 0)
    Serial.write((uint8_t)array[i++]);
}

void firstRun1() {
  digitalWrite(LED, LOW);
  firstRun = false;
  PS4.setLed(255, 0, 0);
  PS4.sendToController();
  delay(500);
  PS4.setLed(0, 0, 0);
  PS4.sendToController();
  delay(500);
  PS4.setLed(255, 0, 0);
  PS4.sendToController();
  delay(500);
  PS4.setLed(0, 0, 0);
  PS4.sendToController();
  delay(500);
  PS4.setLed(rN, gN, bN);
  PS4.sendToController();
  delay(500);
}