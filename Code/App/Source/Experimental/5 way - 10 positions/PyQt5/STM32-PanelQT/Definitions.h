#ifndef DEFINITIONS_H
#define DEFINITIONS_H

#include "Adafruit_GFX.h"
#include "Adafruit_HT1632.h"

//#define SERIAL_TX_BUFFER_SIZE 128
//#define SERIAL_RX_BUFFER_SIZE 128

HardwareSerial Serial1(PA10, PA9);
HardwareSerial Serial3(PB11, PB10);
HardwareSerial Serial4(PC11, PC10);
//HardwareSerial Serial(PA3, PA2);      //  Definition not needed


int speed1 = 20;                         //  Pan & Tilt speed settings
int speed2 = 10;
int speed3 = 5;
int speed4 = 1;

int cam1PTSpeed = 0;
int cam2PTSpeed = 0;
int cam3PTSpeed = 0;

int oldcam1PTSpeed = 2;
int oldcam2PTSpeed = 2;
int oldcam3PTSpeed = 2;


//  -- Screen
#define HT_DATA PE4
#define HT_WR PE5
#define HT_CS PE0
#define HT_CS2 PE2
#define HT_CS3 PE1
#define HT_CS4 PE3
#define HT1632C_CMD     B00000100
#define HT1632_SYS_EN 0x01
#define HT1632_LED_ON 0x03
#define HT1632_BLINK_OFF 0x08
#define HT1632_SLAVE_MODE 0x10    //  Set slave mode and clock source from external clock
#define HT1632_MASTER_MODE 0x14   //  Set master mode and clock source from on-chip RC oscillator
#define HT1632_INT_RC 0x18
#define HT1632_EXT_CLK 0x1C
#define HT1632_COMMON_8NMOS 0x20
#define HT1632_PWM_CONTROL 0xAF
Adafruit_HT1632LEDMatrix matrix = Adafruit_HT1632LEDMatrix(HT_DATA, HT_WR, HT_CS, HT_CS3, HT_CS2, HT_CS4);
int displayUpdate = 0;


//  -- Joystick
#define joyPinX PC3
#define joyPinY PC2
#define joyPinZ PC1
#define joyPinB PC0
float joyX;
float joyY;
bool joyB = false;
const int XdeadRangeLow  = 512 - 40;
const int XdeadRangeHigh = 512 + 40;
const int YdeadRangeLow  = 505 - 40;
const int YdeadRangeHigh = 505 + 40;
int X_min = 394;
int X_max = 638;
int Y_min = 375;
int Y_max = 635;
int Z_min = 260;
int Z_max = 785;
int out_min = -254;
int out_max = 254;
short shortVals[3] = {0, 0, 0};
short XShort = 0;
short YShort = 0;
short ZShort = 0;
short oldShortVal0 = 0;
short oldShortVal1 = 0;
short oldShortVal2 = 0;


short shortValsPC[3] = {0, 0, 0};
short XShortPC = 0;
short YShortPC = 0;
short ZShortPC = 0;

bool isManualMove = false;
unsigned long previousMillisMoveCheck = 0;
unsigned long currentMillisMoveCheck = 0;
long moveCheckInterval = 300;

int xDisplay = 0;
int yDisplay = 0;
int oldxDisplay = 0;
int oldyDisplay = 0;
int s1Speed = 0;
int olds1Speed = 3;
int s2Speed = 0;
int olds2Speed = 3;
int s3Speed = 0;
int olds3Speed = 3;

int displayCommand = 000;
int oldDisplayCommand = 1;
bool displayUpadte = false;

String inData1;
String inData2;
String inData3;
String inData4;

unsigned long previousMillisTick = 0;
long tickInterval = 500;
bool runTick1 = false;
bool runTick2 = false;
bool runTick3 = false;
bool oldRunTick1 = false;
bool oldRunTick2 = false;
bool oldRunTick3 = false;

unsigned long previousMillisDisplay = 0;
unsigned long currentMillisDisplay = 0;
long displayInterval = 2000;
bool startDisplayRefresh = true;

bool setClearKey = false;
unsigned long previousMillisClear = 0;
unsigned long currentMillisClear = 0;
long clearInterval = 2000;
bool setClear = false;
bool startClear = true;

unsigned long previousMillisLEDs = 0;
unsigned long currentMillisLEDs = 0;
long LEDsInterval = 2000;
bool resetLEDs = false;
bool startLEDs = true;

