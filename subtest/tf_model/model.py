# Edge Impulse - OpenMV Image Classification Example

import sensor, image, time, os, tf

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)      # Set frame size to QVGA (320x240)
#sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.
sensor.set_vflip(True)
sensor.set_hmirror(True)

net = "trained.tflite"
labels = [line.rstrip('\n') for line in open("labels.txt")]

clock = time.clock()
while(True):

    clock.tick()
    img = sensor.snapshot()
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5, roi=(25, 20, 110, 110)):
        img.draw_rectangle(obj.rect(), color = (255, 0, 0))

        predictions_list = list(zip(labels, obj.output()))
        img.draw_string(obj.x()+3, obj.y()-3, labels[obj.output().index(max(obj.output()))], mono_space = False, scale = 2, color = (255,0,0))
        #time.sleep(1)
        for i in range(len(predictions_list)):
            print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))
            print("prediction: %s" % predictions_list[obj.output().index(max(obj.output()))][0])
    print(clock.fps(), "fps")

