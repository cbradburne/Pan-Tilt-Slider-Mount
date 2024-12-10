#ifndef DEFINITIONS_H
#define DEFINITIONS_H

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

#define BAUD_RATE 38400 //9600 //57600

#define PIN_STEP_PAN 19
#define PIN_DIRECTION_PAN 18
#define PIN_STEP_TILT 17
#define PIN_DIRECTION_TILT 16
#define PIN_STEP_SLIDER 15
#define PIN_DIRECTION_SLIDER 14

#define PIN_SW1 11
#define PIN_SW2 12
#define PIN_SW3 6

#define SLIDER_PULLEY_TEETH 36.0
//#define PAN_GEAR_RATIO 8.4705882352941176470588235294118  //  144/17 teeth      - Original Mount
//#define TILT_GEAR_RATIO 3.047619047619047619047619047619  //  64/21 teeth       - Original Mount

//#define PAN_GEAR_RATIO 4    //  160/40 teeth          - New Mount 1.8 degree steppers
//#define TILT_GEAR_RATIO 4   //  80/20 teeth           - New Mount

//#define PAN_GEAR_RATIO 8    //  160/40 *2 teeth       - New Mount 0.9 degree steppers
//#define TILT_GEAR_RATIO 8   //  80/20 *2 teeth        - New Mount

#define PAN_GEAR_RATIO 15   //  270/36 *2 teeth      - New Mount 0.9 degree steppers Pulley drive
#define TILT_GEAR_RATIO 15  //  120/16 *2 teeth      - New Mount

#define MAX_STRING_LENGTH 10

#define INSTRUCTION_BYTES_SLIDER_PAN_TILT_SPEED 4

#define INSTRUCTION_IS_COMMAND '?'

#define INSTRUCTION_PAN_DEGREES 'p'
#define INSTRUCTION_TILT_DEGREES 't'
#define INSTRUCTION_SLIDER_MILLIMETRES 'x'

#define INSTRUCTION_PAN_DEGREES_REL 'P'
#define INSTRUCTION_TILT_DEGREES_REL 'T'
#define INSTRUCTION_SLIDER_MILLIMETRES_REL 'X'

#define INSTRUCTION_SET_PAN_SPEED 's'
#define INSTRUCTION_SET_TILT_SPEED 'S'
#define INSTRUCTION_SET_SLIDER_SPEED 'a'

#define INSTRUCTION_SET_SLIDE_LIMIT 'y'
#define INSTRUCTION_SET_ZOOM_LIMIT 'w'

#define INSTRUCTION_SET_PANTILT_SPEED1 'B'
#define INSTRUCTION_SET_PANTILT_SPEED2 'b'
#define INSTRUCTION_SET_PANTILT_SPEED3 'C'
#define INSTRUCTION_SET_PANTILT_SPEED4 'c'
#define INSTRUCTION_SET_SLIDER_SPEED1 'D'
#define INSTRUCTION_SET_SLIDER_SPEED2 'd'
#define INSTRUCTION_SET_SLIDER_SPEED3 'E'
#define INSTRUCTION_SET_SLIDER_SPEED4 'e'

#define INSTRUCTION_IS_SETTINGS_REQUESTED 'F'
#define INSTRUCTION_IS_CHANGE_SETTINGS 'f'

#define INSTRUCTION_RESTORE_DEFAULT_SPEEDS 'l'

#define INSTRUCTION_PANTILT_ACCEL 'Q'
#define INSTRUCTION_SLIDER_ACCEL 'q'

#define INSTRUCTION_DEBUG_STATUS 'R'
#define INSTRUCTION_POSITION_STATUS 'r'
#define INSTRUCTION_KEYFRAMES_STATUS 'k'
#define INSTRUCTION_RESET_LEDS 'W'
#define INSTRUCTION_CLEAR_ARRAY 'Y'
#define INSTRUCTION_SAVE_TO_EEPROM 'U'

#define INSTRUCTION_SET_ZERO_POS 'h'
#define INSTRUCTION_FIND_ZERO_POS 'H'

#define INSTRUCTION_IS_CAM_DELAY 'j'

#define INSTRUCTION_IS_RUN_CAM 'J'

#define INSTRUCTION_DIRECT_MOVE 'm'
#define INSTRUCTION_SETPOS 'M'
#define INSTRUCTION_SLIDE_END1 'v'
#define INSTRUCTION_SLIDE_END2 'V'

#define INSTRUCTION_ZOOM_IN 'Z'
#define INSTRUCTION_ZOOM_OUT 'z'
#define INSTRUCTION_STOP_ZOOM 'N'

#define INSTRUCTION_SET_AUTOFOCUS_ON 'O'
#define INSTRUCTION_SET_AUTOFOCUS_OFF 'o'
#define INSTRUCTION_IS_AUTOFOCUS_ON 'I'
#define INSTRUCTION_IS_AUTOFOCUS_OFF 'i'

#define INSTRUCTION_TOGGLE_RECORDING 'u'
#define INSTRUCTION_IS_RECORDING 'G'
#define INSTRUCTION_IS_NOT_RECORDING 'g'

