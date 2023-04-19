import os
import base64
import requests
import base64
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
    request_body = request.get_json()
    path = request_body['path']
    encoded_string = ""
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
    except:
        pass
    bmp_base64String = 'data:image/bmp;base64,' + encoded_string.decode('utf-8')
    return jsonify({'base64': bmp_base64String})

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
   app.run(host="0.0.0.0")