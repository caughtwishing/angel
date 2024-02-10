import secrets
import socket
from flask import Flask, request, render_template
from utils.funcs import *
from mines.algorithm import *
from mines.rand import *
import time
import secrets
import datetime
from functools import wraps
from crash import crash
from roulette import roulette
# ADMIN KEY: 3kD9aR8tLp7s2jN6wG5hQ1yPxM4cV0iB2oF8uS7nR


# flask stuff
app = Flask(__name__)
host = socket.gethostbyname(socket.gethostname())
port = 5000
# flask stuff

# main utilities
time_start = time.time()
limits = {}
app.secret_key = secrets.token_hex(64)
# main ulitieis

def simple_limit(limit):
    def wrapper(f):
        @wraps(f)
        def limiter(*args,**kwargs):
            ip = request.environ['REMOTE_ADDR']
            if ip in limits:
                time_now = datetime.datetime.now()
                time = limits[ip]['time']
                if time_now-time < datetime.timedelta(minutes=2) and limits[ip]['c'] > limit:
                    return jsonify({"msg": "rate limit", "errors": ["rate_limit"]})
                else:
                    limits[ip]['c'] += 1
            else:
                limits[ip] = {"time": datetime.datetime.now(),"c": 1}
            return f(*args,**kwargs)
        return limiter
    return wrapper

@app.route('/uptime',methods=["GET"])
@simple_limit(limit=5)
def uptime():
    return jsonify({"uptime": time.time() - time_start})

@app.route('/api/crash', methods=['GET'])
def crashapi():
    key = request.args.get('key')
    if checkKey(key):
        prediction = crash.Prediction.predict()
        return jsonify({'result': 'True', 'prediction': prediction})
    else:
        return jsonify({'result': 'False'})
    
@app.route('/api/roulette', methods=['GET'])
def rouletteapi():
    key = request.args.get('key')
    if checkKey(key):
        prediction = roulette.Prediction.predict()
        return jsonify({'result': 'True', 'prediction': prediction})
    else:
        return jsonify({'result': 'False'})

@app.route('/api/mines/algo', methods=['GET'])
def mines():
    key = request.args.get('key')
    clicked = request.args.get('clicked')
    mines = request.args.get('mines')
    boom = request.args.get('safeSpots')
    if checkKey(key):
        prediction = Algorithm().predict(clicked, mines, boom)
        return jsonify({"msg": "success", "prediction": prediction})
    else:
        return jsonify({"msg": "invalid key","errors": ["invalid_key"]})

@app.route('/api/mines/random', methods=['GET'])
def minesrand():
    key = request.args.get('key')
    safe = request.args.get('safe')
    if checkKey(key):
        board = sigma.predict(safe)
        return jsonify({"msg": "prediction complete", "board": board})
    else:
        return jsonify({"msg": "invalid key","errors": ["invalid_key"]})

@app.route('/api/createKey', methods=['POST'])
@simple_limit("5 per minute")
def create_key():
    userid = request.args.get('userid')
    admin_key = request.args.get('adminkey')
    return createKey(userid,admin_key)

@app.route('/api/checkKey', methods=['GET'])
@simple_limit("5 per minute")
def check_if_valid():
    key = request.args.get('key')
    if checkKey(key):
        return jsonify({"msg": "valid key","errors": ["valid_key"]})
    else:
        return jsonify({"msg": "invalid key", "errors": ["invalid_key"]})
    

if __name__ == "__main__":
    app.run()
