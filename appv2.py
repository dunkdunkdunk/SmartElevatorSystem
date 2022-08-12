from multiprocessing import Process, Pipe
# from vision import cameraProcess
# from powerbi import sendData

import cv2

import imutils
import numpy as np

import pandas as pd
from datetime import datetime, timedelta
import requests
import time
import random


def cameraProcess1(data1):
    classifier = cv2.CascadeClassifier(
        '../Dataset/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture('humanface.mp4')

    starttime = datetime.now()

    while cap.read():
        img, numFace, date, mytime, finishtime = cameraProcess2(
            classifier, cap, starttime)
        if numFace >= 0:
            starttime = finishtime
            cv2.imshow('Result', img)
            data1.send([date, mytime, numFace])

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            cv2.imshow('Result', img)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def cameraProcess2(classifier, cap, start):
    ret, frame = cap.read()
    imS = cv2.resize(frame, (640, 480))

    date = datetime.today().strftime("%Y-%m-%d")
    mytime = datetime.now().isoformat()

    processtime = datetime.now()
    if start > processtime:
        timeDiffer = start - processtime
    else:
        timeDiffer = processtime - start
    timeDiffer_sec = int(timeDiffer.total_seconds())

    # print('The difference is approx. %s sec' % timeDiffer_sec)
    blur = cv2.GaussianBlur(imS, ((15, 15)), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    usedarea = 0
    numuser = 0

    lower_blue = np.array([75, 10, 10])
    upper_blue = np.array([130, 255, 255])

    maskblue = cv2.inRange(hsv, lower_blue, upper_blue)

    # find contours and get data
    contours2, _ = cv2.findContours(
        maskblue, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # entry line
    unusedarea = 0
    for con in contours2:
        area = cv2.contourArea(con)
        unusedarea += area
    print(unusedarea)
    if unusedarea < 40000:
        available = 0
    else:
        available = unusedarea // 40000
    # display current number of user
    cv2.putText(imS, "Space left for: "+str(available), (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    if timeDiffer_sec >= 3:
        return imS, available, date, mytime, processtime

    else:
        return imS, -1, date, mytime, processtime


def sendData(data):

    REST_API_URL = 'https://api.powerbi.com/beta/a6901d0c-e6ce-4ac7-93d5-6d406d25285f/datasets/6a482462-7fa4-4a5f-9835-55cd7acf4a62/rows?key=xrSUTFI%2Bs%2F2v4Wwbg35SW7sW9%2F24tr55nS1qsy8bh2urdhlpsGxi%2BFaHlSGoDxK4c%2Br3AJyDG4jO3XPy%2BiJHag%3D%3D'

    # while True:
    data_raw = []
    for i in range(1):
        row = [data[0], data[1], data[2]]
        data_raw.append(row)
        print("Raw data - ", data_raw)

    # set the header record
    HEADER = ["date", "time", "numFace"]

    data_df = pd.DataFrame(data_raw, columns=HEADER)
    data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
    print("JSON dataset", data_json)

    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_json)

    print("Data posted in Power BI API")


if __name__ == '__main__':
    data1, data2 = Pipe()

    camProcess = Process(target=cameraProcess1, args=(data2,))
    camProcess.start()
    while True:
        dataVal = data1.recv()

        pbiProcess = Process(target=sendData, args=(dataVal,))
        pbiProcess.start()
        pbiProcess.join()
