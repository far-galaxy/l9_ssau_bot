# -*- coding: utf-8 -*-
from flask import *
from vkbot import *
from sql import *
from logger import *
import requests
from ast import literal_eval

init_logger()
logger.info('Logger Ready. Initializating...')

app = Flask(__name__)

req = {}
req['client_id'] = VKBot.check_file("settings/client_id")
req['client_secret'] = VKBot.check_file("settings/client_secret")
req['redirect_uri'] = VKBot.check_file("settings/redirect_uri")

sql_pass = VKBot.check_file("settings/sql_pass")

db = Database("localhost","root",sql_pass)

@app.route("/") 
def index():
    return send_file("index.html")

@app.route("/lk") 
def lk():
    return send_file("joke.html")

@app.route('/<path:path>', methods=['GET'])
def get_files(path):
    try:
        if (path.find("style") != -1 or 
          path.find("media") != -1 or
        path.find(".html") != -1):
            return send_file(path)
        else:
            abort(404)
    except FileNotFoundError:
        abort(404)

@app.route('/auth', methods=['GET'])
def auth():
    if request.args.get('state') == "vk":
        code = request.args.get('code')
        req['code'] = code
        data = requests.get("https://oauth.vk.com/access_token", params=req)
        logger.info(data.content)
        if data.status_code == 200:
            data = data.json()
            user = getUser(data)
            
            if isinstance(user, list):
                user_query = """
                INSERT IGNORE INTO l9_users
                (l9Id, vkId, userName, userSurname, userPhotoUrl)
                VALUES (%s, %s, %s, %s, %s)
                """
    
                db.cursor.execute(user_query, user)
                db.database.commit()         
                return redirect("/lk")
            else:
                return user.content
        else:    
            return data.json()["error_description"]
        
    else:
        abort(501)

def getUser(data):
    user_req = {}
    user_req['v'] = '5.81'
    user_req['uids'] = data['user_id']
    user_req['access_token'] = data['access_token']
    user_req['fields'] = 'photo_big'
    user_data = requests.get("https://api.vk.com/method/users.get", params=user_req)
    logger.info(user_data.content)
    if user_data.status_code == 200:
        d = user_data.content.decode()
        user_data = literal_eval(d)['response'][0]

        user = [''] * 5
        user[0] = db.newID()
        user[1] = user_data['id']
        user[2] = user_data['first_name']
        user[3] = user_data['last_name']
        user[4] = user_data['photo_big']
        
        return user
    else:
        return user_data
        
  

if __name__ == "__main__":
    app.run(host='0.0.0.0')
