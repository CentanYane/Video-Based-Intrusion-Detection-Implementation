# from dateutil import rrule
import json
import os
from datetime import datetime, timedelta
import time
import traceback
from os import listdir
import hashlib
import cv2
import requests
from flask import Flask, request, jsonify, Response

import threading

# from FRAS import Recognize, Capture_Image, Train_Image, calculate_token
import Recognize
import Capture_Image, Train_Image, calculate_token

app = Flask(__name__)

my_thread = threading

data_buffer = {

}

DatabaseURL = 'http://192.168.137.76:8081/test'
CameraURL = '0'
CalculateURL = 'http://192.168.137.13:5000'
ip = '192.168.137.1'

vid=1

@app.route("/send_info", methods=["POST"])
def get_datas():
    my_json = request.get_json()
    cam_id = my_json.get("id")
    get_time = my_json.get("time")
    # global data_buffer
    # try:
    #     print(get_time)
    #     data = data_buffer[get_time].copy()
    #     print(data_buffer[get_time])
    # except Exception:
    #     data = []
    #

    global data_buffer
    try:
        # print(get_time)
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        data = data_buffer[current_time_str].copy()
        # print(data)
        print(data_buffer)
        # data = Recognize.datas.copy()
        # print(Recognize.datas.copy())
        # print(data)
    except Exception:
        print(5)
        data = []

    result = {"id": cam_id,
              "data": data}

    total = len(data)
    result["total"] = total

    if total != 0:
        result["success"] = True
    else:
        result["success"] = False

    result["time"] = get_time

    # print(data_buffer)

    # return "good"
    return jsonify(result)


@app.route('/login', methods=['POST'])  # 默认根路径
def login():
    url = DatabaseURL
    header = request.headers
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    username = get_Data.get('username')
    password = get_Data.get('password')
    print(username)
    print(password)

    # 传输到数据库端
    data = {"operation": "login", "username": username, "password": password}
    data = json.dumps(data)
    r = requests.post(url, data=data)
    print(r.text)
    # 将得到的数据json化
    r = r.json()

    if r.get('status') == 'success':
        token = calculate_token.get_token(r.get('userID'))
        data = jsonify({  # 响应体

            "status": "ok",  # 登陆验证结果，比如ok、fail、error。不为ok时返回内容不含token（或为空）
            "token": token,  # token，根据userId计算，无超时
            "userId": r.get('userID'), # 用户识别id
            "group":r.get('group')

        })
        return data, 200, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]
    else:
        data = jsonify({
            "errorCode": "504",  # 业务约定的错误码
            "errorMessage": "not match",  # 业务上的错误信息
            "success": True  # 业务上的请求是否成功

        })
        return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]


@app.route('/userInfo', methods=['POST', 'GET'])
def get_userInfo():
    url = DatabaseURL

    header = request.headers
    # body = request.get_data()
    # body = json.loads(body)
    print(header.get('Authorization'))

    # 检测token是否正确
    if calculate_token.check_token(header.get('Authorization').split(' ', 1, )[1]):
        # 传输到数据库端
        print(1)
        data = {"operation": "userInfo", "userID": header.get('Authorization').split(' ', 1, )[1].split('.')[0]}
        print(data)
        data = json.dumps(data)
        r = requests.post(url, data=data)
        print(r.text)
        r = r.json()

        data = jsonify({
            "name": r.get('name'),  # 要显示在界面上的用户名
            "avatar": r.get('avatar'),  # 用户头像链接
            "group": r.get('group')  # 用户所属权限组，比如Admin、Watcher
        })
        print(data)

        return data, 200, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]
    else:
        print(2)
        data = jsonify({
            "errorCode": "504",  # 业务约定的错误码
            "errorMessage": "not match",  # 业务上的错误信息
            "success": True  # 业务上的请求是否成功
        })
        return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]


