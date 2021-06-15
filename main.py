import sensor, image, time, pyb, tf, os
#import _thread

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_vflip(True)
sensor.set_hmirror(True)

clock = time.clock()
uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)


## tflite model
net = "trained.tflite"
labels = ["cat", "dog"]

## AprilTag parameter
f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

## car parameters
SPEED = 50

## map parameter
TAG_X = 1000
TAG_Y = 1000
TAG_W = 0
TAG_H = 0

clock.tick()

def clockwise():
    #print("turn left")
    uart.write(("/turn/run %d 0.2\n" % SPEED).encode())
    time.sleep(2)

    #print("go Straight")
    uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
    time.sleep(1)

    #print("turn right")
    uart.write(("/turn/run %d -0.2\n" % SPEED).encode())
    time.sleep(3.6)

    #print("go Straight")
    uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
    time.sleep(1.5)

    #print("turn left")
    uart.write(("/turn/run %d 0.2\n" % SPEED).encode())
    time.sleep(2)
    #print("stop")
    uart.write(("/stop/run \n").encode())
    #time.sleep(1)

def counterclockwise():
    #print("turn right")
    uart.write(("/turn/run %d -0.2\n" % SPEED).encode())
    time.sleep(2)

    #print("go Straight")
    uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
    time.sleep(1.5)

    #print("turn left")
    uart.write(("/turn/run %d 0.2\n" % SPEED).encode())
    time.sleep(3.8)

    #print("go Straight")
    uart.write(("/goStraight/run %d 1 1 \n" %SPEED).encode())
    time.sleep(2)

    #print("turn right")
    uart.write(("/turn/run %d -0.2\n" %SPEED).encode())
    time.sleep(1.8)

    #print("stop")
    uart.write(("/stop/run \n").encode())
    #time.sleep(1)


### PART 0 : choose mode
#print("START")

#buf = []

#while not buf:
    #buf = uart.read(13)

#mode = str(buf)

#if "normal" in mode:
    #SPEED = 50
#elif "sport" in mode:
    #SPEED = 80
#else:
    #print("error")

#print("SPEED is %d" % SPEED)


time.sleep(2)
## PART1 : follow map
tmp = 0
while(tmp < 3):
    img = sensor.snapshot()
    TAG_X = 1000
    TAG_Y = 1000
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        TAG_X = tag.cx()
        TAG_Y = tag.cy()
        TAG_W = tag.w()
        TAG_H = tag.h()

        #print(TAG_X, TAG_Y)
        #print(TAG_W*TAG_H)

    if TAG_Y>105:
        #print("GO")
        uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
    else:
        #print("TURN")
        uart.write(("/stop/run \n").encode())
        uart.write(("/turn/run %d -0.2\n" % SPEED).encode())
        time.sleep(1.95)
        #uart.write(("/stop/run \n").encode())
        break
        #if tmp == 0:
            #time.sleep(2.3)
        #else:
            #time.sleep(2.6)
        tmp = tmp + 1

### PART2 : classify pic
time.sleep(0.3)
uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
time.sleep(1.8)
uart.write(("/stop/run \n").encode())
time.sleep(1)
##while(1):
img = sensor.snapshot()
for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5, roi=(25, 20, 110, 110)):
    #print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
    img.draw_rectangle(obj.rect(), color = (255, 0, 0))
    #img.draw_rectangle(20, 0, 110, 110, color = (255, 0, 0))
    # This combines the labels and confidence values into a list of tuples
    predictions_list = list(zip(labels, obj.output()))
    img.draw_string(obj.x()+3, obj.y()-3, labels[obj.output().index(max(obj.output()))], mono_space = False, scale = 2, color = (255,0,0))
    time.sleep(1)
    #for i in range(len(predictions_list)):
        #print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))
        #print("prediction: %s" % predictions_list[obj.output().index(max(obj.output()))][0])

if predictions_list[obj.output().index(max(obj.output()))][0] == "cat":
    clockwise()
else:
    counterclockwise()


#### PART3 : AprilTag calibration

uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
time.sleep(6)
uart.write(("/stop/run \n").encode())

tmp3 = True
while(tmp3):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        #print(tag.cx(), tag.cy())
        #print(tag.w()*tag.h())
        if(tag.w()*tag.h()>= 2000):
            tmp3 = False
            #print("stop: %d", tag.w()*tag.h())
            uart.write(("/stop/run\n").encode())
        else:
            if tag.cx() < 95 and tag.cx() >75:
                #print("go straight:", tag.cx())
                uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
            elif tag.cx()<=75:
                turn = SPEED
                factor = max(1-(75-tag.cx())/24, 0.1)
                #print("turn left", tag.cx(), turn, factor)
                uart.write(("/turn/run %d %f \n" % (turn, factor)).encode())
            elif tag.cx()>=95:
                turn = SPEED
                factor = min((tag.cx()-85)/24, 1)
                #print("turn right", tag.cx(), turn, factor)
                uart.write(("/turn/run %d %f \n" % (turn, -factor)).encode())
            else:
                print("other: %f", degrees(tag.y_rotation()))


