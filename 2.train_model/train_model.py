import numpy as np
import cv2
import time
import os
import pandas as pd
from MavNet import mavnet
from random import shuffle


FILE_I_END = 1

WIDTH = 100
HEIGHT = 100
LR = 1e-4
EPOCHS = 20

MODEL_NAME = 'parrotBeebop-{}-{}-LR-{}.model'.format('mavnetnet_color',LR,FILE_I_END)
PREV_MODEL = 'parrotBeebop-{}-{}-LR-{}.model'.format('mavnetnet_color',LR,FILE_I_END)

LOAD_MODEL = False


model = mavnet(WIDTH, HEIGHT, 1, LR, output=5, model_name=MODEL_NAME)

if LOAD_MODEL:
    model.load(PREV_MODEL)
    print('We have loaded a previous model!!!!')


# iterates through the training files


for e in range(EPOCHS):


    for i in range(13,37):

        try:
            file_name = 'data-{}.npy'.format(i)
            # full file info
            train_data = np.load(file_name)

            shuffle(train_data)
            train = train_data[:-1000]
            test = train_data[-1000:]

            X = np.array([i[1] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
            Y = [i[2] for i in train]

            test_x = np.array([i[1] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
            test_y = [i[2] for i in test]

            model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
                snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)


            if i%10==0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)

        except Exception as e:
            print(str(e))