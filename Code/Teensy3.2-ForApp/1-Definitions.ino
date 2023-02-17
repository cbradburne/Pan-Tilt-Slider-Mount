// Serial1  0  1
// Serial2  7  8
// Serial3 15 14
// Serial4 16 17
// Serial5 21 20

#include "Definitions.h"

void initPCTeensy(void) {
  Serial.begin(38400);
  Serial1.begin(38400);
  Serial2.begin(38400);
  Serial3.begin(38400);
  Serial4.begin(38400);
  Serial5.begin(38400);

  pinMode(13, OUTPUT);
  digitalWrite(13, LEDstate);
}

void mainLoop(void) {
  USBSerialData();

  Serial1Data();
  Serial2Data();
  Serial3Data();

  RefreshLEDs();
}
