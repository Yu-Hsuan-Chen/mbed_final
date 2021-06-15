import time
import serial
import sys,tty,termios

s = serial.Serial(sys.argv[1])


class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
    if k=='\x1b':
        k2 = inkey()
        k3 = inkey()
        k4 = inkey()
        k5 = inkey()
        k6 = inkey()
        if (k3=='C'and k6=='A') or (k3=='A'and k6=='C'):
            print ("up right")
            s.write("/turn/run 100 -0.3\n".encode())
            time.sleep(2.2)
        if (k3=='D'and k6=='A') or (k3=='A'and k6=='D'):
            print ("up left")
            s.write("/turn/run 100 0.3\n".encode())
            time.sleep(2.2)
        if (k3=='C'and k6=='B') or (k3=='B'and k6=='C'):
            print ("down right")
            s.write("/turn/run -100 -0.3\n".encode())
            time.sleep(2.2)
        if (k3=='D'and k6=='B') or (k3=='B'and k6=='D'):
            print ("down left")
            s.write("/turn/run -100 0.3\n".encode())
            time.sleep(2.2)
        if k3=='A' and k6=='A':
            print ("up")
            s.write("/goStraight/run 50 0.9 1\n".encode())
            time.sleep(1)
        if k3=='B' and k6=='B':
            print ("down")
            s.write("/goStraight/run -50 0.9 1\n".encode())
            time.sleep(2.8)
        # time.sleep(1)
        s.write("/stop/run \n".encode())
    elif k=='q':
        print ("quit")
        return 0
    else:
        print ("not an arrow key!")
    return 1

if len(sys.argv) < 1:
    print ("No port input")

# while get():
#     i = 0




tmp = True
while(tmp):
    mode = input("Enter \"all\", \"following\", \"classification\" or \"parking\" to start the program : ( Enter \"finish\" to close the program ) \n")
    if mode == "all":
        s.write("all\n".encode())
    elif mode == "following":
        s.write("following\n".encode())
    elif mode == "classification":
        s.write("classification\n".encode())
    elif mode == "parking":
        s.write("parking\n".encode())
    elif mode == "finish":
        s.write("finish\n".encode())
        tmp = False
    else:
        print("INPUT ERROR! TRY AGAIN! \n")