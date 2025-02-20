/*
 * Motorised Pan, Tilt, Slide mount.
 * 
 * Using:
 * Teensy 3.2           Development board
 * TMC2208 TMC2209      Stepper motor drivers
 * 
 * Original concept by isaac879 
 * Original project video: https://youtu.be/1FfB7cLkUyQ
 * 
 * Modified by Colin Bradburne
 * 
 * Testing and PCB design Tony McGuire
 * 
 */


void setup(){
    initPanTilt();
}

void loop(){
    mainLoop();
}