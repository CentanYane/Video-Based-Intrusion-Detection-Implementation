import csv

import cv2
import os


# counting the numbers
from imutils.video import WebcamVideoStream


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function
def get_images_from_video(name,Id,path):
    cap=cv2.VideoCapture(path)
    cam=WebcamVideoStream(src=path).start()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    count=0
    while count<totalFrameNumber:
        count+=1
        img = cam.read()
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep + name + "." + Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('frame',img)
        except:
            break
    print('here')
    res = "Images Saved for ID : " + str(Id) + " Name : " + name
    row = [Id, name]
    with open("StudentDetails" + os.sep + "StudentDetails.csv", 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    if os.path.exists(path):
        os.remove(path)

def takeImages():


    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    if(is_number(Id) and name.isalpha()):
        cam= WebcamVideoStream(src='rtsp://admin:wzk517226@192.168.1.64:554/h264/ch1/main/av_stream').start()
        # cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep +name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                #display the frame
                cv2.imshow('frame', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open("StudentDetails"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        if(name.isalpha()):
            print("Enter Numeric ID")

def get_images_video():
    for root,dirs,files in os.walk('TrainingVideo'):
        print(files)
        for in_file in files:
            if is_true_video(in_file):
                print('true')
                arguments=in_file.split('.')
                path='TrainingVideo'+os.sep+in_file
                print(path)
                get_images_from_video(arguments[0],arguments[1],path)
            else:
                print('false')
def is_true_video(path):
    judges=path.split('.')
    if len(judges)==3:
       if is_number(judges[1]) and judges[0].isalpha() and is_true_endswith(judges[2]):
           return True
    return False
def is_true_endswith(s):
    if s=='MOV' or s=='MP4':
        return True
    else:
        return False
