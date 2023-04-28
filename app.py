import os
import base64
import requests
import base64
import io
from io import BytesIO
from PIL import Image
from requests_toolbelt.multipart import decoder

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/getBase64FromBmp', methods=['POST'])
def getBase64FromBmp():
    print('request came here 1')
    request_body = request.get_json()
    path = request_body['path']
    encoded_string = ""
    size = 300, 300
    try:
        print('request came here 2')
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print('request came here 3')
        data2 = encoded_string.decode()
        imagedata = base64.b64decode(data2)
        print('request came here 4')
        buf = io.BytesIO(imagedata)
        img = Image.open(buf)
        print('request came here 5')
        print('original size = ',img.size)
        img.thumbnail(size, Image.ANTIALIAS)
        print('new size = ',img.size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        encoded_string = base64.b64encode(buffered.getvalue())
    except Exception as e:
        print(e)
        pass
    bmp_base64String = 'data:image/png;base64,' + encoded_string.decode('utf-8')
    return jsonify({'base64': bmp_base64String})

@app.route('/getPaths')
def getPaths():
    data = ""
    try:
        with open('C:\offlineScreenshots.txt', 'r') as file:
            data = file.read().replace('\\', '/')
    except:
        pass    
    print('data read from file: ' + data)
    return jsonify({'paths': data})

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()