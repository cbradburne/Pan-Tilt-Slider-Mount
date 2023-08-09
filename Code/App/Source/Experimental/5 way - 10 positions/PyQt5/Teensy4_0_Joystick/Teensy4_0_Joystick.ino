int joyPinX = 20;
int joyPinY = 21;
int joyPinZ = 22;
int joyPinW = 23;

int joyPinT = 19;

int joyPinB1 = 2;
int joyPinB2 = 3;
int joyPinB3 = 4;
int joyPinB4 = 5;
int joyPinB5 = 6;

int joyPinLED1 = 7;
int joyPinLED2 = 8;
int joyPinLED3 = 9;
int joyPinLED4 = 10;
int joyPinLED5 = 11;

float joyX;
float joyY;
float joyZ;
float joyW;
float joyT;

bool joyB1 = false;
bool OLDjoyB1 = true;
bool joyB2 = false;
bool OLDjoyB2 = true;
bool joyB3 = false;
bool OLDjoyB3 = true;
bool joyB4 = false;
bool OLDjoyB4 = true;
bool joyB5 = false;
bool OLDjoyB5 = true;

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
  pinMode(joyPinX, INPUT);
  pinMode(joyPinY, INPUT);
  pinMode(joyPinZ, INPUT);
  pinMode(joyPinW, INPUT);
  pinMode(joyPinT, INPUT);

  pinMode(joyPinB1, INPUT_PULLUP);
  pinMode(joyPinB2, INPUT_PULLUP);
  pinMode(joyPinB3, INPUT_PULLUP);
  pinMode(joyPinB4, INPUT_PULLUP);
  pinMode(joyPinB5, INPUT_PULLUP);

  pinMode(joyPinLED1, OUTPUT);
  pinMode(joyPinLED2, OUTPUT);
  pinMode(joyPinLED3, OUTPUT);
  pinMode(joyPinLED4, OUTPUT);
  pinMode(joyPinLED5, OUTPUT);

  digitalWrite(joyPinLED1, HIGH);
  digitalWrite(joyPinLED2, LOW);
  digitalWrite(joyPinLED3, LOW);
  digitalWrite(joyPinLED4, LOW);
  digitalWrite(joyPinLED5, LOW);
  delay(50);
  digitalWrite(joyPinLED1, LOW);
  digitalWrite(joyPinLED2, HIGH);
  digitalWrite(joyPinLED3, LOW);
  digitalWrite(joyPinLED4, LOW);
  digitalWrite(joyPinLED5, LOW);
  delay(50);
  digitalWrite(joyPinLED1, LOW);
  digitalWrite(joyPinLED2, LOW);
  digitalWrite(joyPinLED3, HIGH);
  digitalWrite(joyPinLED4, LOW);
  digitalWrite(joyPinLED5, LOW);
  delay(50);
  digitalWrite(joyPinLED1, LOW);
  digitalWrite(joyPinLED2, LOW);
  digitalWrite(joyPinLED3, LOW);
  digitalWrite(joyPinLED4, HIGH);
  digitalWrite(joyPinLED5, LOW);
  delay(50);
  digitalWrite(joyPinLED1, LOW);
  digitalWrite(joyPinLED2, LOW);
  digitalWrite(joyPinLED3, LOW);
  digitalWrite(joyPinLED4, LOW);
  digitalWrite(joyPinLED5, HIGH);
  delay(50);
  digitalWrite(joyPinLED1, LOW);
  digitalWrite(joyPinLED2, LOW);
  digitalWrite(joyPinLED3, LOW);
  digitalWrite(joyPinLED4, LOW);
  digitalWrite(joyPinLED5, LOW);
  delay(50);
}

void loop() {
  doJoystick();
  delay(50);
  //Serial.begin(38400);
}

