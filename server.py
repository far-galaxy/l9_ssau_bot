# -*- coding: utf-8 -*-
from flask import *
from logger import *
from vk import *
from sql import *
from utils import *
import requests
from ast import literal_eval

app = Flask(__name__)

init_logger(app.logger)

sql_pass = checkFile("settings/sql_pass")
db = L9LK(sql_pass)

md5_key = checkFile("settings/md5_key")
push_key = checkFile("settings/push_key")

subs = set(literal_eval(checkFile("settings/subs")))

@app.route("/") 
def index():
	return send_file("index.html")

@app.route("/stuff") 
def stuff():
	page = request.args.get('page')
	if page == None:
		return send_file("stuff/index.html")
	else:
		return send_file("stuff/video.html")

@app.route('/files/<path:path>', methods=['GET'])
def stuff_files(path):
	try:
		return send_file("stuff/files/"+path)
	except FileNotFoundError:
		abort(404)

@app.route('/stuff/likes', methods=['GET'])		
def get_likes():
	return str(checkFile("stuff/likes"))

@app.route('/stuff/like', methods=['GET'])		
def add_like():
	likes = checkFile("stuff/likes")
	likes += 1
	writeFile("stuff/likes", str(likes))
	return str(likes)


@app.route('/bot/subscribe', methods=['GET'])	
def subscribe():
	try:
		token = request.args.get("token")
		subs.add(token)
		writeFile("settings/subs", str(subs))
		return "ok"
	except  Exception as e:
		app.logger.error("Exception occurred\n", exc_info=True)
		return abort(401)
	
@app.route('/bot/notify')#, methods=['POST'])	
def notify():
	key = request.args.get("key")
	if key == sql_pass:
		head = {
		"Authorization": f"key={push_key}",
		"Content-Type": "application/json"
		}
		data = {
			"notification": {
				"title": "l9labs",
				"body": "Уведомление от бота",
				"click_action": "http://l9labs.ru/"
				},
			"registration_ids": subs
		}
		req = requests.post("https://fcm.googleapis.com/fcm/send", headers=head, params=data)
		
		return str(req.status_code)
	else:
		abort(401)
	
		
@app.route("/lk") 
def lk():
	if "session_token" in request.cookies:
		return send_file("joke.html")
	else:
		return redirect("/")

@app.route('/<path:path>', methods=['GET'])
def get_files(path):
	try:
		if (path.find("js") != -1 or 
		    path.find("media") != -1 or
			path.find("robots.txt") != -1 or
			path.find("favicon.ico") != -1 or
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
		success, token = getAcessToken(code)
		if success:
			success, user_data = getUserInformation(token)
			if success:
				logger.info(user_data)	
				user_id = str(db.initVkUser(user_data))
				
				session_token = hashMD5(md5_key + user_id)
				
				db.db.update("l9_users", 
							 f"l9Id = {user_id}", 
							 f"sessionToken = '{session_token}'")
				
				resp = make_response(redirect("/lk"))
				resp.set_cookie('session_token', session_token)
				return resp
			else:
				logger.error(user_data)
				abort(401, token)				
		else:
			logger.error(token)
			abort(401, token)
	else:
		abort(501)	
		
@app.route('/api/lk/users.get', methods=['GET'])
def usersGet():
	if ("session_token" in request.cookies):
		uid = db.db.get("l9_users", 
						f"sessionToken = '{request.cookies['session_token']}'",
						["l9Id"]).fetchall()[0][0]
		users = []
		for user in db.db.get("l9_users", f"l9Id = {uid}").fetchall():
			keys = ['l9Id','vkId','userName','userSurname','userPhotoUrl']
			users.append(dict(zip(keys, user)))
		return json.dumps(users, sort_keys = False)
	else:
		abort(401)

if __name__ == "__main__":
	app.run(host='0.0.0.0')