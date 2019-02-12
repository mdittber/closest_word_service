import os
import json
import logging
import requests
import flask
import flask_bootstrap


###   Helper function
def str2bool(v):
    v = v.lower()
    if v not in ('yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0'):
        raise ValueError('Entered Value is not correct, should be \'False\' or \'True\'')
    result = v.lower() in ("yes", "true", "t", "1")
    return(result)


###   Load environmetal variables
try:
    LOG_LEVEL = os.environ["LOG_LEVEL"]
    if(LOG_LEVEL == 'CRITICAL'):
        LOG_LEVEL = 50
    elif(LOG_LEVEL == 'ERROR'):
        LOG_LEVEL = 40
    elif(LOG_LEVEL == 'WARNING'):
        LOG_LEVEL = 30
    elif(LOG_LEVEL == 'INFO'):
        LOG_LEVEL = 20
    elif(LOG_LEVEL == 'DEBUG'):
        LOG_LEVEL = 10
    elif(LOG_LEVEL == 'NOTSET'):
        LOG_LEVEL = 0
    else:
        raise ValueError('Entered Value is not correct, should be CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET')
except KeyError:
    logging.error("Please set the environment variable LOG_LEVEL")
    sys.exit(1)
except ValueError as e:
    logging.error("Set the environment variable LOG_LEVEL correctly:", e)
    sys.exit(1)

try:
    LOG = os.environ["LOG"]
    FORMAT = '%(asctime)s %(message)s'
    if(LOG == 'CONSOLE'):
        logging.basicConfig(level=LOG_LEVEL,
                            format=FORMAT,
                            datefmt="%Y-%m-%d %H:%M:%S")
    else:
        logging.basicConfig(filename=LOG,
                            level=LOG_LEVEL, format=FORMAT,
                            datefmt="%Y-%m-%d %H:%M:%S",
                            maxBytes=1e6,
                            backupCount=10)
except KeyError:
    logging.error("Please set the environment variable LOG")
    sys.exit(1)

try:
    API_URL = os.environ["API_URL"]
except KeyError:
    logging.error("Please set the environment variable API_URL")
    sys.exit(1)

try:
    FLASK_HOST = os.environ["FLASK_HOST"]
except KeyError:
    logging.error("Please set the environment variable FLASK_HOST")
    sys.exit(1)

try:
    FLASK_PORT = int(os.environ["FLASK_PORT"])
except KeyError:
    logging.error("Please set the environment variable FLASK_PORT")
    sys.exit(1)

try:
    FLASK_DEBUGGING = os.environ["FLASK_DEBUGGING"]
    FLASK_DEBUGGING = str2bool(FLASK_DEBUGGING)
except KeyError:
    logging.error("Please set the environment variable FLASK_DEBUGGING")
    sys.exit(1)
except ValueError as e:
    logging.error("Set the environment variable FLASK_DEBUGGING correctly:", e)
    sys.exit(1)


###   Initialize Flask
app = flask.Flask(__name__)
flask_bootstrap.Bootstrap(app)

@app.route('/', methods=('GET', 'POST'))
def index():
    word  = None
    words = None
    N     = 10

    if flask.request.method == 'POST':
        payload = {}
        word            = flask.request.form["word"]
        payload["word"] = flask.request.form["word"]
        payload["N"]    = flask.request.form["N"]
        headers         = {'content-type': 'application/json'}
        r     = requests.post(API_URL, data=json.dumps(payload), headers=headers)
        data  = r.json()
        words = data["words"]

    return flask.render_template('index.html', word=word, words=words)


###   Start the server
try:
    if __name__ == "__main__":
        logging.info("Starting service with Flask ...")
        app.secret_key = os.urandom(12)
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUGGING)
    else:
        logging.info("Starting service with a WSGI server ...")
        app.secret_key = os.urandom(12)
except Exception as e:
    logging.error(str(e))
finally:
    logging.info("Stopping server")
