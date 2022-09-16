#ifndef DEFINITIONS_H
#define DEFINITIONS_H

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

#define BAUD_RATE 38400 //9600 //57600

#define PIN_STEP_PAN  19
#define PIN_DIRECTION_PAN 18
#define PIN_STEP_TILT 17
#define PIN_DIRECTION_TILT 16
#define PIN_STEP_SLIDER 15
#define PIN_DIRECTION_SLIDER 14

#define PIN_SW1 11
#define PIN_SW2 12

#define SLIDER_PULLEY_TEETH 36.0
//#define PAN_GEAR_RATIO 8.4705882352941176470588235294118  //  144/17 teeth      - Original Mount
//#define TILT_GEAR_RATIO 3.047619047619047619047619047619  //  64/21 teeth       - Original Mount

//#define PAN_GEAR_RATIO 4    //  160/40 teeth          - New Mount 1.8 degree steppers
//#define TILT_GEAR_RATIO 4   //  80/20 teeth           - New Mount

//#define PAN_GEAR_RATIO 8    //  160/40 *2 teeth       - New Mount 0.9 degree steppers
//#define TILT_GEAR_RATIO 8   //  80/20 *2 teeth        - New Mount

#define PAN_GEAR_RATIO 15    //  270/36 *2 teeth      - New Mount 0.9 degree steppers Pulley drive
#define TILT_GEAR_RATIO 15   //  120/16 *2 teeth      - New Mount

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

#define INSTRUCTION_INC_SLIDER_SPEED 'B'
#define INSTRUCTION_DEC_SLIDER_SPEED 'b'
#define INSTRUCTION_MAX_SLIDER_SPEED 'C'
#define INSTRUCTION_MIN_SLIDER_SPEED 'c'
#define INSTRUCTION_SET_INC_SLIDER_SPEED 'd'
#define INSTRUCTION_SET_MIN_SLIDER_SPEED 'f'
#define INSTRUCTION_SET_MAX_SLIDER_SPEED 'F'

#define INSTRUCTION_RESTORE_DEFAULT_SPEEDS 'l'

#define INSTRUCTION_PAN_ACCEL 'q'
#define INSTRUCTION_TILT_ACCEL 'Q'
#define INSTRUCTION_SLIDER_ACCEL 'w'

#define INSTRUCTION_PAN_JOY_ACCEL 'e'
#define INSTRUCTION_TILT_JOY_ACCEL 'E'
#define INSTRUCTION_SLIDER_JOY_ACCEL 'D'

#define INSTRUCTION_SET_FAST_SPEED 'V'
#define INSTRUCTION_SET_SLOW_SPEED 'v'

#define INSTRUCTION_DEBUG_STATUS 'R'
#define INSTRUCTION_POSITION_STATUS 'r'
#define INSTRUCTION_KEYFRAMES_STATUS 'k'
#define INSTRUCTION_RESET_LEDS 'W'
#define INSTRUCTION_CLEAR_ARRAY 'Y'
#define INSTRUCTION_SAVE_TO_EEPROM 'U'

#define INSTRUCTION_SET_ZERO_POS 'h'

#define INSTRUCTION_IS_CAM_ACCEL 'K'
#define INSTRUCTION_IS_CAM_SPEEDPT 'i'
#define INSTRUCTION_IS_CAM_SPEEDSl 'I'
#define INSTRUCTION_IS_CAM_DELAY 'j'

#define INSTRUCTION_IS_RUN_CAM 'J'
#define INSTRUCTION_IS_RUN_CAM_MOVES 'L'

#define INSTRUCTION_DIRECT_MOVE 'm'
#define INSTRUCTION_SETPOS 'M'

#define INSTRUCTION_ZOOM_IN 'Z'
#define INSTRUCTION_ZOOM_OUT 'z'
#define INSTRUCTION_STOP_ZOOM 'N'

#define INSTRUCTION_TOGGLE_RECORDING 'u'
#define INSTRUCTION_IS_RECORDING 'G'
#define INSTRUCTION_IS_NOT_RECORDING 'g'

#define EEPROM_ADDRESS_PAN_SET_SPEED 12
#define EEPROM_ADDRESS_TILT_SET_SPEED 16
#define EEPROM_ADDRESS_SLIDER_SET_SPEED 20
#define EEPROM_ADDRESS_SLIDER_INC_SPEED 36
#define EEPROM_ADDRESS_SLIDER_MIN_SPEED 40
#define EEPROM_ADDRESS_SLIDER_MAX_SPEED 44
#define EEPROM_ADDRESS_PAN_ACCEL 48
#define EEPROM_ADDRESS_TILT_ACCEL 56
#define EEPROM_ADDRESS_SLIDER_ACCEL 64
#define EEPROM_ADDRESS_PAN_JOY_ACCEL 72
#define EEPROM_ADDRESS_TILT_JOY_ACCEL 80
#define EEPROM_ADDRESS_SLIDER_JOY_ACCEL 88

#define VERSION_NUMBER "Version: 8.5\n8 Sept 2022"