# 待改
@app.route('/streams', methods=['POST', 'GET'])
def get_streams():
    header = request.headers
    # body = request.get_data()
    # body = json.loads(body)
    # 检测token是否正确
    if calculate_token.check_token(header.get('Authorization').split(' ', 1, )[1]):
        data = jsonify({
            "userId": 1,  # 用户识别id
            "data": [
                {
                    "vid": 1,  # 视频流id
                    "key": "",  # 取流时在链接后附加的key（eg rstp://link/?key=xxx），可以没有
                    "title": "深渊巨眼",  # 视频流标题
                    "href": "http://"+ip+":8080/live?port=1935&app=flv&stream=stream_1"  # 视频流地址
                },
                {
                    "vid": 2,  # 视频流id
                    "key": "",  # 取流时在链接后附加的key（eg rstp://link/?key=xxx），可以没有
                    "title": "深渊巨眼2号",  # 视频流标题
                    "href": "http://" + ip + ":8080/live?port=1935&app=flv&stream=stream_2"  # 视频流地址
                },
                {
                    "vid": 3,  # 视频流id
                    "key": "",  # 取流时在链接后附加的key（eg rstp://link/?key=xxx），可以没有
                    "title": "深渊巨眼3号",  # 视频流标题
                    "href": "http://" + ip + ":8080/live?port=1935&app=flv&stream=stream_3"  # 视频流地址
                }
            ],
            "total": 1,  # 列表的内容总数
            "success": True
        })

        return data, 200, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]
    else:
        data = jsonify({
            "errorCode": "504",  # 业务约定的错误码
            "errorMessage": "not match",  # 业务上的错误信息
            "success": True  # 业务上的请求是否成功
        })
        return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]


# 待测
@app.route('/streamSquares', methods=['POST', 'GET'])
def get_stream_Squares():
    header = request.headers
    # 检测token是否正确
    if calculate_token.check_token(header.get('Authorization').split(' ', 1, )[1]):
        # 请求计算端的计算结果
        # my_json = request.get_json()
        # cam_id = my_json.get("id")
        # get_time = my_json.get("time")
        cam_id = request.args.get('vid')

        #比较是否变化
        global vid
        if vid!=cam_id:
            vid=cam_id
            stop_camera(cam_id)

        global data_buffer
        try:
            # print(get_time)
            current_time = datetime.now()
            current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            # data = data_buffer[current_time_str].copy()
            data = Recognize.datas
            print(data)
        except Exception:
            print(6)
            data = []

        result = {"vid": cam_id,
                  "data": data}

        total = len(data)
        result["total"] = total

        if total != 0:
            result["success"] = True
        else:
            result["success"] = True

        # result["time"] = get_time

        # print(data_buffer)

        # return "good"
        return jsonify(result), 200, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                                      ("Access-Control-Allow-Origin", header.get('Origin'))]

    else:
        # token检测不成功
        data = jsonify({
            "errorCode": "504",  # 业务约定的错误码
            "errorMessage": "net match",  # 业务上的错误信息
            "success": True  # 业务上的请求是否成功
        })
        return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]


@app.route('/addCamera', methods=['POST'])
def addCamera():
    body = request.get_data()
    body = json.loads(body)
    data = {'name': body.get('name'), 'rtsp': body.get('rtsp')}
    data = json.dumps(data)
    # 向数据库发送请求，分配id
    r = requests.post(DatabaseURL, data=data)
    print(r.text)
    r = r.json()
    data = {'id': r.get(id), 'name': body.get('name'), 'rtsp': body.get('rtsp')}
    requests.post(CalculateURL, data=data)


@app.route('/addPerson', methods=['POST'])
def addPerson():
    body = request.get_data()
    body = json.loads(body)
    data = {'name': body.get('name'), 'url': body.get('url')}
    requests.post(CalculateURL + '/addPerson', json=data)


@app.route('/deletePerson', methods=['POST'])
def deletePerson():
    body = request.get_data()
    body = json.loads(body)
    data = {'name': body.get('name')}
    requests.post(CalculateURL + '/deletePerson', json=data)


