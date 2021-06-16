# mbed_final

## Overview

### PART0
- Choose which tasks you want to run.
- You can run the whole program or run the subtask only.

### PART1 : follow map 
- By detect the AprilTag to control car go straight or turn left/right.

### PART2 : classification
- Classify the picture of dog or cat.

### PART3 : AprilTag_calibration
- By detect the AprilTag to calibrate the position of car in order to arrive the destination.

### Map :
![](https://github.com/Yu-Hsuan-Chen/mbed_final/blob/master/pic/PNG%E5%BD%B1%E5%83%8F%202.png)

## How to run the program
1. Run main.cpp in mbed.
2. Copy "subtest/tf_model/trained.tflite" and "subtest/tf_model/trained.tflite/labels.txt" to openmv drive.
3. Copy main.py to openmv drive.
4. Connect the mbed and openmv to portable charger.
5. After openmv red led on, run the car_control.py on PC, then enter the message to choose the part you want to run (In Part 0).
6. This message will be sent to mbed via Xbee.
7. Then, you will see openmv red led flashing and off, which mean the message is sent to openmv from mbed via Uart.
8. After the task is done, red led will light again, which means you can enter the next message to run another part.
9. If you want to close the program, just enter the "finish", then openmv, mbed, python will be all closed.
