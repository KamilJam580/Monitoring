import shutil

total, used, free = shutil.disk_usage("/")

print("Total: %d MiB" % (total // (2**20)))
print("Used: %d MiB" % (used // (2**20)))
print("Free: %d MiB" % (free // (2**20)))



from Camera import Camera
import time
import cv2

devices = Camera.getDevicesList()
print(devices)

i=0
Cameras = []
for device in devices:
    Cameras.append(Camera(i))
    i=i+1
time.sleep(1)

print("Ilość kamer: " + str(len(Cameras)))

import threading

### REST
from flask import render_template, Response
from flask import Flask, jsonify
from flask import abort
from flask import request

Login = "kamil"
Password = "123"

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

restAppi = Flask(__name__)
def gen(task_id):
    while True:
        print("Thread runned " + str(task_id))
        #get camera frame
        img = Cameras[task_id].getImg()
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@restAppi.route('/video_feed/<int:task_id>')
def video_feed(task_id):
    #print(task_id)
    return Response(gen(task_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@restAppi.route('/camerasPreview', methods=['GET'])
def camerasPreview():
    login = category = request.args.get('login')
    password = content_id = request.args.get('password')
    print(login)
    print(password)
    if (login == Login) and password == Password:
        return render_template("CamerasPreview.html", name = "Kamil", camerasCount = len(Cameras))
    else: abort(401);

@restAppi.route('/')
def index():
    return render_template("index.html")

@restAppi.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@restAppi.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

restAppiRunned = False
if __name__ == "__main__":
    threading.Thread(target=restAppi.run(debug=False)).start()

#if __name__ == '__main__':
   # restAppi.run(debug=False)