# @app.route("/stop_camera", methods=["POST"])
def stop_camera(v_id):
    global my_thread
    # v_id = request.get_json().get('vid')
    Recognize.flag = False
    print(v_id)
    # _async_raise(my_thread.ident, SystemExit)
    # 加新用户 将视频保存到TrainingVideo文件夹
    time.sleep(1)
    # Capture_Image.get_images_video()
    # Train_Image.TrainImages()
    #

    my_thread = threading.Thread(target=Recognize.recognize_attendence, args=(v_id,))
    my_thread.start()
    return "success"

@app.route("/recog", methods=["POST"])
def recog():
    global vid
    my_vid = request.get_json().get('vid')

    print('success')
    global my_thread
    # Recognize.recognize_attendence()
    my_thread = threading.Thread(target=Recognize.recognize_attendence, args=(my_vid))
    my_thread.start()
    data_thread = threading.Thread(target=save_data, args=())
    data_thread.start()
    time.sleep(1)
    vid = my_vid
    return "success"


def save_data():
    while True:
        global data_buffer
        data = Recognize.datas.copy()
        current_time = datetime.now()
        first_time = current_time + timedelta(minutes=-2)
        first_time_str = first_time.strftime('%Y-%m-%d %H:%M:%S')
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            data_buffer.pop(first_time_str)
        except Exception:
            s = 10
        data_buffer[current_time_str] = data
        time.sleep(1)


# @app.route('/send_record_video', methods=['POST'])
# def send_record_video():
#     header = request.headers
#     if calculate_token.check_token(header.get('Authorization').split(' ', 1, )[1]):
#         # 传输到数据库端
# 
#         my_json = request.get_json()
#         my_name = my_json.get("name")
#         return Response(gen_frames(my_name),
#                         mimetype='multipart/x-mixed-replace; boundary=frame'), 200, [
#                    ("Access-Control-Allow-Methods", "GET,POST,PUT"),
#                    ("Access-Control-Allow-Origin", header.get('Origin'))]
#     else:
#         data = jsonify({
#             "errorCode": "504",  # 业务约定的错误码
#             "errorMessage": "not match",  # 业务上的错误信息
#             "success": True  # 业务上的请求是否成功
#         })
#         return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
#                            ("Access-Control-Allow-Origin", header.get('Origin'))]
# 
# 
# def gen_frames(name):
#     camera = cv2.VideoCapture(name + '.mp4')
#     while True:
#         success, image = camera.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/record_list', methods=['GET'])
def record_list():
    header = request.headers
    if calculate_token.check_token(header.get('Authorization').split(' ', 1, )[1]):
        # 传输到数据库端
        total = 0
        path = 'D:/nginx-with-nginx-http-flv-module/server/record/'
        result_list = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            fileName = file_path.split('/')[-1]
            if fileName.split('.')[-1] == 'mp4':
                date = datetime.fromtimestamp(os.path.getctime(file_path))
                alg = hashlib.md5()
                alg.update(fileName.encode('utf-8'))
                listElement = {'id': fileName.split('_')[0],
                               'name': (fileName.split('.')[0]).split('_')[1],
                               'hash': alg.hexdigest(),
                               'href': 'http://' + ip + ':8192/record/' + fileName,
                               'time': (fileName.split('.')[0]).split('_')[2],
                               'desc': ''}
                result_list.append(listElement)
                total += 1

        return jsonify({'total': total,
                        'success':True,
                        'data': result_list}), 200, [
                   ("Access-Control-Allow-Methods", "GET,POST,PUT"),
                   ("Access-Control-Allow-Origin", header.get('Origin'))]
    else:
        data = jsonify({
            "errorCode": "504",  # 业务约定的错误码
            "errorMessage": "not match",  # 业务上的错误信息
            "success": True  # 业务上的请求是否成功
        })
        return data, 401, [("Access-Control-Allow-Methods", "GET,POST,PUT"),
                           ("Access-Control-Allow-Origin", header.get('Origin'))]


if __name__ == '__main__':
    # recog()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
    print("good")
    # my_thread2 = threading.Thread(target=app.run(threaded=True), args=())

    # my_thread2.start()
    #