void doJoystick() {

  joyX = analogRead(joyPinX);
  if (joyX < XdeadRangeLow) {
    XShort = map(joyX, X_min, XdeadRangeLow, 0, 512);
    //Serial.println(XShort);
    if (XShort < 0) {
      XShort = 0;
    }
  } else if (joyX > XdeadRangeHigh) {
    XShort = map(joyX, XdeadRangeHigh, X_max, 512, 1023);
    //Serial.println(XShort);
    if (XShort > 1023) {
      XShort = 1023;
    }
  } else {
    XShort = 512;
  }

  joyY = analogRead(joyPinY);
  if (joyY < YdeadRangeLow) {
    YShort = map(joyY, Y_min, YdeadRangeLow, 0, 512);
    //Serial.println(YShort);
    if (YShort < 0) {
      YShort = 0;
    }
  } else if (joyY > YdeadRangeHigh) {
    YShort = map(joyY, YdeadRangeHigh, Y_max, 512, 1023);
    //Serial.println(YShort);
    if (YShort > 1023) {
      YShort = 1023;
    }
  } else {
    YShort = 512;
  }

  joyZ = analogRead(joyPinZ);
  if (joyZ < ZdeadRangeLow) {
    ZShort = map(joyZ, Z_min, ZdeadRangeLow, 0, 512);
    //Serial.println(ZShort);
    if (ZShort < 0) {
      ZShort = 0;
    }
  } else if (joyZ > ZdeadRangeHigh) {
    ZShort = map(joyZ, ZdeadRangeHigh, Z_max, 512, 1023);
    //Serial.println(ZShort);
    if (ZShort > 1023) {
      ZShort = 1023;
    }
  } else {
    ZShort = 512;
  }

  joyW = analogRead(joyPinW);
  if (joyW < WdeadRangeLow) {
    WShort = map(joyW, W_min, WdeadRangeLow, 0, 512);
    //Serial.println(WShort);
    if (WShort < 0) {
      WShort = 0;
    }
  } else if (joyW > WdeadRangeHigh) {
    WShort = map(joyW, WdeadRangeHigh, W_max, 512, 1023);
    //Serial.println(WShort);
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

  //joyB = digitalRead(joyPinB);

  //if (joyB != OLDjoyB) {
  //  if (joyB) {
  //    Joystick.button(1, 0);
  //  } else {
  //    Joystick.button(1, 1);
  //  }
  //  OLDjoyB = joyB;
  //}
  ////Serial.println(TShort);



  joyB1 = digitalRead(joyPinB1);
  if (joyB1 != OLDjoyB1) {
    if (joyB1) {
      Joystick.button(1, 0);
    } else {
      Joystick.button(1, 1);
    }
    OLDjoyB1 = joyB1;
  }


  joyB2 = digitalRead(joyPinB2);
  if (joyB2 != OLDjoyB2) {
    if (joyB2) {
      Joystick.button(2, 0);
    } else {
      Joystick.button(2, 1);
    }
    OLDjoyB2 = joyB2;
  }

  joyB3 = digitalRead(joyPinB3);
  if (joyB3 != OLDjoyB3) {
    if (joyB3) {
      Joystick.button(3, 0);
    } else {
      Joystick.button(3, 1);
    }
    OLDjoyB3 = joyB3;
  }

  joyB4 = digitalRead(joyPinB4);
  if (joyB4 != OLDjoyB4) {
    if (joyB4) {
      Joystick.button(4, 0);
    } else {
      Joystick.button(4, 1);
    }
    OLDjoyB4 = joyB4;
  }

  joyB5 = digitalRead(joyPinB5);
  if (joyB5 != OLDjoyB5) {
    if (joyB5) {
      Joystick.button(5, 0);
    } else {
      Joystick.button(5, 1);
    }
    OLDjoyB5 = joyB5;
  }


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

  Joystick.X(XShort);
  Joystick.Y(YShort);
  Joystick.Z(ZShort);
  Joystick.Zrotate(WShort);

  Joystick.hat(-1);
  //Joystick.sliderRight(TShort);
}
