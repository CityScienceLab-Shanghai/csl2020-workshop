import subprocess
from flask import Flask, jsonify, request, g, session
from flask_cors import CORS
from xml_utils import *
from xml.dom.minidom import parse
import xml.dom.minidom
from xmlTemplate import getXML
import json, re, os, signal, random, string
from datetime import timedelta
from redis import Redis, ConnectionPool
import pickle
import logging

proc = {}


class WSGICopyBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        from io import StringIO

        length = environ.get("CONTENT_LENGTH", "0")
        length = 0 if length == "" else int(length)

        body = environ["wsgi.input"].read(length)
        environ["body_copy"] = body
        environ["wsgi.input"] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)

        return callback


ROOT_PATH = "/home/ubuntu/GAMA/headless"
app = Flask(__name__)
CORS(app)

# pool = ConnectionPool(host='', port=6379)
# r = Redis(connection_pool=pool)

# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = r

app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

pattern_name = re.compile("people[0-9]+")
pattern_top6 = re.compile("landuse[0-9]+")
pattern_num = re.compile("[0-9]+\.[0-9]+")
# app.wsgi_app = WSGICopyBody(app.wsgi_app)


def stringfy(matched):
    return f'"{matched.group()}"'


def floatAccuracyContorl(matched):
    return f"{round(float(matched.group()), 6)}"


def getRandomString(length):
    return "".join(random.sample(string.ascii_letters + string.digits, length))


white = [
    "http://workshop.citysciencelabshanghai.media",
    "https://workshop.citysciencelabshanghai.media",
    "http://localhost:8080",
]


@app.after_request
def add_cors_headers(response):
    try:
        r = request.referrer[:-1]
    except:
        return response
    if r in white:
        response.headers.add("Access-Control-Allow-Origin", r)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Headers", "Cache-Control")
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
        response.headers.add("Access-Control-Allow-Headers", "Authorization")
        response.headers.add("Access-Control-Allow-Headers", "Set-Cookie")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        response.headers.add("Set-Cookie", "cross-site-cookie=bar; SameSite=None")
    return response


@app.route("/api/")
def check():
    return "OK"


def haveSession(session=session):
    if "sid" in session:
        return True
    else:
        return False


def getSession(session=session):
    if haveSession(session):
        print(session.get("sid"))
        p = session.get("sid")
        return f"{p}"
    else:
        session["sid"] = getRandomString(8)
        print(session.get("sid"))
        p = session.get("sid")
        return f"{p}"


@app.route("/api/get_session")
def getSession_debug(session=session):
    if haveSession(session):
        print(session.get("sid"))
        p = session.get("sid")
        return f"SSID: {p}"
    else:
        session["sid"] = getRandomString(8)
        print(session.get("sid"))
        p = session.get("sid")
        return f"New SSID: {p}"


@app.route("/api/clear_session")
def clearSession_debug(session=session):
    if haveSession(session):
        try:
            print(session.get("sid"))
            p = session.get("sid")
            session.pop("sid")
            return f"SSID {p} Cleared"
        except:
            return f"Session Clear Failed"
    return f"No Session to clear yet"


@app.route("/api/get_proc")
def getProc():
    global proc
    resp_dict = {"None": "Running", "0": "Ends Normally", "1": "Sleep", "2": "Process doesnt exsit", "-15": "Kill"}
    return str({k: [v, resp_dict[str(v.poll())]] for k, v in proc.items()})


@app.route("/api/status")
def checkStatus():
    global proc
    sid = getSession()
    if sid in proc.keys():
        if proc[sid].poll() is None:
            return "Running"
        return "Terminated"
    else:
        return "Terminated"


@app.route("/api/stop")
def kill():
    global proc
    if getSession() in proc.keys():
        if proc[getSession()].poll() is None:
            try:
                os.killpg(os.getpgid(proc[getSession()].pid), signal.SIGTERM)
                return "Killed"
            except:
                return "Failed"
    return "No Running Process"