bool doLEDrefresh = false;
bool doLEDrefresh2 = false;
bool doLEDrefresh3 = false;
bool doLEDrefresh4 = false;
unsigned long previousMillisLED = 0;
unsigned long currentMillisLED = 0;
long LEDInterval = 500;

int zoom_speed = 0;
int oldZoom_speed = 1;
bool zoomIN = false;
bool zoomOUT = false;

bool isRecording = false;
bool oldIsRecording = false;


//  -- Shuttle Ring
#define ringPinDir PE15
#define ringPinMid PE14
#define ringPinDiv PE13
#define ringPinHlf PE12
bool ringDir = true;
bool ringMid = true;
bool ringDiv = true;
bool ringHlf = true;
int ringLast = 0;
int oldRingLast = 0;


//  -- Jog Wheel
#define encoder0PinA PE10
#define encoder0PinB PE11
int val;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;


//  -- Mode LEDs
#define LEDCP PC13  //  LED clock pulse
#define LEDaG PA4   //  LED 1 Green
#define LEDbG PA6   //  LED 2 Green
#define LEDcG PB5   //  LED 3 Green
#define LEDdG PB9   //  LED 4 Green
#define LEDaR PA5   //  LED 1 Red
#define LEDbR PA8   //  LED 2 Red
#define LEDcR PB8   //  LED 3 Red
#define LEDdR PC12  //  LED 4 Red
#define intLED PA7  //  Internal LED DA1
#define buzzer PE8  //  Internal Buzzer


//  -- Keyboard
#define colA PD0
#define colB PD1
#define colC PD2
#define colD PD3
#define colE PD4
#define colF PD5
#define colG PD6
#define colH PD7
#define colI PD8
#define rowA PD12
#define rowB PD11
#define rowC PD10
#define rowD PD9
#define rowE PD13
#define rowF PD14
unsigned long previousMillisKeyboard = 0;
int keyboardInterval = 5;

int whichCam = 1;
int whichSerialCam = 1;

bool cam1pos1set = false;
bool cam1pos2set = false;
bool cam1pos3set = false;
bool cam1pos4set = false;
bool cam1pos5set = false;
bool cam1pos6set = false;
bool cam1atPos1 = false;
bool cam1atPos2 = false;
bool cam1atPos3 = false;
bool cam1atPos4 = false;
bool cam1atPos5 = false;
bool cam1atPos6 = false;
bool cam1pos1run = false;
bool cam1pos2run = false;
bool cam1pos3run = false;
bool cam1pos4run = false;
bool cam1pos5run = false;
bool cam1pos6run = false;

bool cam2pos1set = false;
bool cam2pos2set = false;
bool cam2pos3set = false;
bool cam2pos4set = false;
bool cam2pos5set = false;
bool cam2pos6set = false;
bool cam2atPos1 = false;
bool cam2atPos2 = false;
bool cam2atPos3 = false;
bool cam2atPos4 = false;
bool cam2atPos5 = false;
bool cam2atPos6 = false;
bool cam2pos1run = false;
bool cam2pos2run = false;
bool cam2pos3run = false;
bool cam2pos4run = false;
bool cam2pos5run = false;
bool cam2pos6run = false;

bool cam3pos1set = false;
bool cam3pos2set = false;
bool cam3pos3set = false;
bool cam3pos4set = false;
bool cam3pos5set = false;
bool cam3pos6set = false;
bool cam3atPos1 = false;
bool cam3atPos2 = false;
bool cam3atPos3 = false;
bool cam3atPos4 = false;
bool cam3atPos5 = false;
bool cam3atPos6 = false;
bool cam3pos1run = false;
bool cam3pos2run = false;
bool cam3pos3run = false;
bool cam3pos4run = false;
bool cam3pos5run = false;
bool cam3pos6run = false;

bool oldcam1pos1set = false;
bool oldcam1pos2set = false;
bool oldcam1pos3set = false;
bool oldcam1pos4set = false;
bool oldcam1pos5set = false;
bool oldcam1pos6set = false;
bool oldcam1atPos1 = false;
bool oldcam1atPos2 = false;
bool oldcam1atPos3 = false;
bool oldcam1atPos4 = false;
bool oldcam1atPos5 = false;
bool oldcam1atPos6 = false;
bool oldcam1pos1run = false;
bool oldcam1pos2run = false;
bool oldcam1pos3run = false;
bool oldcam1pos4run = false;
bool oldcam1pos5run = false;
bool oldcam1pos6run = false;

