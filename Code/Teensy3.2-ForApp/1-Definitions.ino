#include "Definitions.h"

void initPCTeensy(void) {
  Serial.begin(38400);
  Serial1.begin(38400);
  Serial2.begin(38400);
  Serial3.begin(38400);

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
