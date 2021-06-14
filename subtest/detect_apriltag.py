import pyb, sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
sensor.set_vflip(True)
sensor.set_hmirror(True)
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)


def degrees(radians):
   return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

SPEED = 50
#uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())

#uart.write(("/stop/run\n").encode())
while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        #print(tag.cx(), tag.cy())
        #print(tag.w()*tag.h())
        if(tag.w()*tag.h()>= 4000):
            print("stop: %d", tag.w()*tag.h())
            uart.write(("/stop/run\n").encode())
        else:
            #if (degrees(tag.y_rotation())<360 and degrees(tag.y_rotation())>=340) or (degrees(tag.y_rotation())<20 and degrees(tag.y_rotation())>=0):
            if tag.cx() < 85 and tag.cx() >75:
                print("go straight:", tag.cx())
                uart.write(("/goStraight/run %d 1 1 \n" % SPEED).encode())
            #elif degrees(tag.y_rotation())>=20 and degrees(tag.y_rotation())<=90:
            elif tag.cx()<=75:
                turn = 50
                factor = 1-(75-tag.cx())/20
                print("turn left", tag.cx(), turn, factor)
                #turn = 1.2*(180-degrees(tag.y_rotation()))
                #factor = 1-(180-degrees(tag.y_rotation()))/8
                #print("turn left:", degrees(tag.y_rotation()), turn, factor)
                uart.write(("/turn/run %d %f \n" % (turn, factor)).encode())
            #elif degrees(tag.y_rotation())>=90 and degrees(tag.y_rotation())<340:
            elif tag.cx()>=85:
                turn = 50
                factor = min((tag.cx()-85)/20, 1)
                print("turn right", tag.cx(), turn, factor)
                #turn = 1.2*degrees(tag.y_rotation())
                #factor = 1-degrees(tag.y_rotation())/8
                #print("turn right:", degrees(tag.y_rotation()), turn, factor)
                uart.write(("/turn/run %d %f \n" % (turn, -factor)).encode())
            else:
                print("other: %f", degrees(tag.y_rotation()))

        #print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
              #degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        ## Translation units are unknown. Rotation units are in degrees.
        #if(tag.z_translation() >= -3):
            #print("stop: %d", tag.z_translation())
        #else:
        #print(("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args).encode())

