from flask import Flask
import os
import sys
import re

from pymongo import MongoClient, TEXT
import json
app = Flask(__name__)
# api = Api(app)

def envEval(env_name) :
    val = os.environ.get(env_name)
    if(val is None) : return None
    match = re.match(r'^\${(.*)}', val)
    if(match is not None) :
        group1 = str(match.group(1))
        val = os.environ.get(group1)
        return val
    if(re.match(r'^eval *:',val, flags=re.IGNORECASE)) :
        nval = re.sub(r'^eval *:', '', val,flags=re.IGNORECASE)
        nval = re.sub(r'json.loads','__import__("json").loads', nval) # Manually map allowable modules for safety
        nval = re.sub(r'os.environ','__import__("os").environ', nval)
        return eval(nval,{})
    return val


def envMongodbHostPort():
        envHost = envEval("MONGODB_HOST")
        envPort = envEval("MONGODB_PORT")
        try :
            if(envPort is not None ) :
                envPort = int(envPort)
        except Exception as e :
            envPort = None
            logger.error("Unable to convert envPort from '{0}' to integer".format(envPort))
        return envHost, envPort

def envMongodbUsernamePassword():
        envUsername = envEval("MONGODB_USERNAME")
        envPassword = envEval("MONGODB_PASSWORD")
        envAuthDb = envEval("MONGODB_AUTH_DB")
        return envUsername, envPassword, envAuthDb

uri = envEval("MONGODB_URI")
client = MongoClient(uri)
db = client.cvr_db
# db.fruit.insert({"apple" : "red"})
# print(">>>>>>>>ssss>>", db.fruit.find())

#
# (envHost, envPort) = envMongodbHostPort()
# if(envHost is not None and envPort is not None) :
#             host = envHost
#             port = envPort
# client = MongoClient(host, port, maxPoolSize=200)
#
#
#
#
# db = client["cvr_db"]
# (envUsername, envPassword, envAuthDb) = envMongodbUsernamePassword()
# if(envUsername is not None and envPassword is not None, envAuthDb is not None) :
#         print(">>>>> Authenticating with dbname:", envAuthDb)
#         db.authenticate(envUsername, envPassword, source=envAuthDb)
#
# db.add_user('newTestUser', roles=[{'role':'readWrite','db':'cvr_db'}])

# print(self.db.admin.find())
db.cv.create_index([("raw_content", TEXT)])
print(">>>>>>>xxxx")
        # self.db.job.create_index([("title", TEXT), ("description", TEXT)])
        # self.db.rec_cache.create_index("createdAt", expireAfterSeconds=10*60)
        # self.fs = gridfs.GridFS(self.db)
        # self.bu =BatchQueueUtil(self.db)

@app.route('/', methods = ['POST', 'GET'])
def home():
    host = os.environ.get('VCAP_SERVICES')
    host= json.loads(json.dumps(host))
    host =envEval('MONGODB_HOST')
    port = 27017
    db_name = "cvr_db"
    job_data=""
    try :
      print("----------->>>>")
      output = type(host)
      #output = os.popen('ping -c 1 ' + host).read()
      #print(output)
      #db = MongoClient(host, port, maxPoolSize=200)[db_name] 
      #job_data = db.job.find_one({"title": 'Software Developer'})
      #print(">>>", job_data)
    except Exception as e :
      print(">>>>>>>>>>>>>>>>>>>")
      print(e)
    return "home success {0}<hr> {1}<hr>{2}".format(output, os.environ, host) ,200

if __name__ == '__main__':

    print(">>>>>>>>>>>>")
    print(os.path.isfile(".cvr.properties"))
    for index, each in enumerate(sorted(os.environ.items())):
                       print(index, each)

    # port = int(os.getenv("VCAP_APP_PORT"))
    port = int(os.getenv("PORT", 9099))

    print("Running on")
    app.run(host='0.0.0.0', debug=True, port=port, threaded=True)
    # app.run(host='0.0.0.0' port=8080, debug=True)