@app.route("/api/start", methods=["POST", "GET", "OPTIONS"])
def RunSim():
    global proc
    sid = getSession()
    if request.method in ["GET", "OPTIONS"]:
        return "Please use POST method"
    else:
        body = json.loads(str(request.get_data().decode()))
        body["id"] = sid
        with open(f"{ROOT_PATH}/plans/CSS2020_{sid}.xml", "w") as f:
            f.write(getXML(**body))
        proc[sid] = subprocess.Popen(
            ["bash", f"{ROOT_PATH}/gama-headless.sh", f"{ROOT_PATH}/plans/CSS2020_{sid}.xml", f"{ROOT_PATH}/CSS2020"],
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        print(proc[sid].poll())
        return str(proc[sid].poll())


@app.route("/api/result")
def getResult():
    if checkStatus() == "Running":
        return "GAMA is runninng"
    sid = getSession()
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs{sid}.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, "Step")
    Result = {str(id): {} for id in range(1, 13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, "Variable")
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if "Loc" in getAttrValue(v, "name"):
                value = value.replace("location", "").replace(";", ",")
            if "ame" in getAttrValue(v, "name"):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace("people", "")
            if "top6" in getAttrValue(v, "name"):
                value = re.sub(pattern_top6, stringfy, value)
                value = value.replace("landuse", "")
            if "List" in getAttrValue(v, "name") or "top6" in getAttrValue(v, "name"):
                step_result[getAttrValue(v, "name")] = json.loads(value)
            else:
                step_result[getAttrValue(v, "name")] = value
        Result[getAttrValue(step, "id")] = step_result
    return jsonify(Result)


@app.route("/api/debug_result_full")
def getResult_debug_full():
    if checkStatus() == "Running":
        return "GAMA is runninng"
    sid = getSession()
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs{sid}.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, "Step")
    Result = {str(id): {} for id in range(1, 13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, "Variable")
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if "Loc" in getAttrValue(v, "name"):
                value = value.replace("location", "").replace(";", ",")
            if "ame" in getAttrValue(v, "name"):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace("people", "")
            if "top6" in getAttrValue(v, "name"):
                value = re.sub(pattern_top6, stringfy, value)
                value = value.replace("landuse", "")
            if "List" in getAttrValue(v, "name") or "top6" in getAttrValue(v, "name"):
                step_result[getAttrValue(v, "name")] = json.loads(value)
            else:
                step_result[getAttrValue(v, "name")] = value
        Result[getAttrValue(step, "id")] = step_result
    return jsonify(Result)


@app.route("/api/debug_start")
def startSim():
    status, output = subprocess.getstatusoutput(
        f"bash {ROOT_PATH}/gama-headless.sh {ROOT_PATH}/CSS2020.xml {ROOT_PATH}/CSS2020"
    )
    print(status, output)
    return output


@app.route("/api/debug_result_part")
def getResult_debug_part():
    if checkStatus() == "Running":
        return "GAMA is runninng"
    sid = getSession()
    DOMTree = xml.dom.minidom.parse(f"{ROOT_PATH}/CSS2020/simulation-outputs{sid}.xml")
    collection = DOMTree.documentElement
    Steps = getXMLNode(collection, "Step")
    Result = {str(id): {} for id in range(1, 13)}
    for step in Steps:
        step_result = {}
        Variables = getXMLNode(step, "Variable")
        for v in Variables:
            value = getNodeValue(v)
            value = re.sub(pattern_num, floatAccuracyContorl, value)
            if "Loc" in getAttrValue(v, "name"):
                value = value.replace("location", "").replace(";", ",")
            if "ame" in getAttrValue(v, "name"):
                value = re.sub(pattern_name, stringfy, value)
                value = value.replace("people", "")
            if "top6" in getAttrValue(v, "name"):
                value = re.sub(pattern_top6, stringfy, value)
                value = value.replace("landuse", "")
            if "List" in getAttrValue(v, "name") or "top6" in getAttrValue(v, "name"):
                step_result[getAttrValue(v, "name")] = json.loads(value)[:6]
            else:
                step_result[getAttrValue(v, "name")] = value
        Result[getAttrValue(step, "id")] = step_result
    return jsonify(Result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
