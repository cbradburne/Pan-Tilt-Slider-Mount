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

int speed1 = 20;                         //  Pan & Tilt speed settings
int speed2 = 10;
int speed3 = 5;
int speed4 = 1;

//String readSerial1;
//String readSerial2;
//String readSerial3;

int whichSerialCam = 1;

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

bool LEDstate = LOW;

int s1Speed = 0;
int olds1Speed = 3;
int s2Speed = 0;
int olds2Speed = 3;
int s3Speed = 0;
int olds3Speed = 3;

int cam1PTSpeed = 0;
int cam2PTSpeed = 0;
int cam3PTSpeed = 0;