bool oldcam2pos1set = false;
bool oldcam2pos2set = false;
bool oldcam2pos3set = false;
bool oldcam2pos4set = false;
bool oldcam2pos5set = false;
bool oldcam2pos6set = false;
bool oldcam2atPos1 = false;
bool oldcam2atPos2 = false;
bool oldcam2atPos3 = false;
bool oldcam2atPos4 = false;
bool oldcam2atPos5 = false;
bool oldcam2atPos6 = false;
bool oldcam2pos1run = false;
bool oldcam2pos2run = false;
bool oldcam2pos3run = false;
bool oldcam2pos4run = false;
bool oldcam2pos5run = false;
bool oldcam2pos6run = false;

bool oldcam3pos1set = false;
bool oldcam3pos2set = false;
bool oldcam3pos3set = false;
bool oldcam3pos4set = false;
bool oldcam3pos5set = false;
bool oldcam3pos6set = false;
bool oldcam3atPos1 = false;
bool oldcam3atPos2 = false;
bool oldcam3atPos3 = false;
bool oldcam3atPos4 = false;
bool oldcam3atPos5 = false;
bool oldcam3atPos6 = false;
bool oldcam3pos1run = false;
bool oldcam3pos2run = false;
bool oldcam3pos3run = false;
bool oldcam3pos4run = false;
bool oldcam3pos5run = false;
bool oldcam3pos6run = false;

bool cam1PosUpdate = false;
bool cam2PosUpdate = false;
bool cam3PosUpdate = false;

int keyReadingJB;
int keyReading11;
int keyReading12;
int keyReading14;
int keyReading15;
int keyReading16;
int keyReading17;
int keyReading18;
int keyReading19;
int keyReading21;
int keyReading22;
int keyReading23;
int keyReading24;
int keyReading25;
int keyReading26;
int keyReading27;
int keyReading28;
int keyReading29;
int keyReading31;
int keyReading32;
int keyReading33;
int keyReading34;
int keyReading35;
int keyReading36;
int keyReading37;
int keyReading38;
int keyReading39;
int keyReading41;
int keyReading42;
int keyReading43;
int keyReading44;
int keyReading45;
int keyReading46;
int keyReading47;
int keyReading48;
int keyReading49;
int keyReading51;
int keyReading52;
int keyReading53;
int keyReading54;
int keyReading55;
int keyReading56;
int keyReading61;
int keyReading62;
int keyReading63;
int keyReading64;
int keyReading65;
int keyReading66;
int keyReading67;
int keyReading68;

int buttonStateJB = LOW;
int buttonState11 = HIGH;
int buttonState12 = HIGH;
int buttonState14 = HIGH;
int buttonState15 = HIGH;
int buttonState16 = HIGH;
int buttonState17 = HIGH;
int buttonState18 = HIGH;
int buttonState19 = HIGH;
int buttonState21 = HIGH;
int buttonState22 = HIGH;
int buttonState23 = HIGH;
int buttonState24 = HIGH;
int buttonState25 = HIGH;
int buttonState26 = HIGH;
int buttonState27 = HIGH;
int buttonState28 = HIGH;
int buttonState29 = HIGH;
int buttonState31 = HIGH;
int buttonState32 = HIGH;
int buttonState33 = HIGH;
int buttonState34 = HIGH;
int buttonState35 = HIGH;
int buttonState36 = HIGH;
int buttonState37 = HIGH;
int buttonState38 = HIGH;
int buttonState39 = HIGH;
int buttonState41 = HIGH;
int buttonState42 = HIGH;
int buttonState43 = HIGH;
int buttonState44 = HIGH;
int buttonState45 = HIGH;
int buttonState46 = HIGH;
int buttonState47 = HIGH;
int buttonState48 = HIGH;
int buttonState49 = HIGH;
int buttonState51 = HIGH;
int buttonState52 = HIGH;
int buttonState53 = HIGH;
int buttonState54 = HIGH;
int buttonState55 = HIGH;
int buttonState56 = HIGH;
int buttonState61 = HIGH;
int buttonState62 = HIGH;
int buttonState63 = HIGH;
int buttonState64 = HIGH;
int buttonState65 = HIGH;
int buttonState66 = HIGH;
int buttonState67 = HIGH;
int buttonState68 = HIGH;

