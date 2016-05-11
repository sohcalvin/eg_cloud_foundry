from flask import Flask
import os
import sys

app = Flask(__name__)
# api = Api(app)

@app.route('/', methods = ['POST', 'GET'])
def home():
    return "home success " ,200

if __name__ == '__main__':

    # port = int(os.getenv("VCAP_APP_PORT"))
    port = int(os.getenv("PORT", 9099))

    print("Running on")
    app.run(host='0.0.0.0', debug=True, port=port, threaded=True)
    # app.run(host='0.0.0.0' port=8080, debug=True)
