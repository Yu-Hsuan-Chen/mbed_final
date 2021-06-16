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

## LED setting (1: red, 2: green, 3: blue, 4: IR)
led_s = pyb.LED(1) #start / can receive massage from mbed
led_s.on()
led_x = pyb.LED(2) #xbee error
led_x.off()
led_c = pyb.LED(3) #close
led_c.off()

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


## PART 0
def initialization(mode):
    SPEED = 50
    TAG_X = 1000
    TAG_Y = 1000
    TAG_W = 0
    TAG_H = 0
    led_s.on()
    time.sleep(0.5)
    led_s.off()
    time.sleep(0.5)
    led_s.on()
    time.sleep(0.5)
    led_s.off()
    time.sleep(0.5)
    led_s.on()
    time.sleep(0.5)
    led_s.off()

def close():
    led_s.off()
    led_c.on()
    time.sleep(0.5)
    led_c.off()
    time.sleep(0.5)
    led_c.on()
    time.sleep(0.5)
    led_c.off()
    time.sleep(0.5)
    led_c.on()
    time.sleep(0.5)
    led_c.off()

## PART 1
def follow_map():
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
            tmp = tmp + 1
    time.sleep(0.3)
    uart.write(("/stop/run \n").encode())

## PART2
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

def classify_pic():
    uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
    time.sleep(1.8)
    uart.write(("/stop/run \n").encode())
    time.sleep(1)
    ##while(1):
    img = sensor.snapshot()
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5, roi=(25, 20, 110, 110)):
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

## PART3
def AprilTag_calibration():
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
                    factor = max(1-(75-tag.cx())/23, 0.1)
                    #print("turn left", tag.cx(), turn, factor)
                    uart.write(("/turn/run %d %f \n" % (turn, factor)).encode())
                elif tag.cx()>=95:
                    turn = SPEED
                    factor = min((tag.cx()-85)/23, 1)
                    #print("turn right", tag.cx(), turn, factor)
                    uart.write(("/turn/run %d %f \n" % (turn, -factor)).encode())
                else:
                    print("other: %f", degrees(tag.y_rotation()))


while(1):
    buf = []
    buf = uart.read(20)
    start = str(buf)
    if "all" in start:
        mode = "ALL"
        initialization(mode)
        follow_map()
        classify_pic()
        AprilTag_calibration()
        print("all done")
        uart.write(("Done\n").encode())
        led_s.on()
    elif "following" in start:
        mode = "FOLLOW LINE"
        initialization(mode)
        follow_map()
        print("follow done")
        uart.write(("Done\n").encode())
        led_s.on()
    elif "classification" in start:
        mode = "CLASSIFICATION"
        initialization(mode)
        classify_pic()
        print("class done")
        uart.write(("Done\n").encode())
        led_s.on()
    elif "parking" in start:
        mode = "PARKING"
        initialization(mode)
        AprilTag_calibration()
        print("parking done")
        uart.write(("Done\n").encode())
        led_s.on()
    elif "finish" in start:
        close()
        break
    elif "xbee error" in start:
        led_x.on()
        time.sleep(0.5)
        led_x.off()
        time.sleep(0.5)
        led_x.on()
        time.sleep(0.5)
        led_x.off()
        time.sleep(0.5)
        led_x.on()
        time.sleep(0.5)
        led_x.off()
        print("xbee error")
        break