int lastButtonStateJB = LOW;
int lastButtonState11 = HIGH;
int lastButtonState12 = HIGH;
int lastButtonState14 = HIGH;
int lastButtonState15 = HIGH;
int lastButtonState16 = HIGH;
int lastButtonState17 = HIGH;
int lastButtonState18 = HIGH;
int lastButtonState19 = HIGH;
int lastButtonState21 = HIGH;
int lastButtonState22 = HIGH;
int lastButtonState23 = HIGH;
int lastButtonState24 = HIGH;
int lastButtonState25 = HIGH;
int lastButtonState26 = HIGH;
int lastButtonState27 = HIGH;
int lastButtonState28 = HIGH;
int lastButtonState29 = HIGH;
int lastButtonState31 = HIGH;
int lastButtonState32 = HIGH;
int lastButtonState33 = HIGH;
int lastButtonState34 = HIGH;
int lastButtonState35 = HIGH;
int lastButtonState36 = HIGH;
int lastButtonState37 = HIGH;
int lastButtonState38 = HIGH;
int lastButtonState39 = HIGH;
int lastButtonState41 = HIGH;
int lastButtonState42 = HIGH;
int lastButtonState43 = HIGH;
int lastButtonState44 = HIGH;
int lastButtonState45 = HIGH;
int lastButtonState46 = HIGH;
int lastButtonState47 = HIGH;
int lastButtonState48 = HIGH;
int lastButtonState49 = HIGH;
int lastButtonState51 = HIGH;
int lastButtonState52 = HIGH;
int lastButtonState53 = HIGH;
int lastButtonState54 = HIGH;
int lastButtonState55 = HIGH;
int lastButtonState56 = HIGH;
int lastButtonState61 = HIGH;
int lastButtonState62 = HIGH;
int lastButtonState63 = HIGH;
int lastButtonState64 = HIGH;
int lastButtonState65 = HIGH;
int lastButtonState66 = HIGH;
int lastButtonState67 = HIGH;
int lastButtonState68 = HIGH;

unsigned long lastDebounceTimeJB = 0;
unsigned long lastDebounceTime11 = 0;
unsigned long lastDebounceTime12 = 0;
unsigned long lastDebounceTime14 = 0;
unsigned long lastDebounceTime15 = 0;
unsigned long lastDebounceTime16 = 0;
unsigned long lastDebounceTime17 = 0;
unsigned long lastDebounceTime18 = 0;
unsigned long lastDebounceTime19 = 0;
unsigned long lastDebounceTime21 = 0;
unsigned long lastDebounceTime22 = 0;
unsigned long lastDebounceTime23 = 0;
unsigned long lastDebounceTime24 = 0;
unsigned long lastDebounceTime25 = 0;
unsigned long lastDebounceTime26 = 0;
unsigned long lastDebounceTime27 = 0;
unsigned long lastDebounceTime28 = 0;
unsigned long lastDebounceTime29 = 0;
unsigned long lastDebounceTime31 = 0;
unsigned long lastDebounceTime32 = 0;
unsigned long lastDebounceTime33 = 0;
unsigned long lastDebounceTime34 = 0;
unsigned long lastDebounceTime35 = 0;
unsigned long lastDebounceTime36 = 0;
unsigned long lastDebounceTime37 = 0;
unsigned long lastDebounceTime38 = 0;
unsigned long lastDebounceTime39 = 0;
unsigned long lastDebounceTime41 = 0;
unsigned long lastDebounceTime42 = 0;
unsigned long lastDebounceTime43 = 0;
unsigned long lastDebounceTime44 = 0;
unsigned long lastDebounceTime45 = 0;
unsigned long lastDebounceTime46 = 0;
unsigned long lastDebounceTime47 = 0;
unsigned long lastDebounceTime48 = 0;
unsigned long lastDebounceTime49 = 0;
unsigned long lastDebounceTime51 = 0;
unsigned long lastDebounceTime52 = 0;
unsigned long lastDebounceTime53 = 0;
unsigned long lastDebounceTime54 = 0;
unsigned long lastDebounceTime55 = 0;
unsigned long lastDebounceTime56 = 0;
unsigned long lastDebounceTime61 = 0;
unsigned long lastDebounceTime62 = 0;
unsigned long lastDebounceTime63 = 0;
unsigned long lastDebounceTime64 = 0;
unsigned long lastDebounceTime65 = 0;
unsigned long lastDebounceTime66 = 0;
unsigned long lastDebounceTime67 = 0;
unsigned long lastDebounceTime68 = 0;

bool set1held = false;
unsigned long debounceDelay = 10;

#endif
