#include <EEPROM.h>

#define BAUD_RATE 38400  //9600 //57600

#define SLIDER_PULLEY_TEETH 20.0  // old value 36.0  // 36 teeth, 1.8 deg stepper

#define PAN_GEAR_RATIO 15   //  270/36 * 2 - (270 tooth / 36 tooth) * 2 mm (GT2 belt)     - 0.9 degree steppers
#define TILT_GEAR_RATIO 15  //  120/16 * 2 - (120 tooth / 16 tooth) * 2 mm (GT2 belt)     - 0.9 degree steppers

#define MAX_STRING_LENGTH 10

#define INSTRUCTION_IS_COMMAND '?'

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

#define INSTRUCTION_PANTILT_ACCEL 'Q'
#define INSTRUCTION_SLIDER_ACCEL 'q'

#define INSTRUCTION_DEBUG_STATUS 'R'
#define INSTRUCTION_SAVE_TO_EEPROM 'U'

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

float slideLimit = 130000;  // 3 metres
float zoomLimit = 5550;     // 12 - 35mm

char stringText[MAX_STRING_LENGTH + 1];
char c;

float pan_steps_per_degree = (400.0 * 16 * PAN_GEAR_RATIO) / 360.0;            //  Stepper motor has 400 steps per 360 degrees (0.9 deg per step). Steps per full motor rotation * micro stepping / 360 (per deg)
float tilt_steps_per_degree = (400.0 * 16 * TILT_GEAR_RATIO) / 360.0;          //  Stepper motor has 400 steps per 360 degrees
float slider_steps_per_millimetre = (200.0 * 16) / (SLIDER_PULLEY_TEETH * 2);  //  Stepper motor has 200 steps per 360 degrees, the timing pully has 20 teeth and the belt has a pitch of 2mm

float pantilt_set_speed = 20;  //  degrees/second.
float slider_set_speed = 60;   //  mm/second.

float pantilt_accel = 1000;
float slider_accel = 8000;

float pantilt_speed1 = 1;
float pantilt_speed2 = 5;
float pantilt_speed3 = 10;
float pantilt_speed4 = 20;

float slider_speed1 = 20;
float slider_speed2 = 40;
float slider_speed3 = 80;
float slider_speed4 = 120;

float zoom_set_speed = 2000;
float zoom_accel = 16000;

int SerialCommandValueInt;
float SerialCommandValueFloat;

float panDegreesToSteps(float angle) {
  return pan_steps_per_degree * angle;
}
float tiltDegreesToSteps(float angle) {
  return tilt_steps_per_degree * angle;
}
long sliderMillimetresToSteps(float mm) {
  return round(mm * slider_steps_per_millimetre);
}
float sliderStepsToMillimetres(long steps) {
  return (float)steps / slider_steps_per_millimetre;
}
float panStepsToDegrees(long steps) {
  return steps / pan_steps_per_degree;
}
float panStepsToDegrees(float steps) {
  return steps / pan_steps_per_degree;
}
float tiltStepsToDegrees(long steps) {
  return steps / tilt_steps_per_degree;
}
float tiltStepsToDegrees(float steps) {
  return steps / tilt_steps_per_degree;
}

void SerialFlush(void) {
  while (Serial.available() > 0) {
    c = Serial.read();
  }
}

