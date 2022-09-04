# -*- coding: utf-8 -*-
from flask import *
from logger import *
from vk import *
from sql import *

init_logger()

app = Flask(__name__)

sql_pass = checkFile("settings/sql_pass")
db = L9LK(sql_pass)

@app.route("/") 
def index():
	return send_file("index.html")

@app.route("/lk") 
def lk():
	return send_file("joke.html")

@app.route('/<path:path>', methods=['GET'])
def get_files(path):
	try:
		if (path.find("js") != -1 or 
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
		success, token = getAcessToken(code)
		if success:
			success, user_data = getUserInformation(token)
			if success:
				logger.info(user_data)
				user_id = str(db.initVkUser(user_data))
				
				resp = make_response(redirect("/lk"))
				resp.set_cookie('userID', user_id)
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
	uid = request.args.get('l9Id')
	users = []
	for user in db.db.get("l9_users", f"l9Id = {uid}").fetchall():
		keys = ['l9Id','vkId','userName','userSurname','userPhotoUrl']
		users.append(dict(zip(keys, user)))
	return json.dumps(users, sort_keys = False)

if __name__ == "__main__":
	app.run(host='0.0.0.0')