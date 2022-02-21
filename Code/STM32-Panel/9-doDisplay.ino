
//  --  Do LED Display Matrix

void doDisplay() {
  /*
    if (oldRingLast != ringLast || oldxDisplay != xDisplay || oldyDisplay != yDisplay || olds1Speed != s1Speed || oldDisplayCommand != displayCommand || displayUpadte) {
    oldRingLast = ringLast;
    oldxDisplay = xDisplay;
    oldyDisplay = yDisplay;
    olds1Speed = s1Speed;
    oldDisplayCommand = displayCommand;
    oldIsRecording = isRecording;
    displayUpadte = false;

    matrix.clearScreen();
    }
  */

  if (oldRingLast != ringLast) {
    if (ringLast == 0) {
      matrix.setPixel(9, 1);
      matrix.setPixel(9, 2);
      matrix.setPixel(9, 3);
      matrix.setPixel(9, 4);
      matrix.setPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 1) {
      matrix.setPixel(9, 1);
      matrix.setPixel(9, 2);
      matrix.setPixel(9, 3);
      matrix.setPixel(9, 4);
      matrix.setPixel(9, 5);

      matrix.setPixel(8, 1);
      matrix.setPixel(8, 2);
      matrix.setPixel(8, 3);
      matrix.setPixel(8, 4);
      matrix.setPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 2) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.setPixel(8, 1);
      matrix.setPixel(8, 2);
      matrix.setPixel(8, 3);
      matrix.setPixel(8, 4);
      matrix.setPixel(8, 5);

      matrix.setPixel(7, 1);
      matrix.setPixel(7, 2);
      matrix.setPixel(7, 3);
      matrix.setPixel(7, 4);
      matrix.setPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 3) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.setPixel(7, 1);
      matrix.setPixel(7, 2);
      matrix.setPixel(7, 3);
      matrix.setPixel(7, 4);
      matrix.setPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 4) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.setPixel(7, 1);
      matrix.setPixel(7, 2);
      matrix.setPixel(7, 3);
      matrix.setPixel(7, 4);
      matrix.setPixel(7, 5);

      matrix.setPixel(6, 1);
      matrix.setPixel(6, 2);
      matrix.setPixel(6, 3);
      matrix.setPixel(6, 4);
      matrix.setPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 5) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.setPixel(6, 1);
      matrix.setPixel(6, 2);
      matrix.setPixel(6, 3);
      matrix.setPixel(6, 4);
      matrix.setPixel(6, 5);

      matrix.setPixel(5, 1);
      matrix.setPixel(5, 2);
      matrix.setPixel(5, 3);
      matrix.setPixel(5, 4);
      matrix.setPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 6) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.setPixel(5, 1);
      matrix.setPixel(5, 2);
      matrix.setPixel(5, 3);
      matrix.setPixel(5, 4);
      matrix.setPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 7) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.setPixel(5, 1);
      matrix.setPixel(5, 2);
      matrix.setPixel(5, 3);
      matrix.setPixel(5, 4);
      matrix.setPixel(5, 5);

      matrix.setPixel(4, 1);
      matrix.setPixel(4, 2);
      matrix.setPixel(4, 3);
      matrix.setPixel(4, 4);
      matrix.setPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 8) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.setPixel(4, 1);
      matrix.setPixel(4, 2);
      matrix.setPixel(4, 3);
      matrix.setPixel(4, 4);
      matrix.setPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 9) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.setPixel(4, 1);
      matrix.setPixel(4, 2);
      matrix.setPixel(4, 3);
      matrix.setPixel(4, 4);
      matrix.setPixel(4, 5);

      matrix.setPixel(3, 1);
      matrix.setPixel(3, 2);
      matrix.setPixel(3, 3);
      matrix.setPixel(3, 4);
      matrix.setPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 10) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.setPixel(3, 1);
      matrix.setPixel(3, 2);
      matrix.setPixel(3, 3);
      matrix.setPixel(3, 4);
      matrix.setPixel(3, 5);

      matrix.setPixel(2, 1);
      matrix.setPixel(2, 2);
      matrix.setPixel(2, 3);
      matrix.setPixel(2, 4);
      matrix.setPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 11) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.setPixel(2, 1);
      matrix.setPixel(2, 2);
      matrix.setPixel(2, 3);
      matrix.setPixel(2, 4);
      matrix.setPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 12) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.setPixel(2, 1);
      matrix.setPixel(2, 2);
      matrix.setPixel(2, 3);
      matrix.setPixel(2, 4);
      matrix.setPixel(2, 5);

      matrix.setPixel(1, 1);
      matrix.setPixel(1, 2);
      matrix.setPixel(1, 3);
      matrix.setPixel(1, 4);
      matrix.setPixel(1, 5);

      matrix.clrPixel(0, 1);
      matrix.clrPixel(0, 2);
      matrix.clrPixel(0, 3);
      matrix.clrPixel(0, 4);
      matrix.clrPixel(0, 5);
    }
    if (ringLast == 13) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.setPixel(1, 1);
      matrix.setPixel(1, 2);
      matrix.setPixel(1, 3);
      matrix.setPixel(1, 4);
      matrix.setPixel(1, 5);

      matrix.setPixel(0, 1);
      matrix.setPixel(0, 2);
      matrix.setPixel(0, 3);
      matrix.setPixel(0, 4);
      matrix.setPixel(0, 5);
    }
    if (ringLast == 14) {
      matrix.clrPixel(9, 1);
      matrix.clrPixel(9, 2);
      matrix.clrPixel(9, 3);
      matrix.clrPixel(9, 4);
      matrix.clrPixel(9, 5);

      matrix.clrPixel(8, 1);
      matrix.clrPixel(8, 2);
      matrix.clrPixel(8, 3);
      matrix.clrPixel(8, 4);
      matrix.clrPixel(8, 5);

      matrix.clrPixel(7, 1);
      matrix.clrPixel(7, 2);
      matrix.clrPixel(7, 3);
      matrix.clrPixel(7, 4);
      matrix.clrPixel(7, 5);

      matrix.clrPixel(6, 1);
      matrix.clrPixel(6, 2);
      matrix.clrPixel(6, 3);
      matrix.clrPixel(6, 4);
      matrix.clrPixel(6, 5);

      matrix.clrPixel(5, 1);
      matrix.clrPixel(5, 2);
      matrix.clrPixel(5, 3);
      matrix.clrPixel(5, 4);
      matrix.clrPixel(5, 5);

      matrix.clrPixel(4, 1);
      matrix.clrPixel(4, 2);
      matrix.clrPixel(4, 3);
      matrix.clrPixel(4, 4);
      matrix.clrPixel(4, 5);

      matrix.clrPixel(3, 1);
      matrix.clrPixel(3, 2);
      matrix.clrPixel(3, 3);
      matrix.clrPixel(3, 4);
      matrix.clrPixel(3, 5);

      matrix.clrPixel(2, 1);
      matrix.clrPixel(2, 2);
      matrix.clrPixel(2, 3);
      matrix.clrPixel(2, 4);
      matrix.clrPixel(2, 5);

      matrix.clrPixel(1, 1);
      matrix.clrPixel(1, 2);
      matrix.clrPixel(1, 3);
      matrix.clrPixel(1, 4);
      matrix.clrPixel(1, 5);

      matrix.setPixel(0, 1);
      matrix.setPixel(0, 2);
      matrix.setPixel(0, 3);
      matrix.setPixel(0, 4);
      matrix.setPixel(0, 5);
    }

    oldRingLast = ringLast;
    matrix.writeScreen();
  }




  //    ----  P&T ----

  if (oldxDisplay != xDisplay || oldyDisplay != yDisplay) {

    for (uint8_t y = 0; y < 7; y++) {
      for (uint8_t x = 100; x < 105; x++) {
        matrix.clrPixel(x, y);
      }
    }
    matrix.setPixel((xDisplay + 100), yDisplay);

    oldxDisplay = xDisplay;
    oldyDisplay = yDisplay;
    matrix.writeScreen();
  }




  //    ----  Pan Tilt Speed  ----

  if (oldcam1PTSpeed != cam1PTSpeed) {
    if (cam1PTSpeed == 7) {
      matrix.setPixel(90, 0);
      matrix.setPixel(90, 1);
      matrix.setPixel(90, 2);
      matrix.setPixel(90, 3);
      matrix.setPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 6) {
      matrix.clrPixel(90, 0);
      matrix.setPixel(90, 1);
      matrix.setPixel(90, 2);
      matrix.setPixel(90, 3);
      matrix.setPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 5) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.setPixel(90, 2);
      matrix.setPixel(90, 3);
      matrix.setPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 4) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.clrPixel(90, 2);
      matrix.setPixel(90, 3);
      matrix.setPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 3) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.clrPixel(90, 2);
      matrix.clrPixel(90, 3);
      matrix.setPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 2) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.clrPixel(90, 2);
      matrix.clrPixel(90, 3);
      matrix.clrPixel(90, 4);
      matrix.setPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 1) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.clrPixel(90, 2);
      matrix.clrPixel(90, 3);
      matrix.clrPixel(90, 4);
      matrix.clrPixel(90, 5);
      matrix.setPixel(90, 6);
    }
    else if (cam1PTSpeed == 0) {
      matrix.clrPixel(90, 0);
      matrix.clrPixel(90, 1);
      matrix.clrPixel(90, 2);
      matrix.clrPixel(90, 3);
      matrix.clrPixel(90, 4);
      matrix.clrPixel(90, 5);
      matrix.clrPixel(90, 6);
    }
    
    //Serial.print("=1");
    //Serial.println(cam1PTSpeed);
    
    oldcam1PTSpeed = cam1PTSpeed;
    matrix.writeScreen();
  }

  if (oldcam2PTSpeed != cam2PTSpeed) {
    if (cam2PTSpeed == 7) {
      matrix.setPixel(92, 0);
      matrix.setPixel(92, 1);
      matrix.setPixel(92, 2);
      matrix.setPixel(92, 3);
      matrix.setPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 6) {
      matrix.clrPixel(92, 0);
      matrix.setPixel(92, 1);
      matrix.setPixel(92, 2);
      matrix.setPixel(92, 3);
      matrix.setPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 5) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.setPixel(92, 2);
      matrix.setPixel(92, 3);
      matrix.setPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 4) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.clrPixel(92, 2);
      matrix.setPixel(92, 3);
      matrix.setPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 3) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.clrPixel(92, 2);
      matrix.clrPixel(92, 3);
      matrix.setPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 2) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.clrPixel(92, 2);
      matrix.clrPixel(92, 3);
      matrix.clrPixel(92, 4);
      matrix.setPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 1) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.clrPixel(92, 2);
      matrix.clrPixel(92, 3);
      matrix.clrPixel(92, 4);
      matrix.clrPixel(92, 5);
      matrix.setPixel(92, 6);
    }
    else if (cam2PTSpeed == 0) {
      matrix.clrPixel(92, 0);
      matrix.clrPixel(92, 1);
      matrix.clrPixel(92, 2);
      matrix.clrPixel(92, 3);
      matrix.clrPixel(92, 4);
      matrix.clrPixel(92, 5);
      matrix.clrPixel(92, 6);
    }
    
    //Serial.print("=2");
    //Serial.println(cam2PTSpeed);

    oldcam2PTSpeed = cam2PTSpeed;
    matrix.writeScreen();
  }

  if (oldcam3PTSpeed != cam3PTSpeed) {
    if (cam3PTSpeed == 7) {
      matrix.setPixel(94, 0);
      matrix.setPixel(94, 1);
      matrix.setPixel(94, 2);
      matrix.setPixel(94, 3);
      matrix.setPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 6) {
      matrix.clrPixel(94, 0);
      matrix.setPixel(94, 1);
      matrix.setPixel(94, 2);
      matrix.setPixel(94, 3);
      matrix.setPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 5) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.setPixel(94, 2);
      matrix.setPixel(94, 3);
      matrix.setPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 4) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.clrPixel(94, 2);
      matrix.setPixel(94, 3);
      matrix.setPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 3) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.clrPixel(94, 2);
      matrix.clrPixel(94, 3);
      matrix.setPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 2) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.clrPixel(94, 2);
      matrix.clrPixel(94, 3);
      matrix.clrPixel(94, 4);
      matrix.setPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 1) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.clrPixel(94, 2);
      matrix.clrPixel(94, 3);
      matrix.clrPixel(94, 4);
      matrix.clrPixel(94, 5);
      matrix.setPixel(94, 6);
    }
    else if (cam3PTSpeed == 0) {
      matrix.clrPixel(94, 0);
      matrix.clrPixel(94, 1);
      matrix.clrPixel(94, 2);
      matrix.clrPixel(94, 3);
      matrix.clrPixel(94, 4);
      matrix.clrPixel(94, 5);
      matrix.clrPixel(94, 6);
    }
    
    //Serial.print("=3");
    //Serial.println(cam3PTSpeed);

    oldcam3PTSpeed = cam3PTSpeed;
    matrix.writeScreen();
  }




  //    ----  Slider Speed  ----

  if (olds1Speed != s1Speed) {
    if (s1Speed == 7) {
      matrix.setPixel(10, 0);
      matrix.setPixel(10, 1);
      matrix.setPixel(10, 2);
      matrix.setPixel(10, 3);
      matrix.setPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 6) {
      matrix.clrPixel(10, 0);
      matrix.setPixel(10, 1);
      matrix.setPixel(10, 2);
      matrix.setPixel(10, 3);
      matrix.setPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 5) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.setPixel(10, 2);
      matrix.setPixel(10, 3);
      matrix.setPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 4) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.clrPixel(10, 2);
      matrix.setPixel(10, 3);
      matrix.setPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 3) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.clrPixel(10, 2);
      matrix.clrPixel(10, 3);
      matrix.setPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 2) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.clrPixel(10, 2);
      matrix.clrPixel(10, 3);
      matrix.clrPixel(10, 4);
      matrix.setPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 1) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.clrPixel(10, 2);
      matrix.clrPixel(10, 3);
      matrix.clrPixel(10, 4);
      matrix.clrPixel(10, 5);
      matrix.setPixel(10, 6);
    }
    else if (s1Speed == 0) {
      matrix.clrPixel(10, 0);
      matrix.clrPixel(10, 1);
      matrix.clrPixel(10, 2);
      matrix.clrPixel(10, 3);
      matrix.clrPixel(10, 4);
      matrix.clrPixel(10, 5);
      matrix.clrPixel(10, 6);
    }
    
    //Serial.print("=1");
    //Serial.println(s1Speed);
    
    olds1Speed = s1Speed;
    matrix.writeScreen();
  }

  if (olds2Speed != s2Speed) {
    if (s2Speed == 7) {
      matrix.setPixel(12, 0);
      matrix.setPixel(12, 1);
      matrix.setPixel(12, 2);
      matrix.setPixel(12, 3);
      matrix.setPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 6) {
      matrix.clrPixel(12, 0);
      matrix.setPixel(12, 1);
      matrix.setPixel(12, 2);
      matrix.setPixel(12, 3);
      matrix.setPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 5) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.setPixel(12, 2);
      matrix.setPixel(12, 3);
      matrix.setPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 4) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.clrPixel(12, 2);
      matrix.setPixel(12, 3);
      matrix.setPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 3) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.clrPixel(12, 2);
      matrix.clrPixel(12, 3);
      matrix.setPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 2) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.clrPixel(12, 2);
      matrix.clrPixel(12, 3);
      matrix.clrPixel(12, 4);
      matrix.setPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 1) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.clrPixel(12, 2);
      matrix.clrPixel(12, 3);
      matrix.clrPixel(12, 4);
      matrix.clrPixel(12, 5);
      matrix.setPixel(12, 6);
    }
    else if (s2Speed == 0) {
      matrix.clrPixel(12, 0);
      matrix.clrPixel(12, 1);
      matrix.clrPixel(12, 2);
      matrix.clrPixel(12, 3);
      matrix.clrPixel(12, 4);
      matrix.clrPixel(12, 5);
      matrix.clrPixel(12, 6);
    }
    
    //Serial.print("=2");
    //Serial.println(s2Speed);

    olds2Speed = s2Speed;
    matrix.writeScreen();
  }

  if (olds3Speed != s3Speed) {
    if (s3Speed == 7) {
      matrix.setPixel(14, 0);
      matrix.setPixel(14, 1);
      matrix.setPixel(14, 2);
      matrix.setPixel(14, 3);
      matrix.setPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 6) {
      matrix.clrPixel(14, 0);
      matrix.setPixel(14, 1);
      matrix.setPixel(14, 2);
      matrix.setPixel(14, 3);
      matrix.setPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 5) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.setPixel(14, 2);
      matrix.setPixel(14, 3);
      matrix.setPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 4) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.clrPixel(14, 2);
      matrix.setPixel(14, 3);
      matrix.setPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 3) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.clrPixel(14, 2);
      matrix.clrPixel(14, 3);
      matrix.setPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 2) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.clrPixel(14, 2);
      matrix.clrPixel(14, 3);
      matrix.clrPixel(14, 4);
      matrix.setPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 1) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.clrPixel(14, 2);
      matrix.clrPixel(14, 3);
      matrix.clrPixel(14, 4);
      matrix.clrPixel(14, 5);
      matrix.setPixel(14, 6);
    }
    else if (s3Speed == 0) {
      matrix.clrPixel(14, 0);
      matrix.clrPixel(14, 1);
      matrix.clrPixel(14, 2);
      matrix.clrPixel(14, 3);
      matrix.clrPixel(14, 4);
      matrix.clrPixel(14, 5);
      matrix.clrPixel(14, 6);
    }
    
    //Serial.print("=3");
    //Serial.println(s3Speed);

    olds3Speed = s3Speed;
    matrix.writeScreen();
  }



  //    ----  TEXT  ----

  if (oldDisplayCommand != displayCommand) {
    for (uint8_t y = 0; y < 7; y++) {
      for (uint8_t x = 55; x < 90; x++) {
        matrix.clrPixel(x, y);
      }
    }

    if (displayCommand == 111) {                      //  Cam 1 At pos 1 command 1
      textDisplay((char *)"C1+P1");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 121) {                 //  Cam 1 At pos 2 ...
      textDisplay((char *)"C1+P2");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 131) {                 //  Cam 1 At pos 3 ...
      textDisplay((char *)"C1+P3");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 141) {
      textDisplay((char *)"C1+P4");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 151) {
      textDisplay((char *)"C1+P5");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 161) {
      textDisplay((char *)"C1+P6");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 112) {                //  Cam 1 Move to pos 1 ...
      textDisplay((char *)"C1>P1");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 122) {
      textDisplay((char *)"C1>P2");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 132) {
      textDisplay((char *)"C1>P3");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 142) {
      textDisplay((char *)"C1>P4");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 152) {
      textDisplay((char *)"C1>P5");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 162) {
      textDisplay((char *)"C1>P6");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 113) {
      textDisplay((char *)"C1@P1");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 123) {
      textDisplay((char *)"C1@P2");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 133) {
      textDisplay((char *)"C1@P3");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 143) {
      textDisplay((char *)"C1@P4");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 153) {
      textDisplay((char *)"C1@P5");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 163) {
      textDisplay((char *)"C1@P6");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 100) {
      textDisplay((char *)"Clear");
      startDisplayRefresh = true;
      cam1PosUpdate = true;
    }
    else if (displayCommand == 114) {
      textDisplay((char *)"StopRec");
      startDisplayRefresh = true;
      digitalWrite(LEDaR, HIGH);
      setLEDs();
    }
    else if (displayCommand == 124) {
      textDisplay((char *)"Rec.");
      startDisplayRefresh = true;
      digitalWrite(LEDaR, LOW);
      setLEDs();
    }
    else if (displayCommand == 115) {
      char a[24] = "Z+ ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    else if (displayCommand == 125) {
      char a[24] = "Z- ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    //  *******************************************************************************************
    else if (displayCommand == 211) {                 //  Cam 2 At pos 1 command 1
      textDisplay((char *)"C2+P1");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 221) {                 //  Cam 2 At pos 2 ...
      textDisplay((char *)"C2+P2");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 231) {                 //  Cam 2 At pos 3 ...
      textDisplay((char *)"C2+P3");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 241) {
      textDisplay((char *)"C2+P4");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 251) {
      textDisplay((char *)"C2+P5");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 261) {
      textDisplay((char *)"C2+P6");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 212) {                //  Cam 2 Move to pos 1 ...
      textDisplay((char *)"C2>P1");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 222) {
      textDisplay((char *)"C2>P2");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 232) {
      textDisplay((char *)"C2>P3");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 242) {
      textDisplay((char *)"C2>P4");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 252) {
      textDisplay((char *)"C2>P5");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 262) {
      textDisplay((char *)"C2>P6");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 213) {
      textDisplay((char *)"C2@P1");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 223) {
      textDisplay((char *)"C2@P2");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 233) {
      textDisplay((char *)"C2@P3");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 243) {
      textDisplay((char *)"C2@P4");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 253) {
      textDisplay((char *)"C2@P5");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 263) {
      textDisplay((char *)"C2@P6");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 200) {
      textDisplay((char *)"Clear");
      startDisplayRefresh = true;
      cam2PosUpdate = true;
    }
    else if (displayCommand == 214) {
      textDisplay((char *)"StopRec");
      startDisplayRefresh = true;
      digitalWrite(LEDbR, HIGH);
      setLEDs();
    }
    else if (displayCommand == 224) {
      textDisplay((char *)"Rec.");
      startDisplayRefresh = true;
      digitalWrite(LEDbR, LOW);
      setLEDs();
    }
    else if (displayCommand == 215) {
      char a[24] = "Z+ ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    else if (displayCommand == 225) {
      char a[24] = "Z- ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    //  *******************************************************************************************
    else if (displayCommand == 311) {                 //  Cam 3 At pos 1 command 1
      textDisplay((char *)"C3+P1");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 321) {                 //  Cam 3 At pos 2 ...
      textDisplay((char *)"C3+P2");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 331) {                 //  Cam 3 At pos 3 ...
      textDisplay((char *)"C3+P3");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 341) {
      textDisplay((char *)"C3+P4");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 351) {
      textDisplay((char *)"C3+P5");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 361) {
      textDisplay((char *)"C3+P6");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 312) {                //  Cam 3 Move to pos 1 ...
      textDisplay((char *)"C3>P1");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 322) {
      textDisplay((char *)"C3>P2");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 332) {
      textDisplay((char *)"C3>P3");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 342) {
      textDisplay((char *)"C3>P4");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 352) {
      textDisplay((char *)"C3>P5");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 362) {
      textDisplay((char *)"C3>P6");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 313) {
      textDisplay((char *)"C3@P1");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 323) {
      textDisplay((char *)"C3@P2");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 333) {
      textDisplay((char *)"C3@P3");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 343) {
      textDisplay((char *)"C3@P4");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 353) {
      textDisplay((char *)"C3@P5");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 363) {
      textDisplay((char *)"C3@P6");
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 300) {
      if (whichCam == 1) {
        textDisplay((char *)"1Clear");
      }
      else if (whichCam == 2) {
        textDisplay((char *)"2Clear");
      }
      else if (whichCam == 3) {
        textDisplay((char *)"3Clear");
      }
      startDisplayRefresh = true;
      cam3PosUpdate = true;
    }
    else if (displayCommand == 314) {
      textDisplay((char *)"StopRec");
      startDisplayRefresh = true;
      digitalWrite(LEDcR, HIGH);
      setLEDs();
    }
    else if (displayCommand == 324) {
      textDisplay((char *)"Rec.");
      startDisplayRefresh = true;
      digitalWrite(LEDcR, LOW);
      setLEDs();
    }
    else if (displayCommand == 315) {
      char a[24] = "Z+ ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    else if (displayCommand == 325) {
      char a[24] = "Z- ";
      char tmp[6];
      textDisplay((char *)(strcat(a, itoa(zoom_speed, tmp, 10))));
      startDisplayRefresh = true;
      setLEDs();
    }
    else if (displayCommand == 001) {
      textDisplay((char *)"DefSpd");
      startDisplayRefresh = true;
    }

    oldDisplayCommand = displayCommand;
    matrix.writeScreen();
    
    Serial.print("~");
    Serial.println(displayCommand);
  }

  if (cam1pos1set != oldcam1pos1set || cam1pos1run != oldcam1pos1run || cam1atPos1 != oldcam1atPos1 || (cam1pos1run == true && runTick1 != oldRunTick1)) {
    if (cam1pos1set && !cam1pos1run && !cam1atPos1) {             //  cam1 - set
      matrix.clrPixel(15, 0);
      matrix.clrPixel(16, 0);
      matrix.setPixel(17, 0);
      matrix.clrPixel(18, 0);
      matrix.clrPixel(19, 0);
      oldcam1pos1set = cam1pos1set;
      oldcam1pos1run = cam1pos1run;
      oldcam1atPos1 = cam1atPos1;
    }
    else if (cam1pos1set && cam1pos1run && !cam1atPos1 && runTick1) {         //  cam1 - set & running
      matrix.setPixel(15, 0);
      matrix.clrPixel(16, 0);
      matrix.setPixel(17, 0);
      matrix.clrPixel(18, 0);
      matrix.setPixel(19, 0);
      oldcam1pos1set = cam1pos1set;
      oldcam1pos1run = cam1pos1run;
      oldcam1atPos1 = cam1atPos1;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos1set && cam1pos1run && !cam1atPos1 && !runTick1) {         //  cam1 - set & running
      matrix.clrPixel(15, 0);
      matrix.setPixel(16, 0);
      matrix.clrPixel(17, 0);
      matrix.setPixel(18, 0);
      matrix.clrPixel(19, 0);
      oldcam1pos1set = cam1pos1set;
      oldcam1pos1run = cam1pos1run;
      oldcam1atPos1 = cam1atPos1;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos1set && !cam1pos1run && cam1atPos1) {         //  cam1 - set & at pos
      matrix.setPixel(15, 0);
      matrix.setPixel(16, 0);
      matrix.setPixel(17, 0);
      matrix.setPixel(18, 0);
      matrix.setPixel(19, 0);
      oldcam1pos1set = cam1pos1set;
      oldcam1pos1run = cam1pos1run;
      oldcam1atPos1 = cam1atPos1;
    }
    else if (!cam1pos1set) {                                      //  cam1 - clear
      matrix.clrPixel(15, 0);
      matrix.clrPixel(16, 0);
      matrix.clrPixel(17, 0);
      matrix.clrPixel(18, 0);
      matrix.clrPixel(19, 0);
      oldcam1pos1set = cam1pos1set;
    }
    matrix.writeScreen();
  }



  if (cam1pos2set != oldcam1pos2set || cam1pos2run != oldcam1pos2run || cam1atPos2 != oldcam1atPos2 || (cam1pos2run == true && runTick1 != oldRunTick1)) {
    if (cam1pos2set && !cam1pos2run && !cam1atPos2) {
      matrix.clrPixel(23, 0);
      matrix.clrPixel(24, 0);
      matrix.setPixel(25, 0);
      matrix.clrPixel(26, 0);
      matrix.clrPixel(27, 0);
      oldcam1pos2set = cam1pos2set;
      oldcam1pos2run = cam1pos2run;
      oldcam1atPos2 = cam1atPos2;
    }
    else if (cam1pos2set && cam1pos2run && !cam1atPos2 && runTick1) {
      matrix.setPixel(23, 0);
      matrix.clrPixel(24, 0);
      matrix.setPixel(25, 0);
      matrix.clrPixel(26, 0);
      matrix.setPixel(27, 0);
      oldcam1pos2set = cam1pos2set;
      oldcam1pos2run = cam1pos2run;
      oldcam1atPos2 = cam1atPos2;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos2set && cam1pos2run && !cam1atPos2 && !runTick1) {
      matrix.clrPixel(23, 0);
      matrix.setPixel(24, 0);
      matrix.clrPixel(25, 0);
      matrix.setPixel(26, 0);
      matrix.clrPixel(27, 0);
      oldcam1pos2set = cam1pos2set;
      oldcam1pos2run = cam1pos2run;
      oldcam1atPos2 = cam1atPos2;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos2set && !cam1pos2run && cam1atPos2) {
      matrix.setPixel(23, 0);
      matrix.setPixel(24, 0);
      matrix.setPixel(25, 0);
      matrix.setPixel(26, 0);
      matrix.setPixel(27, 0);
      oldcam1pos2set = cam1pos2set;
      oldcam1pos2run = cam1pos2run;
      oldcam1atPos2 = cam1atPos2;
    }
    else if (!cam1pos2set) {
      matrix.clrPixel(23, 0);
      matrix.clrPixel(24, 0);
      matrix.clrPixel(25, 0);
      matrix.clrPixel(26, 0);
      matrix.clrPixel(27, 0);
      oldcam1pos2set = cam1pos2set;
    }
    matrix.writeScreen();
  }


  if (cam1pos3set != oldcam1pos3set || cam1pos3run != oldcam1pos3run || cam1atPos3 != oldcam1atPos3 || (cam1pos3run == true && runTick1 != oldRunTick1)) {
    if (cam1pos3set && !cam1pos3run && !cam1atPos3) {
      matrix.clrPixel(30, 0);
      matrix.clrPixel(31, 0);
      matrix.setPixel(32, 0);
      matrix.clrPixel(33, 0);
      matrix.clrPixel(34, 0);
      oldcam1pos3set = cam1pos3set;
      oldcam1pos3run = cam1pos3run;
      oldcam1atPos3 = cam1atPos3;
    }
    else if (cam1pos3set && cam1pos3run && !cam1atPos3 && runTick1) {
      matrix.setPixel(30, 0);
      matrix.clrPixel(31, 0);
      matrix.setPixel(32, 0);
      matrix.clrPixel(33, 0);
      matrix.setPixel(34, 0);
      oldcam1pos3set = cam1pos3set;
      oldcam1pos3run = cam1pos3run;
      oldcam1atPos3 = cam1atPos3;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos3set && cam1pos3run && !cam1atPos3 && !runTick1) {
      matrix.clrPixel(30, 0);
      matrix.setPixel(31, 0);
      matrix.clrPixel(32, 0);
      matrix.setPixel(33, 0);
      matrix.clrPixel(34, 0);
      oldcam1pos3set = cam1pos3set;
      oldcam1pos3run = cam1pos3run;
      oldcam1atPos3 = cam1atPos3;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos3set && !cam1pos3run && cam1atPos3) {
      matrix.setPixel(30, 0);
      matrix.setPixel(31, 0);
      matrix.setPixel(32, 0);
      matrix.setPixel(33, 0);
      matrix.setPixel(34, 0);
      oldcam1pos3set = cam1pos3set;
      oldcam1pos3run = cam1pos3run;
      oldcam1atPos3 = cam1atPos3;
    }
    else if (!cam1pos3set) {
      matrix.clrPixel(30, 0);
      matrix.clrPixel(31, 0);
      matrix.clrPixel(32, 0);
      matrix.clrPixel(33, 0);
      matrix.clrPixel(34, 0);
      oldcam1pos3set = cam1pos3set;
    }
    matrix.writeScreen();
  }


  if (cam1pos4set != oldcam1pos4set || cam1pos4run != oldcam1pos4run || cam1atPos4 != oldcam1atPos4 || (cam1pos4run == true && runTick1 != oldRunTick1)) {
    if (cam1pos4set && !cam1pos4run && !cam1atPos4) {
      matrix.clrPixel(37, 0);
      matrix.clrPixel(38, 0);
      matrix.setPixel(39, 0);
      matrix.clrPixel(40, 0);
      matrix.clrPixel(41, 0);
      oldcam1pos4set = cam1pos4set;
      oldcam1pos4run = cam1pos4run;
      oldcam1atPos4 = cam1atPos4;
    }
    else if (cam1pos4set && cam1pos4run && !cam1atPos4 && runTick1) {
      matrix.setPixel(37, 0);
      matrix.clrPixel(38, 0);
      matrix.setPixel(39, 0);
      matrix.clrPixel(40, 0);
      matrix.setPixel(41, 0);
      oldcam1pos4set = cam1pos4set;
      oldcam1pos4run = cam1pos4run;
      oldcam1atPos4 = cam1atPos4;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos4set && cam1pos4run && !cam1atPos4 && !runTick1) {
      matrix.clrPixel(37, 0);
      matrix.setPixel(38, 0);
      matrix.clrPixel(39, 0);
      matrix.setPixel(40, 0);
      matrix.clrPixel(41, 0);
      oldcam1pos4set = cam1pos4set;
      oldcam1pos4run = cam1pos4run;
      oldcam1atPos4 = cam1atPos4;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos4set && !cam1pos4run && cam1atPos4) {
      matrix.setPixel(37, 0);
      matrix.setPixel(38, 0);
      matrix.setPixel(39, 0);
      matrix.setPixel(40, 0);
      matrix.setPixel(41, 0);
      oldcam1pos4set = cam1pos4set;
      oldcam1pos4run = cam1pos4run;
      oldcam1atPos4 = cam1atPos4;
    }
    else if (!cam1pos4set) {
      matrix.clrPixel(37, 0);
      matrix.clrPixel(38, 0);
      matrix.clrPixel(39, 0);
      matrix.clrPixel(40, 0);
      matrix.clrPixel(41, 0);
      oldcam1pos4set = cam1pos4set;
    }
    matrix.writeScreen();
  }


  if (cam1pos5set != oldcam1pos5set || cam1pos5run != oldcam1pos5run || cam1atPos5 != oldcam1atPos5 || (cam1pos5run == true && runTick1 != oldRunTick1)) {
    if (cam1pos5set && !cam1pos5run && !cam1atPos5) {
      matrix.clrPixel(43, 0);
      matrix.clrPixel(44, 0);
      matrix.setPixel(45, 0);
      matrix.clrPixel(46, 0);
      matrix.clrPixel(47, 0);
      oldcam1pos5set = cam1pos5set;
      oldcam1pos5run = cam1pos5run;
      oldcam1atPos5 = cam1atPos5;
    }
    else if (cam1pos5set && cam1pos5run && !cam1atPos5 && runTick1) {
      matrix.setPixel(43, 0);
      matrix.clrPixel(44, 0);
      matrix.setPixel(45, 0);
      matrix.clrPixel(46, 0);
      matrix.setPixel(47, 0);
      oldcam1pos5set = cam1pos5set;
      oldcam1pos5run = cam1pos5run;
      oldcam1atPos5 = cam1atPos5;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos5set && cam1pos5run && !cam1atPos5 && !runTick1) {
      matrix.clrPixel(43, 0);
      matrix.setPixel(44, 0);
      matrix.clrPixel(45, 0);
      matrix.setPixel(46, 0);
      matrix.clrPixel(47, 0);
      oldcam1pos5set = cam1pos5set;
      oldcam1pos5run = cam1pos5run;
      oldcam1atPos5 = cam1atPos5;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos5set && !cam1pos5run && cam1atPos5) {
      matrix.setPixel(43, 0);
      matrix.setPixel(44, 0);
      matrix.setPixel(45, 0);
      matrix.setPixel(46, 0);
      matrix.setPixel(47, 0);
      oldcam1pos5set = cam1pos5set;
      oldcam1pos5run = cam1pos5run;
      oldcam1atPos5 = cam1atPos5;
    }
    else if (!cam1pos5set) {
      matrix.clrPixel(43, 0);
      matrix.clrPixel(44, 0);
      matrix.clrPixel(45, 0);
      matrix.clrPixel(46, 0);
      matrix.clrPixel(47, 0);
      oldcam1pos5set = cam1pos5set;
    }
    matrix.writeScreen();
  }


  if (cam1pos6set != oldcam1pos6set || cam1pos6run != oldcam1pos6run || cam1atPos6 != oldcam1atPos6 || (cam1pos6run == true && runTick1 != oldRunTick1)) {
    if (cam1pos6set && !cam1pos6run && !cam1atPos6) {
      matrix.clrPixel(50, 0);
      matrix.clrPixel(51, 0);
      matrix.setPixel(52, 0);
      matrix.clrPixel(53, 0);
      matrix.clrPixel(54, 0);
      oldcam1pos6set = cam1pos6set;
      oldcam1pos6run = cam1pos6run;
      oldcam1atPos6 = cam1atPos6;
    }
    else if (cam1pos6set && cam1pos6run && !cam1atPos6 && runTick1) {
      matrix.setPixel(50, 0);
      matrix.clrPixel(51, 0);
      matrix.setPixel(52, 0);
      matrix.clrPixel(53, 0);
      matrix.setPixel(54, 0);
      oldcam1pos6set = cam1pos6set;
      oldcam1pos6run = cam1pos6run;
      oldcam1atPos6 = cam1atPos6;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos6set && cam1pos6run && !cam1atPos6 && !runTick1) {
      matrix.clrPixel(50, 0);
      matrix.setPixel(51, 0);
      matrix.clrPixel(52, 0);
      matrix.setPixel(53, 0);
      matrix.clrPixel(54, 0);
      oldcam1pos6set = cam1pos6set;
      oldcam1pos6run = cam1pos6run;
      oldcam1atPos6 = cam1atPos6;
      oldRunTick1 = runTick1;
    }
    else if (cam1pos6set && !cam1pos6run && cam1atPos6) {
      matrix.setPixel(50, 0);
      matrix.setPixel(51, 0);
      matrix.setPixel(52, 0);
      matrix.setPixel(53, 0);
      matrix.setPixel(54, 0);
      oldcam1pos6set = cam1pos6set;
      oldcam1pos6run = cam1pos6run;
      oldcam1atPos6 = cam1atPos6;
    }
    else if (!cam1pos6set) {
      matrix.clrPixel(50, 0);
      matrix.clrPixel(51, 0);
      matrix.clrPixel(52, 0);
      matrix.clrPixel(53, 0);
      matrix.clrPixel(54, 0);
      oldcam1pos6set = cam1pos6set;
    }
    //cam1PosUpdate = false;
    //displayUpadte = false;
    matrix.writeScreen();
  }

  //  *******************************************************************************************
  //if (cam2PosUpdate) {
  if (cam2pos1set != oldcam2pos1set || cam2pos1run != oldcam2pos1run || cam2atPos1 != oldcam2atPos1 || (cam2pos1run == true && runTick2 != oldRunTick2)) {
    if (cam2pos1set && !cam2pos1run && !cam2atPos1) {             //  cam2 - set
      matrix.clrPixel(15, 3);
      matrix.clrPixel(16, 3);
      matrix.setPixel(17, 3);
      matrix.clrPixel(18, 3);
      matrix.clrPixel(19, 3);
      oldcam2pos1set = cam2pos1set;
      oldcam2pos1run = cam2pos1run;
      oldcam2atPos1 = cam2atPos1;
    }
    else if (cam2pos1set && cam2pos1run && !cam2atPos1 && runTick2) {         //  cam2 - set & running
      matrix.setPixel(15, 3);
      matrix.clrPixel(16, 3);
      matrix.setPixel(17, 3);
      matrix.clrPixel(18, 3);
      matrix.setPixel(19, 3);
      oldcam2pos1set = cam2pos1set;
      oldcam2pos1run = cam2pos1run;
      oldcam2atPos1 = cam2atPos1;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos1set && cam2pos1run && !cam2atPos1 && !runTick2) {         //  cam2 - set & running
      matrix.clrPixel(15, 3);
      matrix.setPixel(16, 3);
      matrix.clrPixel(17, 3);
      matrix.setPixel(18, 3);
      matrix.clrPixel(19, 3);
      oldcam2pos1set = cam2pos1set;
      oldcam2pos1run = cam2pos1run;
      oldcam2atPos1 = cam2atPos1;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos1set && !cam2pos1run && cam2atPos1) {         //  cam2 - set & at pos
      matrix.setPixel(15, 3);
      matrix.setPixel(16, 3);
      matrix.setPixel(17, 3);
      matrix.setPixel(18, 3);
      matrix.setPixel(19, 3);
      oldcam2pos1set = cam2pos1set;
      oldcam2pos1run = cam2pos1run;
      oldcam2atPos1 = cam2atPos1;
    }
    else if (!cam2pos1set) {                                      //  cam2 - clear
      matrix.clrPixel(15, 3);
      matrix.clrPixel(16, 3);
      matrix.clrPixel(17, 3);
      matrix.clrPixel(18, 3);
      matrix.clrPixel(19, 3);
      oldcam2pos1set = cam2pos1set;
    }
    matrix.writeScreen();
  }



  if (cam2pos2set != oldcam2pos2set || cam2pos2run != oldcam2pos2run || cam2atPos2 != oldcam2atPos2 || (cam2pos2run == true && runTick2 != oldRunTick2)) {
    if (cam2pos2set && !cam2pos2run && !cam2atPos2) {
      matrix.clrPixel(23, 3);
      matrix.clrPixel(24, 3);
      matrix.setPixel(25, 3);
      matrix.clrPixel(26, 3);
      matrix.clrPixel(27, 3);
      oldcam2pos2set = cam2pos2set;
      oldcam2pos2run = cam2pos2run;
      oldcam2atPos2 = cam2atPos2;
    }
    else if (cam2pos2set && cam2pos2run && !cam2atPos2 && runTick2) {
      matrix.setPixel(23, 3);
      matrix.clrPixel(24, 3);
      matrix.setPixel(25, 3);
      matrix.clrPixel(26, 3);
      matrix.setPixel(27, 3);
      oldcam2pos2set = cam2pos2set;
      oldcam2pos2run = cam2pos2run;
      oldcam2atPos2 = cam2atPos2;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos2set && cam2pos2run && !cam2atPos2 && !runTick2) {
      matrix.clrPixel(23, 3);
      matrix.setPixel(24, 3);
      matrix.clrPixel(25, 3);
      matrix.setPixel(26, 3);
      matrix.clrPixel(27, 3);
      oldcam2pos2set = cam2pos2set;
      oldcam2pos2run = cam2pos2run;
      oldcam2atPos2 = cam2atPos2;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos2set && !cam2pos2run && cam2atPos2) {
      matrix.setPixel(23, 3);
      matrix.setPixel(24, 3);
      matrix.setPixel(25, 3);
      matrix.setPixel(26, 3);
      matrix.setPixel(27, 3);
      oldcam2pos2set = cam2pos2set;
      oldcam2pos2run = cam2pos2run;
      oldcam2atPos2 = cam2atPos2;
    }
    else if (!cam2pos2set) {
      matrix.clrPixel(23, 3);
      matrix.clrPixel(24, 3);
      matrix.clrPixel(25, 3);
      matrix.clrPixel(26, 3);
      matrix.clrPixel(27, 3);
      oldcam2pos2set = cam2pos2set;
    }
    matrix.writeScreen();
  }


  if (cam2pos3set != oldcam2pos3set || cam2pos3run != oldcam2pos3run || cam2atPos3 != oldcam2atPos3 || (cam2pos3run == true && runTick2 != oldRunTick2)) {
    if (cam2pos3set && !cam2pos3run && !cam2atPos3) {
      matrix.clrPixel(30, 3);
      matrix.clrPixel(31, 3);
      matrix.setPixel(32, 3);
      matrix.clrPixel(33, 3);
      matrix.clrPixel(34, 3);
      oldcam2pos3set = cam2pos3set;
      oldcam2pos3run = cam2pos3run;
      oldcam2atPos3 = cam2atPos3;
    }
    else if (cam2pos3set && cam2pos3run && !cam2atPos3 && runTick2) {
      matrix.setPixel(30, 3);
      matrix.clrPixel(31, 3);
      matrix.setPixel(32, 3);
      matrix.clrPixel(33, 3);
      matrix.setPixel(34, 3);
      oldcam2pos3set = cam2pos3set;
      oldcam2pos3run = cam2pos3run;
      oldcam2atPos3 = cam2atPos3;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos3set && cam2pos3run && !cam2atPos3 && !runTick2) {
      matrix.clrPixel(30, 3);
      matrix.setPixel(31, 3);
      matrix.clrPixel(32, 3);
      matrix.setPixel(33, 3);
      matrix.clrPixel(34, 3);
      oldcam2pos3set = cam2pos3set;
      oldcam2pos3run = cam2pos3run;
      oldcam2atPos3 = cam2atPos3;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos3set && !cam2pos3run && cam2atPos3) {
      matrix.setPixel(30, 3);
      matrix.setPixel(31, 3);
      matrix.setPixel(32, 3);
      matrix.setPixel(33, 3);
      matrix.setPixel(34, 3);
      oldcam2pos3set = cam2pos3set;
      oldcam2pos3run = cam2pos3run;
      oldcam2atPos3 = cam2atPos3;
    }
    else if (!cam2pos3set) {
      matrix.clrPixel(30, 3);
      matrix.clrPixel(31, 3);
      matrix.clrPixel(32, 3);
      matrix.clrPixel(33, 3);
      matrix.clrPixel(34, 3);
      oldcam2pos3set = cam2pos3set;
    }
    matrix.writeScreen();
  }


  if (cam2pos4set != oldcam2pos4set || cam2pos4run != oldcam2pos4run || cam2atPos4 != oldcam2atPos4 || (cam2pos4run == true && runTick2 != oldRunTick2)) {
    if (cam2pos4set && !cam2pos4run && !cam2atPos4) {
      matrix.clrPixel(37, 3);
      matrix.clrPixel(38, 3);
      matrix.setPixel(39, 3);
      matrix.clrPixel(40, 3);
      matrix.clrPixel(41, 3);
      oldcam2pos4set = cam2pos4set;
      oldcam2pos4run = cam2pos4run;
      oldcam2atPos4 = cam2atPos4;
    }
    else if (cam2pos4set && cam2pos4run && !cam2atPos4 && runTick2) {
      matrix.setPixel(37, 3);
      matrix.clrPixel(38, 3);
      matrix.setPixel(39, 3);
      matrix.clrPixel(40, 3);
      matrix.setPixel(41, 3);
      oldcam2pos4set = cam2pos4set;
      oldcam2pos4run = cam2pos4run;
      oldcam2atPos4 = cam2atPos4;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos4set && cam2pos4run && !cam2atPos4 && !runTick2) {
      matrix.clrPixel(37, 3);
      matrix.setPixel(38, 3);
      matrix.clrPixel(39, 3);
      matrix.setPixel(40, 3);
      matrix.clrPixel(41, 3);
      oldcam2pos4set = cam2pos4set;
      oldcam2pos4run = cam2pos4run;
      oldcam2atPos4 = cam2atPos4;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos4set && !cam2pos4run && cam2atPos4) {
      matrix.setPixel(37, 3);
      matrix.setPixel(38, 3);
      matrix.setPixel(39, 3);
      matrix.setPixel(40, 3);
      matrix.setPixel(41, 3);
      oldcam2pos4set = cam2pos4set;
      oldcam2pos4run = cam2pos4run;
      oldcam2atPos4 = cam2atPos4;
    }
    else if (!cam2pos4set) {
      matrix.clrPixel(37, 3);
      matrix.clrPixel(38, 3);
      matrix.clrPixel(39, 3);
      matrix.clrPixel(40, 3);
      matrix.clrPixel(41, 3);
      oldcam2pos4set = cam2pos4set;
    }
    matrix.writeScreen();
  }


  if (cam2pos5set != oldcam2pos5set || cam2pos5run != oldcam2pos5run || cam2atPos5 != oldcam2atPos5 || (cam2pos5run == true && runTick2 != oldRunTick2)) {
    if (cam2pos5set && !cam2pos5run && !cam2atPos5) {
      matrix.clrPixel(43, 3);
      matrix.clrPixel(44, 3);
      matrix.setPixel(45, 3);
      matrix.clrPixel(46, 3);
      matrix.clrPixel(47, 3);
      oldcam2pos5set = cam2pos5set;
      oldcam2pos5run = cam2pos5run;
      oldcam2atPos5 = cam2atPos5;
    }
    else if (cam2pos5set && cam2pos5run && !cam2atPos5 && runTick2) {
      matrix.setPixel(43, 3);
      matrix.clrPixel(44, 3);
      matrix.setPixel(45, 3);
      matrix.clrPixel(46, 3);
      matrix.setPixel(47, 3);
      oldcam2pos5set = cam2pos5set;
      oldcam2pos5run = cam2pos5run;
      oldcam2atPos5 = cam2atPos5;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos5set && cam2pos5run && !cam2atPos5 && !runTick2) {
      matrix.clrPixel(43, 3);
      matrix.setPixel(44, 3);
      matrix.clrPixel(45, 3);
      matrix.setPixel(46, 3);
      matrix.clrPixel(47, 3);
      oldcam2pos5set = cam2pos5set;
      oldcam2pos5run = cam2pos5run;
      oldcam2atPos5 = cam2atPos5;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos5set && !cam2pos5run && cam2atPos5) {
      matrix.setPixel(43, 3);
      matrix.setPixel(44, 3);
      matrix.setPixel(45, 3);
      matrix.setPixel(46, 3);
      matrix.setPixel(47, 3);
      oldcam2pos5set = cam2pos5set;
      oldcam2pos5run = cam2pos5run;
      oldcam2atPos5 = cam2atPos5;
    }
    else if (!cam2pos5set) {
      matrix.clrPixel(43, 3);
      matrix.clrPixel(44, 3);
      matrix.clrPixel(45, 3);
      matrix.clrPixel(46, 3);
      matrix.clrPixel(47, 3);
      oldcam2pos5set = cam2pos5set;
    }
    matrix.writeScreen();
  }


  if (cam2pos6set != oldcam2pos6set || cam2pos6run != oldcam2pos6run || cam2atPos6 != oldcam2atPos6 || (cam2pos6run == true && runTick2 != oldRunTick2)) {
    if (cam2pos6set && !cam2pos6run && !cam2atPos6) {
      matrix.clrPixel(50, 3);
      matrix.clrPixel(51, 3);
      matrix.setPixel(52, 3);
      matrix.clrPixel(53, 3);
      matrix.clrPixel(54, 3);
      oldcam2pos6set = cam2pos6set;
      oldcam2pos6run = cam2pos6run;
      oldcam2atPos6 = cam2atPos6;
    }
    else if (cam2pos6set && cam2pos6run && !cam2atPos6 && runTick2) {
      matrix.setPixel(50, 3);
      matrix.clrPixel(51, 3);
      matrix.setPixel(52, 3);
      matrix.clrPixel(53, 3);
      matrix.setPixel(54, 3);
      oldcam2pos6set = cam2pos6set;
      oldcam2pos6run = cam2pos6run;
      oldcam2atPos6 = cam2atPos6;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos6set && cam2pos6run && !cam2atPos6 && !runTick2) {
      matrix.clrPixel(50, 3);
      matrix.setPixel(51, 3);
      matrix.clrPixel(52, 3);
      matrix.setPixel(53, 3);
      matrix.clrPixel(54, 3);
      oldcam2pos6set = cam2pos6set;
      oldcam2pos6run = cam2pos6run;
      oldcam2atPos6 = cam2atPos6;
      oldRunTick2 = runTick2;
    }
    else if (cam2pos6set && !cam2pos6run && cam2atPos6) {
      matrix.setPixel(50, 3);
      matrix.setPixel(51, 3);
      matrix.setPixel(52, 3);
      matrix.setPixel(53, 3);
      matrix.setPixel(54, 3);
      oldcam2pos6set = cam2pos6set;
      oldcam2pos6run = cam2pos6run;
      oldcam2atPos6 = cam2atPos6;
    }
    else if (!cam2pos6set) {
      matrix.clrPixel(50, 3);
      matrix.clrPixel(51, 3);
      matrix.clrPixel(52, 3);
      matrix.clrPixel(53, 3);
      matrix.clrPixel(54, 3);
      oldcam2pos6set = cam2pos6set;
    }
    //cam2PosUpdate = false;
    //displayUpadte = false;
    matrix.writeScreen();
  }

  if (cam3pos1set != oldcam3pos1set || cam3pos1run != oldcam3pos1run || cam3atPos1 != oldcam3atPos1 || (cam3pos1run == true && runTick3 != oldRunTick3)) {
    if (cam3pos1set && !cam3pos1run && !cam3atPos1) {             //  cam3 - set
      matrix.clrPixel(15, 6);
      matrix.clrPixel(16, 6);
      matrix.setPixel(17, 6);
      matrix.clrPixel(18, 6);
      matrix.clrPixel(19, 6);
      oldcam3pos1set = cam3pos1set;
      oldcam3pos1run = cam3pos1run;
      oldcam3atPos1 = cam3atPos1;
    }
    else if (cam3pos1set && cam3pos1run && !cam3atPos1 && runTick3) {         //  cam3 - set & running
      matrix.setPixel(15, 6);
      matrix.clrPixel(16, 6);
      matrix.setPixel(17, 6);
      matrix.clrPixel(18, 6);
      matrix.setPixel(19, 6);
      oldcam3pos1set = cam3pos1set;
      oldcam3pos1run = cam3pos1run;
      oldcam3atPos1 = cam3atPos1;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos1set && cam3pos1run && !cam3atPos1 && !runTick3) {         //  cam3 - set & running
      matrix.clrPixel(15, 6);
      matrix.setPixel(16, 6);
      matrix.clrPixel(17, 6);
      matrix.setPixel(18, 6);
      matrix.clrPixel(19, 6);
      oldcam3pos1set = cam3pos1set;
      oldcam3pos1run = cam3pos1run;
      oldcam3atPos1 = cam3atPos1;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos1set && !cam3pos1run && cam3atPos1) {         //  cam3 - set & at pos
      matrix.setPixel(15, 6);
      matrix.setPixel(16, 6);
      matrix.setPixel(17, 6);
      matrix.setPixel(18, 6);
      matrix.setPixel(19, 6);
      oldcam3pos1set = cam3pos1set;
      oldcam3pos1run = cam3pos1run;
      oldcam3atPos1 = cam3atPos1;
    }
    else if (!cam3pos1set) {                                      //  cam3 - clear
      matrix.clrPixel(15, 6);
      matrix.clrPixel(16, 6);
      matrix.clrPixel(17, 6);
      matrix.clrPixel(18, 6);
      matrix.clrPixel(19, 6);
      oldcam3pos1set = cam3pos1set;
    }
    matrix.writeScreen();
  }



  if (cam3pos2set != oldcam3pos2set || cam3pos2run != oldcam3pos2run || cam3atPos2 != oldcam3atPos2 || (cam3pos2run == true && runTick3 != oldRunTick3)) {
    if (cam3pos2set && !cam3pos2run && !cam3atPos2) {
      matrix.clrPixel(23, 6);
      matrix.clrPixel(24, 6);
      matrix.setPixel(25, 6);
      matrix.clrPixel(26, 6);
      matrix.clrPixel(27, 6);
      oldcam3pos2set = cam3pos2set;
      oldcam3pos2run = cam3pos2run;
      oldcam3atPos2 = cam3atPos2;
    }
    else if (cam3pos2set && cam3pos2run && !cam3atPos2 && runTick3) {
      matrix.setPixel(23, 6);
      matrix.clrPixel(24, 6);
      matrix.setPixel(25, 6);
      matrix.clrPixel(26, 6);
      matrix.setPixel(27, 6);
      oldcam3pos2set = cam3pos2set;
      oldcam3pos2run = cam3pos2run;
      oldcam3atPos2 = cam3atPos2;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos2set && cam3pos2run && !cam3atPos2 && !runTick3) {
      matrix.clrPixel(23, 6);
      matrix.setPixel(24, 6);
      matrix.clrPixel(25, 6);
      matrix.setPixel(26, 6);
      matrix.clrPixel(27, 6);
      oldcam3pos2set = cam3pos2set;
      oldcam3pos2run = cam3pos2run;
      oldcam3atPos2 = cam3atPos2;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos2set && !cam3pos2run && cam3atPos2) {
      matrix.setPixel(23, 6);
      matrix.setPixel(24, 6);
      matrix.setPixel(25, 6);
      matrix.setPixel(26, 6);
      matrix.setPixel(27, 6);
      oldcam3pos2set = cam3pos2set;
      oldcam3pos2run = cam3pos2run;
      oldcam3atPos2 = cam3atPos2;
    }
    else if (!cam3pos2set) {
      matrix.clrPixel(23, 6);
      matrix.clrPixel(24, 6);
      matrix.clrPixel(25, 6);
      matrix.clrPixel(26, 6);
      matrix.clrPixel(27, 6);
      oldcam3pos2set = cam3pos2set;
    }
    matrix.writeScreen();
  }


  if (cam3pos3set != oldcam3pos3set || cam3pos3run != oldcam3pos3run || cam3atPos3 != oldcam3atPos3 || (cam3pos3run == true && runTick3 != oldRunTick3)) {
    if (cam3pos3set && !cam3pos3run && !cam3atPos3) {
      matrix.clrPixel(30, 6);
      matrix.clrPixel(31, 6);
      matrix.setPixel(32, 6);
      matrix.clrPixel(33, 6);
      matrix.clrPixel(34, 6);
      oldcam3pos3set = cam3pos3set;
      oldcam3pos3run = cam3pos3run;
      oldcam3atPos3 = cam3atPos3;
    }
    else if (cam3pos3set && cam3pos3run && !cam3atPos3 && runTick3) {
      matrix.setPixel(30, 6);
      matrix.clrPixel(31, 6);
      matrix.setPixel(32, 6);
      matrix.clrPixel(33, 6);
      matrix.setPixel(34, 6);
      oldcam3pos3set = cam3pos3set;
      oldcam3pos3run = cam3pos3run;
      oldcam3atPos3 = cam3atPos3;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos3set && cam3pos3run && !cam3atPos3 && !runTick3) {
      matrix.clrPixel(30, 6);
      matrix.setPixel(31, 6);
      matrix.clrPixel(32, 6);
      matrix.setPixel(33, 6);
      matrix.clrPixel(34, 6);
      oldcam3pos3set = cam3pos3set;
      oldcam3pos3run = cam3pos3run;
      oldcam3atPos3 = cam3atPos3;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos3set && !cam3pos3run && cam3atPos3) {
      matrix.setPixel(30, 6);
      matrix.setPixel(31, 6);
      matrix.setPixel(32, 6);
      matrix.setPixel(33, 6);
      matrix.setPixel(34, 6);
      oldcam3pos3set = cam3pos3set;
      oldcam3pos3run = cam3pos3run;
      oldcam3atPos3 = cam3atPos3;
    }
    else if (!cam3pos3set) {
      matrix.clrPixel(30, 6);
      matrix.clrPixel(31, 6);
      matrix.clrPixel(32, 6);
      matrix.clrPixel(33, 6);
      matrix.clrPixel(34, 6);
      oldcam3pos3set = cam3pos3set;
    }
    matrix.writeScreen();
  }


  if (cam3pos4set != oldcam3pos4set || cam3pos4run != oldcam3pos4run || cam3atPos4 != oldcam3atPos4 || (cam3pos4run == true && runTick3 != oldRunTick3)) {
    if (cam3pos4set && !cam3pos4run && !cam3atPos4) {
      matrix.clrPixel(37, 6);
      matrix.clrPixel(38, 6);
      matrix.setPixel(39, 6);
      matrix.clrPixel(40, 6);
      matrix.clrPixel(41, 6);
      oldcam3pos4set = cam3pos4set;
      oldcam3pos4run = cam3pos4run;
      oldcam3atPos4 = cam3atPos4;
    }
    else if (cam3pos4set && cam3pos4run && !cam3atPos4 && runTick3) {
      matrix.setPixel(37, 6);
      matrix.clrPixel(38, 6);
      matrix.setPixel(39, 6);
      matrix.clrPixel(40, 6);
      matrix.setPixel(41, 6);
      oldcam3pos4set = cam3pos4set;
      oldcam3pos4run = cam3pos4run;
      oldcam3atPos4 = cam3atPos4;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos4set && cam3pos4run && !cam3atPos4 && !runTick3) {
      matrix.clrPixel(37, 6);
      matrix.setPixel(38, 6);
      matrix.clrPixel(39, 6);
      matrix.setPixel(40, 6);
      matrix.clrPixel(41, 6);
      oldcam3pos4set = cam3pos4set;
      oldcam3pos4run = cam3pos4run;
      oldcam3atPos4 = cam3atPos4;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos4set && !cam3pos4run && cam3atPos4) {
      matrix.setPixel(37, 6);
      matrix.setPixel(38, 6);
      matrix.setPixel(39, 6);
      matrix.setPixel(40, 6);
      matrix.setPixel(41, 6);
      oldcam3pos4set = cam3pos4set;
      oldcam3pos4run = cam3pos4run;
      oldcam3atPos4 = cam3atPos4;
    }
    else if (!cam3pos4set) {
      matrix.clrPixel(37, 6);
      matrix.clrPixel(38, 6);
      matrix.clrPixel(39, 6);
      matrix.clrPixel(40, 6);
      matrix.clrPixel(41, 6);
      oldcam3pos4set = cam3pos4set;
    }
    matrix.writeScreen();
  }


  if (cam3pos5set != oldcam3pos5set || cam3pos5run != oldcam3pos5run || cam3atPos5 != oldcam3atPos5 || (cam3pos5run == true && runTick3 != oldRunTick3)) {
    if (cam3pos5set && !cam3pos5run && !cam3atPos5) {
      matrix.clrPixel(43, 6);
      matrix.clrPixel(44, 6);
      matrix.setPixel(45, 6);
      matrix.clrPixel(46, 6);
      matrix.clrPixel(47, 6);
      oldcam3pos5set = cam3pos5set;
      oldcam3pos5run = cam3pos5run;
      oldcam3atPos5 = cam3atPos5;
    }
    else if (cam3pos5set && cam3pos5run && !cam3atPos5 && runTick3) {
      matrix.setPixel(43, 6);
      matrix.clrPixel(44, 6);
      matrix.setPixel(45, 6);
      matrix.clrPixel(46, 6);
      matrix.setPixel(47, 6);
      oldcam3pos5set = cam3pos5set;
      oldcam3pos5run = cam3pos5run;
      oldcam3atPos5 = cam3atPos5;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos5set && cam3pos5run && !cam3atPos5 && !runTick3) {
      matrix.clrPixel(43, 6);
      matrix.setPixel(44, 6);
      matrix.clrPixel(45, 6);
      matrix.setPixel(46, 6);
      matrix.clrPixel(47, 6);
      oldcam3pos5set = cam3pos5set;
      oldcam3pos5run = cam3pos5run;
      oldcam3atPos5 = cam3atPos5;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos5set && !cam3pos5run && cam3atPos5) {
      matrix.setPixel(43, 6);
      matrix.setPixel(44, 6);
      matrix.setPixel(45, 6);
      matrix.setPixel(46, 6);
      matrix.setPixel(47, 6);
      oldcam3pos5set = cam3pos5set;
      oldcam3pos5run = cam3pos5run;
      oldcam3atPos5 = cam3atPos5;
    }
    else if (!cam3pos5set) {
      matrix.clrPixel(43, 6);
      matrix.clrPixel(44, 6);
      matrix.clrPixel(45, 6);
      matrix.clrPixel(46, 6);
      matrix.clrPixel(47, 6);
      oldcam3pos5set = cam3pos5set;
    }
    matrix.writeScreen();
  }


  if (cam3pos6set != oldcam3pos6set || cam3pos6run != oldcam3pos6run || cam3atPos6 != oldcam3atPos6 || (cam3pos6run == true && runTick3 != oldRunTick3)) {
    if (cam3pos6set && !cam3pos6run && !cam3atPos6) {
      matrix.clrPixel(50, 6);
      matrix.clrPixel(51, 6);
      matrix.setPixel(52, 6);
      matrix.clrPixel(53, 6);
      matrix.clrPixel(54, 6);
      oldcam3pos6set = cam3pos6set;
      oldcam3pos6run = cam3pos6run;
      oldcam3atPos6 = cam3atPos6;
    }
    else if (cam3pos6set && cam3pos6run && !cam3atPos6 && runTick3) {
      matrix.setPixel(50, 6);
      matrix.clrPixel(51, 6);
      matrix.setPixel(52, 6);
      matrix.clrPixel(53, 6);
      matrix.setPixel(54, 6);
      oldcam3pos6set = cam3pos6set;
      oldcam3pos6run = cam3pos6run;
      oldcam3atPos6 = cam3atPos6;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos6set && cam3pos6run && !cam3atPos6 && !runTick3) {
      matrix.clrPixel(50, 6);
      matrix.setPixel(51, 6);
      matrix.clrPixel(52, 6);
      matrix.setPixel(53, 6);
      matrix.clrPixel(54, 6);
      oldcam3pos6set = cam3pos6set;
      oldcam3pos6run = cam3pos6run;
      oldcam3atPos6 = cam3atPos6;
      oldRunTick3 = runTick3;
    }
    else if (cam3pos6set && !cam3pos6run && cam3atPos6) {
      matrix.setPixel(50, 6);
      matrix.setPixel(51, 6);
      matrix.setPixel(52, 6);
      matrix.setPixel(53, 6);
      matrix.setPixel(54, 6);
      oldcam3pos6set = cam3pos6set;
      oldcam3pos6run = cam3pos6run;
      oldcam3atPos6 = cam3atPos6;
    }
    else if (!cam3pos6set) {
      matrix.clrPixel(50, 6);
      matrix.clrPixel(51, 6);
      matrix.clrPixel(52, 6);
      matrix.clrPixel(53, 6);
      matrix.clrPixel(54, 6);
      oldcam3pos6set = cam3pos6set;
    }
    matrix.writeScreen();
  }
}


//  char a[24] = "X";
//  char tmp[6];
//  sendCharArray((char *)(strcat(a, itoa(speedNo, tmp, 10))));

void textDisplay(char *array) {
  int i = 0;
  while (array[i] != 0) {
    matrix.setCursor(55 + (i * 5), 0);
    matrix.print(array[i++]);
  }
}

void camDisplay(char *array) {
  for (uint8_t y = 0; y < 7; y++) {
    for (uint8_t x = 95; x < 100; x++) {
      matrix.clrPixel(x, y);
    }
  }
  int i = 0;
  while (array[i] != 0) {
    matrix.setCursor(95 + (i * 5), 0);
    matrix.print(array[i++]);
  }
  matrix.writeScreen();
}

void startTextDisplay(char *array) {
  int i = 0;
  while (array[i] != 0) {
    matrix.setCursor(0 + (i * 5), 0);
    matrix.print(array[i++]);
  }
}
