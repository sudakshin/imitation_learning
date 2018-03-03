import numpy as np
from mss_capture import test
import cv2
from MavNet import mavnet
import pyautogui
import pyxhook
import time


WIDTH = 100
HEIGHT = 100
LR = 1e-4

key = 0

def OnKeyPress(event):
    global key
    key = 0
    if event.Ascii in 116:
        key = 116

#w = [1,0,0,0,0]
#a = [0,1,0,0,0]
#d = [0,0,1,0,0]
#nk = [0,0,0,1,0]
#j = [0,0,0,0,1]

check_junction = True
junction_count = 0
start_time = 0.0
junction_order = [ 'left', 'right', 'straight', 'left', 'straight', 'straight']


def straight():
    pyautogui.hotkey('w')

def left():
    pyautogui.hotkey('a')
    
def right():
    pyautogui.hotkey('d')
    
def no_keys():
    

def junction():
    if check_junction == True :
        start_time = time.time()
        check_junction = False
        if junction_order[junction_count] == 'left' :
            left()
            left()
            left()
            straight()
            straight()
            straight()

        elif junction_order[junction_count] == 'right' :
            right()
            right()
            right()
            straight()
            straight()
            straight()

        else :
            straight()
            straight()
            straight()
            straight()
            straight()
            straight()

        junction_count = junction_count + 1


model = mavnet(WIDTH, HEIGHT, 1, LR, output=5)
MODEL_NAME = 'parrotBeebop-mavnet_color-0.0001-LR-1.model'#

model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')

def main():

    new_hook=pyxhook.HookManager()
    new_hook.KeyDown=OnKeyPress
    new_hook.HookKeyboard()
    new_hook.start()
    screen = test()
    global key
    paused =True
    while(True):        
        
        if not paused:
            screen = test()
            prediction = model.predict([screen.reshape(WIDTH,HEIGHT,1)])[0]
            prediction = np.array(prediction)
            mode_choice = np.argmax(prediction)
            
            if mode_choice == 0:
                straight()
            elif mode_choice == 1:
                left()
            elif mode_choice == 2:
                right()
            elif mode_choice == 3:
                no_keys()
            elif mode_choice == 4:
                junction()

        # p pauses game and can get annoying.
        if key == 116:
            if paused:
                paused = False
                print('UnPaused')
            else:
                paused = True
                print('Paused')
                key = 0
        
        if time.time() - start_time >= 10.0 :
            check_junction = True

main()