

from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
def camera_factory(choice):
    if choice==1 :
        cap=cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    if choice==2 :
        cap=cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    return cap
def stream_factory(choice):
    if choice==1 :
        cap=WebcamVideoStream(src=0).start()
    if choice==2 :
        cap=WebcamVideoStream(src='rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream').start()
    return cap

def get_camera(choice):
    vs=stream_factory(choice)
    while True :
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # 检查是否需要把帧通过cv2展示
        # if args["display"] > 0:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    vs.stop()





def improved_camera(choice):
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-frames", type=int, default=100,
                    help="# of frames to loop over for FPS test")
    ap.add_argument("-d", "--display", type=int, default=-1,
                    help="Whether or not frames should be displayed")
    args = vars(ap.parse_args())

    # 获取视频流指针，初始化FPS计数器
    print("[INFO] sampling frames from webcam...")
    stream = camera_factory(1)
    fps = FPS().start()

    # 循环遍历一些帧
    while fps._numFrames < args["num_frames"]:
        # 从流中获取帧，resize 宽度为400
        (grabbed, frame) = stream.read()
        frame = imutils.resize(frame, width=400)

        # 检查帧是否要展示
        if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

        # 更新FPS计数器
        fps.update()

    # 停止计数器
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # 清理、释放资源
    stream.release()
    cv2.destroyAllWindows()

    # 创建线程化的视频流，允许摄像机传感器预热，并且启动FPS计数器
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    # 使用线程循环处理每一帧
    while fps._numFrames < args["num_frames"]:
        # 从线程化的视频流中获取帧，resize到宽度为400像素
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # 检查是否需要把帧通过cv2展示
        if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

        # 更新FPS计数器
        fps.update()

    # 停止计数 展示FPS的统计信息
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # 做一些清理工作 释放摄像头 关闭打开的窗口
    cv2.destroyAllWindows()
    vs.stop()
def camer():
    import cv2

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    # cap = cv2.VideoCapture('rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream')
    cap=cv2.VideoCapture(0)
    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (10,159,255), 2)


        # Display
        cv2.imshow('Webcam Check', img)

        # Stop if escape key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