#define EEPROM_ADDRESS_PANTILT_SET_SPEED 54
#define EEPROM_ADDRESS_SLIDER_SET_SPEED 58
#define EEPROM_ADDRESS_ZOOM_LIMIT 62
#define EEPROM_ADDRESS_SLIDE_LIMIT 70
#define EEPROM_ADDRESS_PANTILT_ACCEL 14
#define EEPROM_ADDRESS_SLIDER_ACCEL 18
#define EEPROM_ADDRESS_PANTILT_SPEED1 22
#define EEPROM_ADDRESS_PANTILT_SPEED2 26
#define EEPROM_ADDRESS_PANTILT_SPEED3 30
#define EEPROM_ADDRESS_PANTILT_SPEED4 34
#define EEPROM_ADDRESS_SLIDER_SPEED1 38
#define EEPROM_ADDRESS_SLIDER_SPEED2 42
#define EEPROM_ADDRESS_SLIDER_SPEED3 46
#define EEPROM_ADDRESS_SLIDER_SPEED4 50

#define VERSION_NUMBER "2 June 2024"

float slideLimit = 130000;     // 3 metres
float zoomLimit = 5550;      // 12 - 35mm

bool withSlider = true;
bool DEBUG1 = false;
bool useKeyframeSpeeds = false;
bool upsideDown = false;
bool slideReverse = false;
bool startedAsync = false;

bool panAsync = false;
bool tiltAsync = false;
bool sliderAsync = false;
bool zoomAsync = false;

bool panRunning = false;
bool tiltRunning = false;
bool sliderRunning = false;
bool zoomRunning = false;

bool sliderAtZero = false;
bool sliderAtLimit = false;
bool findingHome = false;

bool zoomedIn = false;
bool zoomedOut = false;

char stringText[MAX_STRING_LENGTH + 1];
char c;

float pan_steps_per_degree = (400.0 * 16 * PAN_GEAR_RATIO) / 360.0;            //  Stepper motor has 400 steps per 360 degrees
float tilt_steps_per_degree = (400.0 * 16 * TILT_GEAR_RATIO) / 360.0;          //  Stepper motor has 400 steps per 360 degrees
float slider_steps_per_millimetre = (200.0 * 16) / (SLIDER_PULLEY_TEETH * 2);  //  Stepper motor has 200 steps per 360 degrees, the timing pully has 36 teeth and the belt has a pitch of 2mm

float pantilt_set_speed = 20;     //  degrees/second.
float slider_set_speed = 60;      //  mm/second.

float pantilt_accel = 200;
float slider_accel = 1000;

float pantilt_speed1 = 1;
float pantilt_speed2 = 5;
float pantilt_speed3 = 10;
float pantilt_speed4 = 20;

float slider_speed1 = 20;
float slider_speed2 = 40;
float slider_speed3 = 80;
float slider_speed4 = 120;

float zoom_set_speed = 8000;
float zoom_accel = 16000;

float pantiltMaxFactor = 1.0;    // Speed factor of joystick moves ( 1 = 100% )
float sliderMaxFactor = 1.0;
float zoomMaxFactor = 1.0;

bool panNeg = false;
bool tiltNeg = false;
bool slideNeg = false;
bool zoomNeg = false;

int SerialCommandValueInt;
float SerialCommandValueFloat;

String atIndex = "";

float speedFactorS = 0.0;
float speedFactorP = 0.0;
float speedFactorT = 0.0;
float speedFactorZ = 0.0;

bool sentMoved = false;

bool motorRunning = false;

unsigned long previousMillis = 0;
const long zoomInterval = 50;
bool zoomIN = false;
bool zoomOUT = false;
float zoom_speed;

bool pos1set = false;
bool pos2set = false;
bool pos3set = false;
bool pos4set = false;
bool pos5set = false;
bool pos6set = false;
bool pos7set = false;
bool pos8set = false;
bool pos9set = false;
bool pos0set = false;

bool atPos1 = false;
bool atPos2 = false;
bool atPos3 = false;
bool atPos4 = false;
bool atPos5 = false;
bool atPos6 = false;
bool atPos7 = false;
bool atPos8 = false;
bool atPos9 = false;
bool atPos0 = false;

bool isManualMove = false;
unsigned long previousMillisMoveCheck = 0;
unsigned long currentMillisMoveCheck = 0;
unsigned long moveCheckInterval = 1000;

int camDlyNo = 0;
unsigned long previousTime;

int whichSetting = 0;

int dlyPos = 0;

int dlyPos1Time = 0;
int dlyPos2Time = 0;
int dlyPos3Time = 0;
int dlyPos4Time = 0;
int dlyPos5Time = 0;

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

struct KeyframeElement {
  long panStepCount = 0;
  long tiltStepCount = 0;
  float panTiltSpeed = 0;
  long sliderStepCount = 0;
  float sliderSpeed = 0;
  int isRecorded = 0;
};

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

void initPanTilt(void);
void SerialFlush(void);
void SerialData(void);
void Serial1Flush(void);
void Serial1Data(void);
void Serial2Flush(void);
void Serial2Data(void);
void Serial3Flush(void);
void Serial3Data(void);
void mainLoop(void);
void panDegrees(float);
void tiltDegrees(float);
void sliderMoveTo(float);
void debugReport(void);
float boundFloat(float, float, float);
float panDegreesToSteps(float);
float tiltDegreesToSteps(float);
long sliderMillimetresToSteps(float);
float panStepsToDegrees(long);
float panStepsToDegrees(float);
float tiltStepsToDegrees(long);
float tiltStepsToDegrees(float);
float sliderStepsToMillimetres(long);
void clearKeyframes(void);
void moveToIndex(int);
void editKeyframe(void);
void printKeyframeElements(void);
void saveEEPROM(void);
void printEEPROM(void);
void getEEPROMVariables(void);
void scaleKeyframeSpeed(float);

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

#endif