import numpy as np
import cv2
import os
from mss_capture import abc
import pyxhook
import mss


KeyList = [ 119, 97, 100, 113, 102]
#            w   a    d    q    f
starting_value = 1
key = 0


while True:
    file_name = 'test-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        training_data = []
        break


def OnKeyPress(event):
    global key
    key = 0
    if event.Ascii in KeyList:
        key = event.Ascii

def OnKeyRelease(event):
    global key
    key = 0

paused = True
new_hook=pyxhook.HookManager()
new_hook.KeyDown=OnKeyPress
new_hook.KeyUp = OnKeyRelease
new_hook.HookKeyboard()
new_hook.start()


print('STARTING!!!')
while(True):
    global key
    if key == 119:
        paused = False
    if not paused:
        output=[]
        screen = abc()
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        screen = cv2.resize(screen, (100,55))

        #global key
        if key == 119: #w
            output = [1,0,0,0,0]
    	elif key == 97: #a
    	    output = [0,1,0,0,0]
        elif key == 100: #d
    	    output = [0,0,1,0,0]
    	elif key ==102: #f          pressed many times while crossing the junction.
    	    output = [0,0,0,0,1]
        else:            #Nokeys
	        output = [0,0,0,1,0]
        

        if key==113:
            np.save(file_name,training_data)
            for i in range(25):
                print('DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                new_hook.cancel()
            break
        else:
            training_data.append([screen,output])    
