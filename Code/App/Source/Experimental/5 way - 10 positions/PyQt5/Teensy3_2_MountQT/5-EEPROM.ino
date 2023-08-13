//  EEPROM

void saveEEPROM(void) {
  EEPROM.put(EEPROM_ADDRESS_PAN_SET_SPEED, pan_set_speed);
  EEPROM.put(EEPROM_ADDRESS_TILT_SET_SPEED, tilt_set_speed);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SET_SPEED, slider_set_speed);
  EEPROM.put(EEPROM_ADDRESS_PAN_ACCEL, pan_accel);
  EEPROM.put(EEPROM_ADDRESS_TILT_ACCEL, tilt_accel);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_ACCEL, slider_accel);
  EEPROM.put(EEPROM_ADDRESS_PAN_JOY_ACCEL, panAccelJoy);
  EEPROM.put(EEPROM_ADDRESS_TILT_JOY_ACCEL, tiltAccelJoy);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_JOY_ACCEL, sliderAccelJoy);

  Serial1.println("Saved to EEPROM.\n");
  Serial1.println("#$");
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void setEEPROMVariables(void) {
  EEPROM.get(EEPROM_ADDRESS_PAN_SET_SPEED, pan_set_speed);
  EEPROM.get(EEPROM_ADDRESS_TILT_SET_SPEED, tilt_set_speed);
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SET_SPEED, slider_set_speed);
  EEPROM.get(EEPROM_ADDRESS_PAN_ACCEL, pan_accel);
  EEPROM.get(EEPROM_ADDRESS_TILT_ACCEL, tilt_accel);
  EEPROM.get(EEPROM_ADDRESS_SLIDER_ACCEL, slider_accel);
  EEPROM.get(EEPROM_ADDRESS_PAN_JOY_ACCEL, panAccelJoy);
  EEPROM.get(EEPROM_ADDRESS_TILT_JOY_ACCEL, tiltAccelJoy);
  EEPROM.get(EEPROM_ADDRESS_SLIDER_JOY_ACCEL, sliderAccelJoy);

  pan_def_speed = pan_set_speed;
  tilt_def_speed = tilt_set_speed;
  slider_def_speed = slider_set_speed;
}


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


void printEEPROM(void) {
  float ftemp;
  //Serial.println("EEPROM:");
  Serial1.println("EEPROM:");
  EEPROM.get(EEPROM_ADDRESS_PAN_SET_SPEED, ftemp);
  Serial1.println(String("Pan Speed               : ") + ftemp + String("°/s"));
  EEPROM.get(EEPROM_ADDRESS_TILT_SET_SPEED, ftemp);
  Serial1.println(String("Tilt Speed              : ") + ftemp + String("°/s"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SET_SPEED, ftemp);
  Serial1.println(String("Slider Speed            : ") + ftemp + String("mm/s\n"));
  EEPROM.get(EEPROM_ADDRESS_PAN_ACCEL, ftemp);
  Serial1.println(String("Pan accel               : ") + ftemp + String(" steps/s²"));
  EEPROM.get(EEPROM_ADDRESS_TILT_ACCEL, ftemp);
  Serial1.println(String("Tilt accel              : ") + ftemp + String(" steps/s²"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_ACCEL, ftemp);
  Serial1.println(String("Slider accel            : ") + ftemp + String(" steps/s²\n"));
  EEPROM.get(EEPROM_ADDRESS_PAN_JOY_ACCEL, ftemp);
  Serial1.println(String("Pan Joy accel factor    : ") + ftemp);
  EEPROM.get(EEPROM_ADDRESS_TILT_JOY_ACCEL, ftemp);
  Serial1.println(String("Tilt Joy accel factor   : ") + ftemp);
  EEPROM.get(EEPROM_ADDRESS_SLIDER_JOY_ACCEL, ftemp);
  Serial1.println(String("Slider Joy accel factor : ") + ftemp + String("\n"));

  Serial1.print("\n");
  Serial1.println("#$");
}