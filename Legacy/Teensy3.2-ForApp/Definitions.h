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

int speed1 = 20;                         //  Pan & Tilt speed settings
int speed2 = 10;
int speed3 = 5;
int speed4 = 1;

int whichSerialCam = 1;

int SerialCommandValueInt;

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

int cam1SlSpeed = 0;
int cam2SlSpeed = 0;
int cam3SlSpeed = 0;

int cam1PTSpeed = 0;
int cam2PTSpeed = 0;
int cam3PTSpeed = 0;

bool cam1Alive = false;
bool cam2Alive = false;
bool cam3Alive = false;

unsigned long previousCam1Alive = 0;
unsigned long previousCam2Alive = 0;
unsigned long previousCam3Alive = 0;