/*
 * a
 * 
 * b
 * B
 * c
 * C
 * d
 * D
 * e
 * E
 * f
 * F
 * g
 * G
 * 
 * 
 * i
 * I
 * j
 * J
 * k
 * K
 * l
 * L
 * m
 * M
 * 
 * N
 * 
 * 
 * p
 * P
 * q
 * Q
 * r
 * R
 * s
 * S
 * t
 * T
 * 
 * U
 * v
 * V
 * w
 * W
 * x
 * X
 * 
 * 
 * z
 * Z
 * 
 */

bool DEBUG1 = false;
bool useKeyframeSpeeds = false;

char stringText[MAX_STRING_LENGTH + 1];
char c;

float pan_steps_per_degree = (200.0 * 16 * PAN_GEAR_RATIO) / 360.0;           //  Stepper motor has 200 steps per 360 degrees
float tilt_steps_per_degree = (200.0 * 16 * TILT_GEAR_RATIO) / 360.0;         //  Stepper motor has 200 steps per 360 degrees
float slider_steps_per_millimetre = (200.0 * 16) / (SLIDER_PULLEY_TEETH * 2); //  Stepper motor has 200 steps per 360 degrees, the timing pully has 36 teeth and the belt has a pitch of 2mm

float pan_set_speed = 20;           //  degrees/second.
float tilt_set_speed = 20;          //  degrees/second.
float slider_set_speed = 60;        //  mm/second.

float pan_def_speed = 20;
float tilt_def_speed = 20;
float slider_def_speed = 60;

float slider_inc_speed = 10;
float slider_min_speed = 10;
float slider_max_speed = 150;

int LEDsliderSpeed;
int LEDpanSpeed;
int LEDtiltSpeed;
int LEDPTSpeed;

float tempPanSpeed = 0;
float tempTiltSpeed = 0;
float tempSliderSpeed = 0;

int SerialCommandValueInt;
float SerialCommandValueFloat;

float pan_accel = 500;
float tilt_accel = 500;
float slider_accel = 500;

float panMaxFactor = 1.0;             // Speed factor of joystick moves ( 1 = 100% )
float tiltMaxFactor = 1.0;
float sliderMaxFactor = 1.0;

float panAccelJoy = 1;                // Accel factor of joystick moves ( 1 = 100% )
float tiltAccelJoy = 1;
float sliderAccelJoy = 1;

String atIndex = "";

float speedFactorS = 0.0;
float speedFactorP = 0.0;
float speedFactorT = 0.0;

bool sentMoved = false;

bool motorRunning = false;

unsigned long previousMillis = 0;
const long zoomInterval = 50;
bool zoomIN = false;
bool zoomOUT = false;
int zoom_speed;

bool pos1set = false;
bool pos2set = false;
bool pos3set = false;
bool pos4set = false;
bool pos5set = false;
bool pos6set = false;

bool atPos1 = false;
bool atPos2 = false;
bool atPos3 = false;
bool atPos4 = false;
bool atPos5 = false;
bool atPos6 = false;

bool isManualMove = false;
unsigned long previousMillisMoveCheck = 0;
unsigned long currentMillisMoveCheck = 0;
long moveCheckInterval = 1000;

int camDlyNo = 0;
unsigned long previousTime;

int dlyPos = 0;

int dlyPos1Time = 0;
int dlyPos2Time = 0;
int dlyPos3Time = 0;
int dlyPos4Time = 0;
int dlyPos5Time = 0;

bool isLastRunMove = false;
bool runCamLoop = false;
bool runCamLoopMoves = false;
int counter = 1;
int targetTimer = 3000;
static unsigned lastTick = 0;
constexpr unsigned PID_Interval = 10;   // ms
//constexpr float P = 0.0011;             // (P)roportional constant of the regulator needs to be adjusted (depends on speed and acceleration setting)
constexpr float P = 0.0014;
int32_t targetP = 0;
int32_t targetT = 0;
int32_t targetS = 0;
float deltaP = 0.0;
float deltaT = 0.0; 
float deltaS = 0.0;
float factorP = 0.0;
float factorT = 0.0;
float factorS = 0.0;
bool panEnd = false;
bool tiltEnd = false;
bool sliderEnd = false;

//elapsedMillis retargetTimer = 0;
//elapsedMillis outputTimer = 0;

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

struct KeyframeElement {
    long panStepCount = 0;
    float panSpeed = 0;
    long tiltStepCount = 0;
    float tiltSpeed = 0;
    long sliderStepCount = 0;
    float sliderSpeed = 0;
    int isRecorded = 0;
    int runDelay = 4000;
    int runAccel = 2000;
};

struct FloatCoordinate {
    float x;
    float y;
    float z;
};

struct LinePoints {
    float x0;
    float y0;
    float x1;
    float y1;
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
void setEEPROMVariables(void);
void scaleKeyframeSpeed(float);

/*------------------------------------------------------------------------------------------------------------------------------------------------------*/

#endif
