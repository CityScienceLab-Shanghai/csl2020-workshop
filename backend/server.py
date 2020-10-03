import subprocess
from flask import Flask, jsonify, request, g
import json
from xml_utils import *
from xml.dom.minidom import parse
import xml.dom.minidom
from xmlTemplate import getXML
import json, re

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
pattern = re.compile("people[0-9]+")
# app.wsgi_app = WSGICopyBody(app.wsgi_app)

def stringfy(matched):
    return (f"\"{matched.group()}\"")

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

@app.route('/start', methods = ['POST', 'GET'])
def RunSim():
    global proc
    if request.method == 'GET':
        return 'Please use POST method'
    else:
        body = json.loads(str(request.get_data().decode()))
        with open(f"{ROOT_PATH}/CSS2020.xml","w") as f:
            f.write(getXML(**body))
        proc = subprocess.Popen(f'bash {ROOT_PATH}/gama-headless.sh {ROOT_PATH}/CSS2020.xml {ROOT_PATH}/CSS2020', shell=True, stdout=subprocess.PIPE)
        print(proc.poll())
        return str(proc.poll())

@app.route('/result')
def getResult2():
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs1.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, 'Step')
    Result = {str(id):{} for id in range(1,13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, 'Variable')
        for v in Variables:
            value = getNodeValue(v)
            if 'Loc' in getAttrValue(v, 'name'):
                value = value.replace('location','').replace(';',',')
            if 'ame' in getAttrValue(v, 'name'):
                value = re.sub(pattern, stringfy, value)
            if 'List' in getAttrValue(v, 'name'):
                step_result[getAttrValue(v, 'name')] = json.loads(value)
            else:
                step_result[getAttrValue(v, 'name')] = getNodeValue(v)
        Result[getAttrValue(step, 'id')] = step_result
    return jsonify(Result)

@app.route('/debug_start')
def startSim():
    status, output = subprocess.getstatusoutput(f'bash {ROOT_PATH}/gama-headless.sh {ROOT_PATH}/CSS2020.xml {ROOT_PATH}/CSS2020')
    print(status, output)
    return output

@app.route('/debug_result')
def getResult():
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs2.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, 'Step')
    Result = {str(id):{} for id in range(1,13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, 'Variable')
        for v in Variables:
            value = getNodeValue(v)
            if 'Loc' in getAttrValue(v, 'name'):
                value = value.replace('location','').replace(';',',')
            if 'ame' in getAttrValue(v, 'name'):
                value = re.sub(pattern, stringfy, value)
            if 'List' in getAttrValue(v, 'name'):
                step_result[getAttrValue(v, 'name')] = json.loads(value)
            else:
                step_result[getAttrValue(v, 'name')] = getNodeValue(v)
        Result[getAttrValue(step, 'id')] = step_result
    return jsonify(Result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

