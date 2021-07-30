import datetime
import os
import threading
import time

import cv2
import numpy
import pandas as pd

# -------------------------
from flask import jsonify, json
from imutils.video import WebcamVideoStream

datas = []
flag = True
video_flag = True
global im
global ret
global cam
local_url = "http://127.0.0.1:5000/send_info"


# 录像
def load_video(name, cap):
    global im
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%Y-%m-%d %H-%M-%S')
    file_name_str = 'D:\\nginx-with-nginx-http-flv-module\\server\\record\\' + name + '_' + current_time_str + '.mp4'
    fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')  # 视频编解码器
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
    out = cv2.VideoWriter(file_name_str, fourcc, fps, (width, height))  # 写入视频
    start_time = time.time()
    while cap.isOpened():
        out.write(im)  # 写入帧
        end_time = time.time()
        if (end_time - start_time > 5):
            print("out")
            global video_flag
            out.release()
            video_flag = True
            break
        else:
            s = 10
            # print(name)
        time.sleep(0.015)
    print(2)


def get_image():
    global cam, flag
    # cam = cv2.VideoCapture(0)
    # cam = cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    global ret, im
    while flag:
        # global datas
        try:
            ret, im = cam.read()
        except Exception:
            break
        # print(datas)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def recognize_attendence(vid):
    global im, cam
    global flag
    flag = True
    get_name = ''
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel" + os.sep + "trainer.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    # cam = cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    # 'rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream'
    # vs = WebcamVideoStream(src='rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream').start()
    # vs=WebcamVideoStream(src=0).start()

    # cam = cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    cam = cv2.VideoCapture('rtmp://localhost:1935/flv/stream_' + vid)
    # cam = cv2.VideoCapture(0)

    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    image_thread = threading.Thread(target=get_image, args=())
    image_thread.start()
    # minW = 640
    # minH = 480

    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 视频编解码器
    # fps = cam.get(cv2.CAP_PROP_FPS)  # 帧数
    # width, height = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
    # out = cv2.VideoWriter('result.mp4', fourcc, fps, (width, height))  # 写入视频

    # global flag
    # flag = True
    while flag:
        newDatas = []
        # ret, im = cam.read()
        # im=vs.read()
        # ret,im=vs.read()
        try:
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(int(minW), int(minH)),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)
        except Exception:
            continue

        for (x, y, w, h) in faces:

            data = {"id": "1", "name": "gdf", "x": int(x), "y": int(y), "width": int(w), "height": int(h)}

            # 发送信息

            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 100:
                cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id) + "_" + aa
                data['id'] = str(Id)

            else:
                # Id = '  Unknown  '
                # tt = ''
                # confstr = "  {0}%".format(round(100 - conf))
                continue

            if (100 - conf) > 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            tt = str(tt)[2:-2]
            if (100 - conf) > 55:
                get_name = tt.split('_')[1]
                name_in_file = tt
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                # 打开线程
                global video_flag
                if video_flag == True:
                    video_flag = False
                    video_thread = threading.Thread(target=load_video, args=(name_in_file, cam,))
                    video_thread.start()

            # else:
            # if out.isOpened():
            #     out.release()

            cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100 - conf) > 53:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)
            elif (100 - conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

            data["name"] = tt

            data_json = json.dumps(data)
            newDatas.append(data)
            # print(newDatas)

        global datas
        datas = newDatas.copy()
        # print(datas)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

        cv2.imshow('Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            # out.release()
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance" + os.sep + "Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName, index=False)
    print("Attendance Successful")
    cam.release()
    cv2.destroyAllWindows()