void saveEEPROM(void) {
  EEPROM.put(EEPROM_ADDRESS_PANTILT_SET_SPEED, pantilt_set_speed);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SET_SPEED, slider_set_speed);
  EEPROM.put(EEPROM_ADDRESS_SLIDE_LIMIT, slideLimit);
  EEPROM.put(EEPROM_ADDRESS_ZOOM_LIMIT, zoomLimit);
  EEPROM.put(EEPROM_ADDRESS_PANTILT_ACCEL, pantilt_accel);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_ACCEL, slider_accel);
  EEPROM.put(EEPROM_ADDRESS_PANTILT_SPEED1, pantilt_speed1);
  EEPROM.put(EEPROM_ADDRESS_PANTILT_SPEED2, pantilt_speed2);
  EEPROM.put(EEPROM_ADDRESS_PANTILT_SPEED3, pantilt_speed3);
  EEPROM.put(EEPROM_ADDRESS_PANTILT_SPEED4, pantilt_speed4);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SPEED1, slider_speed1);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SPEED2, slider_speed2);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SPEED3, slider_speed3);
  EEPROM.put(EEPROM_ADDRESS_SLIDER_SPEED4, slider_speed4);

  Serial.println("Saved to EEPROM.\n");
}
void printEEPROM(void) {
  float ftemp;
  Serial.println("\nEEPROM:");
  EEPROM.get(EEPROM_ADDRESS_PANTILT_SET_SPEED, ftemp);
  Serial.println(String("Pan/Tilt Speed      : ") + ftemp + String(" deg/s"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SET_SPEED, ftemp);
  Serial.println(String("Slider Speed        : ") + ftemp + String(" mm/s\n"));
  EEPROM.get(EEPROM_ADDRESS_SLIDE_LIMIT, ftemp);
  Serial.println(String("Slide Limit         : ") + sliderStepsToMillimetres(ftemp) + String(" mm"));
  EEPROM.get(EEPROM_ADDRESS_ZOOM_LIMIT, ftemp);
  Serial.println(String("Zoom Limit          : ") + ftemp + String("\n"));
  EEPROM.get(EEPROM_ADDRESS_PANTILT_ACCEL, ftemp);
  Serial.println(String("Pan/Tilt accel      : ") + ftemp + String(" steps/sSq"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_ACCEL, ftemp);
  Serial.println(String("Slider accel        : ") + ftemp + String(" steps/sSq\n"));
  EEPROM.get(EEPROM_ADDRESS_PANTILT_SPEED1, ftemp);
  Serial.println(String("Pan/Tilt Speed 1    : ") + ftemp + String(" deg/s"));
  EEPROM.get(EEPROM_ADDRESS_PANTILT_SPEED2, ftemp);
  Serial.println(String("Pan/Tilt Speed 2    : ") + ftemp + String(" deg/s"));
  EEPROM.get(EEPROM_ADDRESS_PANTILT_SPEED3, ftemp);
  Serial.println(String("Pan/Tilt Speed 3    : ") + ftemp + String(" deg/s"));
  EEPROM.get(EEPROM_ADDRESS_PANTILT_SPEED4, ftemp);
  Serial.println(String("Pan/Tilt Speed 4    : ") + ftemp + String(" deg/s\n"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SPEED1, ftemp);
  Serial.println(String("Slider Speed 1      : ") + ftemp + String(" mm/s"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SPEED2, ftemp);
  Serial.println(String("Slider Speed 2      : ") + ftemp + String(" mm/s"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SPEED3, ftemp);
  Serial.println(String("Slider Speed 3      : ") + ftemp + String(" mm/s"));
  EEPROM.get(EEPROM_ADDRESS_SLIDER_SPEED4, ftemp);
  Serial.println(String("Slider Speed 4      : ") + ftemp + String(" mm/s\n"));
}

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  char instruction;
  if (Serial.available() > 0) {
    instruction = Serial.read();
  }
  if (instruction == INSTRUCTION_IS_COMMAND) {
    delay(2);  //wait to make sure all data in the Serial message has arived
    instruction = Serial.read();
    memset(&stringText[0], 0, sizeof(stringText));  //clear the array
    while (Serial.available()) {                    //set elemetns of stringText to the Serial values sent
      char digit = Serial.read();                   //read in a char
      strncat(stringText, &digit, 1);               //add digit to the end of the array
    }
    SerialFlush();                               //Clear any excess data in the Serial buffer
    SerialCommandValueInt = atoi(stringText);    //converts stringText to an int
    SerialCommandValueFloat = atof(stringText);  //converts stringText to a float
    if (instruction == '+') {                    //The Bluetooth module sends a message starting with "+CONNECTING" which should be discarded.
      delay(100);                                //wait to make sure all data in the Serial message has arived
      SerialFlush();                             //Clear any excess data in the Serial buffer
      return;
    }


    switch (instruction) {
      case INSTRUCTION_SET_PANTILT_SPEED1:
        {
          pantilt_speed1 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_PANTILT_SPEED2:
        {
          pantilt_speed2 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_PANTILT_SPEED3:
        {
          pantilt_speed3 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_PANTILT_SPEED4:
        {
          pantilt_speed4 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_SLIDER_SPEED1:
        {
          slider_speed1 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_SLIDER_SPEED2:
        {
          slider_speed2 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_SLIDER_SPEED3:
        {
          slider_speed3 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_SLIDER_SPEED4:
        {
          slider_speed4 = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SET_SLIDE_LIMIT:
        {
          slideLimit = sliderMillimetresToSteps(SerialCommandValueInt);
        }
        break;
      case INSTRUCTION_SET_ZOOM_LIMIT:
        {
          zoomLimit = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_PANTILT_ACCEL:
        {
          pantilt_accel = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SLIDER_ACCEL:
        {
          slider_accel = SerialCommandValueInt;
        }
        break;
      case INSTRUCTION_SAVE_TO_EEPROM:
        {
          saveEEPROM();
        }
        break;
      case INSTRUCTION_DEBUG_STATUS:
        {
          printEEPROM();
        }
        break;
      default:
        break;  // if unrecognised charater, do nothing
    }
  }
}
