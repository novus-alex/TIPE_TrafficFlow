import cv2
from time import *
import numpy as np
import os

kernel = np.ones((4,4),np.uint8)

def get_time_log():
    return f'[{time.strftime("%H:%M:%S", localtime())}]'

def log(msg):
    print(f'{get_time_log()}: {msg}')

class FileHandler:
    def __init__(self, filename):
        self.frames = []
        vid = cv2.VideoCapture(os.path.abspath(filename))
        success,image = vid.read()
    #log('Starting spliting the video...')
        while success:
            self.frames.append(image)    
            success,image = vid.read()
        #log('Succesfully splited the video.')
        

    def get_cv2_object(self):
        return self.frames

def analyze(frames):
    car_positions = []
    for i in range(len(frames)-1):
        positions = []
        fGray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        sGray = cv2.cvtColor(frames[i+1], cv2.COLOR_BGR2GRAY)

        diff_img = cv2.absdiff(fGray, sGray)
        ret, thresh = cv2.threshold(diff_img, 30, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, kernel, iterations = 1)
    
        contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            positions.append([x, y])
        car_positions.append(positions)
    return car_positions


f = FileHandler('TIPE/VideoAnalyzing/test.mp4').get_cv2_object()
r = analyze(f)

speeds = []
for i in range(1, len(r)):
    car_speed = []
    for j in range(len(r[i])):
        print((r[i][j][0]-r[i-1][j][0])/0.6)
        car_speed.append((r[i][j][0]-r[i-1][j][0])/0.6)
    speeds.append(car_speed)

for i in range(len(speeds)):
    print(r[i][0])