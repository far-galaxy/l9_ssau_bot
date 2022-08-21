from flask import *
from vkbot import *
import requests

app = Flask(__name__)

req = {}
req['client_id'] = VKBot.check_file("settings/client_id")
req['client_secret'] = VKBot.check_file("settings/client_secret")
req['redirect_uri'] = VKBot.check_file("settings/redirect_uri")

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
    code = request.args.get('code')
    req['code'] = code
    data = requests.get("https://oauth.vk.com/access_token", params=req)
    if data.status_code == 200:
        data = data.json()
        user_req = {}
        user_req['v'] = '5.81'
        user_req['uids'] = data['user_id']
        user_req['access_token'] = data['access_token']
        user_req['fields'] = 'photo_big'
        user_data = requests.get("https://api.vk.com/method/users.get", params=user_req)
        if user_data.status_code == 200:
            return str(user_data.json())
    return "Ошибка"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
