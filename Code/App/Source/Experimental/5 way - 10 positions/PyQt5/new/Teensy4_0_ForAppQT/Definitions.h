short shortVals[3] = {0, 0, 0};
short XShort = 0;
short YShort = 0;
short ZShort = 0;
short oldShortVal0 = 0;
short oldShortVal1 = 0;
short oldShortVal2 = 0;

String inData1;
String inData2;
String inData3;
String inData4;
String inData5;
String inData6;

String inData1Temp;
String inData2Temp;
String inData3Temp;
String inData4Temp;
String inData5Temp;

//int speed1 = 1;                         //  Pan & Tilt speed settings
//int speed2 = 5;
//int speed3 = 10;
//int speed4 = 20;

//int Sspeed1 = 20;
//int Sspeed2 = 60;
//int Sspeed3 = 120;
//int Sspeed4 = 160;

int whichSerialCam = 1;

int SerialCommandValueInt;

bool resetLEDs = false;
bool startLEDs = true;
bool doLEDrefresh = false;
bool doLEDrefresh2 = false;
bool doLEDrefresh3 = false;
bool doLEDrefresh4 = false;
bool doLEDrefresh5 = false;
bool doLEDrefresh6 = false;
unsigned long previousMillisLED = 0;
unsigned long currentMillisLED = 0;
unsigned long LEDInterval = 500;

bool LEDstate = LOW;

int s1Speed = 0;
int olds1Speed = 3;
int s2Speed = 0;
int olds2Speed = 3;
int s3Speed = 0;
int olds3Speed = 3;
int s4Speed = 0;
int olds4Speed = 3;
int s5Speed = 0;
int olds5Speed = 3;

int s1SSpeed = 0;
int olds1SSpeed = 2;
int s2SSpeed = 0;
int olds2SSpeed = 2;
int s3SSpeed = 0;
int olds3SSpeed = 2;
int s4SSpeed = 0;
int olds4SSpeed = 2;
int s5SSpeed = 0;
int olds5SSpeed = 2;

int cam1PTSpeed = 0;
int cam2PTSpeed = 0;
int cam3PTSpeed = 0;
int cam4PTSpeed = 0;
int cam5PTSpeed = 0;
