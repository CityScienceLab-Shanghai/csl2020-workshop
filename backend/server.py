import subprocess
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from xml_utils import *
from xml.dom.minidom import parse
import xml.dom.minidom
from xmlTemplate import getXML
import json, re, os, signal

proc = None

class WSGICopyBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        from io import StringIO
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['body_copy'] = body
        environ['wsgi.input'] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback

ROOT_PATH = '/home/ubuntu/headless'
app = Flask(__name__)
CORS(app)
pattern_name = re.compile("people[0-9]+")
pattern_num = re.compile("[0-9]+\.[0-9]+")
# app.wsgi_app = WSGICopyBody(app.wsgi_app)

def stringfy(matched):
    return (f"\"{matched.group()}\"")

def floatAccuracyContorl(matched):
    return (f"{round(float(matched.group()), 6)}")

white = ['http://workshop.citysciencelabshanghai.media', 'https://workshop.citysciencelabshanghai.media']

@app.after_request
def add_cors_headers(response):
    try:
        r = request.referrer[:-1]
    except:
        return response
    if r in white:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response


@app.route('/')
def check():
    return 'OK'

@app.route('/status')
def checkStatus():
    global proc
    if proc:
        if proc.poll() is None:
            return "Running"
        return "Terminated"
    else:
        return "Terminated"

@app.route('/stop')
def kill():
    global proc
    if proc:
        if proc.poll() is None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                return "Killed"
            except:
                return "Failed"
    return "No Running Process"

@app.route('/start', methods = ['POST', 'GET', 'OPTIONS'])
def RunSim():
    global proc
    if request.method in ['GET', 'OPTIONS']:
        return 'Please use POST method'
    else:
        body = json.loads(str(request.get_data().decode()))
        with open(f"{ROOT_PATH}/CSS2020.xml","w") as f:
            f.write(getXML(**body))
        proc = subprocess.Popen(['bash', f'{ROOT_PATH}/gama-headless.sh', f'{ROOT_PATH}/CSS2020.xml', f'{ROOT_PATH}/CSS2020'], stdout=subprocess.PIPE, preexec_fn=os.setsid)
        print(proc.poll())
        return str(proc.poll())

@app.route('/result')
def getResult():
    if checkStatus() == 'Running':
        return 'GAMA is runninng'
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs1.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, 'Step')
    Result = {str(id):{} for id in range(1,13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, 'Variable')
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if 'Loc' in getAttrValue(v, 'name'):
                value = value.replace('location','').replace(';',',')
            if 'ame' in getAttrValue(v, 'name'):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace('people', '')
            if 'List' in getAttrValue(v, 'name'):
                step_result[getAttrValue(v, 'name')] = json.loads(value)
            else:
                step_result[getAttrValue(v, 'name')] = value
        Result[getAttrValue(step, 'id')] = step_result
    return jsonify(Result)

@app.route('/debug_result_full')
def getResult_debug_full():
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs1.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, 'Step')
    Result = {str(id):{} for id in range(1,13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, 'Variable')
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if 'Loc' in getAttrValue(v, 'name'):
                value = value.replace('location','').replace(';',',')
            if 'ame' in getAttrValue(v, 'name'):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace('people', '')
            if 'List' in getAttrValue(v, 'name'):
                step_result[getAttrValue(v, 'name')] = json.loads(value)
            else:
                step_result[getAttrValue(v, 'name')] = value
        Result[getAttrValue(step, 'id')] = step_result
    return jsonify(Result)

@app.route('/debug_start')
def startSim():
    status, output = subprocess.getstatusoutput(f'bash {ROOT_PATH}/gama-headless.sh {ROOT_PATH}/CSS2020.xml {ROOT_PATH}/CSS2020')
    print(status, output)
    return output

@app.route('/debug_result_part')
def getResult_debug_part():
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs1.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, 'Step')
    Result = {str(id):{} for id in range(1,13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, 'Variable')
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if 'Loc' in getAttrValue(v, 'name'):
                value = value.replace('location','').replace(';',',')
            if 'ame' in getAttrValue(v, 'name'):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace('people', '')
            if 'List' in getAttrValue(v, 'name'):
                step_result[getAttrValue(v, 'name')] = json.loads(value)[:5]
            else:
                step_result[getAttrValue(v, 'name')] = value
        Result[getAttrValue(step, 'id')] = step_result
    return jsonify(Result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

