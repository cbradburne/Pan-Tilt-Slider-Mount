int joyPinX = 21;
int joyPinY = 22;
int joyPinZ = 19;
int joyPinW = 23;

int joyPinT = 17;
int joyPinB = 18;

float joyX;
float joyY;
float joyZ;
float joyW;
float joyT;
bool joyB = false;
bool OLDjoyB = true;

const int XdeadRangeLow = 500;
const int XdeadRangeHigh = 560;
const int YdeadRangeLow = 480;
const int YdeadRangeHigh = 540;
const int ZdeadRangeLow = 500;
const int ZdeadRangeHigh = 560;
const int WdeadRangeLow = 500;
const int WdeadRangeHigh = 560;
const int TdeadRangeLow = 500;
const int TdeadRangeHigh = 560;

int X_min = 2;
int X_max = 1023;
int Y_min = 2;
int Y_max = 1023;
int Z_min = 2;
int Z_max = 1023;
int W_min = 2;
int W_max = 1023;
int T_min = 2;
int T_max = 1023;
short XShort = 0;
short YShort = 0;
short ZShort = 0;
short WShort = 0;
short TShort = 0;

void setup() {
  //Serial.begin(9600);
  pinMode(joyPinX, INPUT);
  pinMode(joyPinY, INPUT);
  pinMode(joyPinZ, INPUT);
  pinMode(joyPinW, INPUT);
  pinMode(joyPinT, INPUT);
  pinMode(joyPinB, INPUT_PULLUP);
}

void loop() {
  doJoystick();
  delay(50);
}

void doJoystick() {
  joyX = analogRead(joyPinX);
  if (joyX < XdeadRangeLow) {
    XShort = map(joyX, X_min, XdeadRangeLow, 0, 512);
    if (XShort < 0) {
      XShort = 0;
    }
  } else if (joyX > XdeadRangeHigh) {
    XShort = map(joyX, XdeadRangeHigh, X_max, 512, 1023);
    if (XShort > 1023) {
      XShort = 1023;
    }
  } else {
    XShort = 512;
  }

  joyY = analogRead(joyPinY);
  if (joyY < YdeadRangeLow) {
    YShort = map(joyY, Y_min, YdeadRangeLow, 0, 512);
    if (YShort < 0) {
      YShort = 0;
    }
  } else if (joyY > YdeadRangeHigh) {
    YShort = map(joyY, YdeadRangeHigh, Y_max, 512, 1023);
    if (YShort > 1023) {
      YShort = 1023;
    }
  } else {
    YShort = 512;
  }

  joyZ = analogRead(joyPinZ);
  if (joyZ < ZdeadRangeLow) {
    ZShort = map(joyZ, Z_min, ZdeadRangeLow, 0, 512);
    if (ZShort < 0) {
      ZShort = 0;
    }
  } else if (joyZ > ZdeadRangeHigh) {
    ZShort = map(joyZ, ZdeadRangeHigh, Z_max, 512, 1023);
    if (ZShort > 1023) {
      ZShort = 1023;
    }
  } else {
    ZShort = 512;
  }

  joyW = analogRead(joyPinW);
  if (joyW < WdeadRangeLow) {
    WShort = map(joyW, W_min, WdeadRangeLow, 0, 512);
    if (WShort < 0) {
      WShort = 0;
    }
  } else if (joyW > WdeadRangeHigh) {
    WShort = map(joyW, WdeadRangeHigh, W_max, 512, 1023);
    if (WShort > 1023) {
      WShort = 1023;
    }
  } else {
    WShort = 512;
  }

  joyT = analogRead(joyPinT);
  if (joyT < TdeadRangeLow) {
    TShort = map(joyT, T_min, TdeadRangeLow, 0, 512);
    if (TShort < 0) {
      TShort = 0;
    }
  } else if (joyT > TdeadRangeHigh) {
    TShort = map(joyT, TdeadRangeHigh, T_max, 512, 1023);
    if (TShort > 1023) {
      TShort = 1023;
    }
  } else {
    TShort = 512;
  }

  joyB = digitalRead(joyPinB);

  if (joyB != OLDjoyB) {
    if (joyB) {
      Joystick.button(1, 0);
    } else {
      Joystick.button(1, 1);
    }
    OLDjoyB = joyB;
  }
  //Serial.println(TShort);

  Joystick.X(XShort);
  Joystick.Y(YShort);
  Joystick.Z(ZShort);
  Joystick.Zrotate(WShort);

  //Joystick.button(1, 0);
  //Joystick.button(1, 0);
  //Joystick.button(2, 0);
  //Joystick.button(3, 0);
  //Joystick.button(4, 0);
  //Joystick.button(5, 0);
  //Joystick.button(6, 0);
  //Joystick.button(7, 0);
  //Joystick.button(8, 0);
  //Joystick.button(9, 0);
  //Joystick.button(10, 0);

  Joystick.hat(-1);
  //Joystick.sliderRight(TShort);

}
