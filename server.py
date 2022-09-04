# -*- coding: utf-8 -*-
from flask import *
from logger import *
from vk import *

init_logger()

app = Flask(__name__)

@app.route("/") 
def index():
	return send_file("index.html")

@app.route('/auth', methods=['GET'])
def auth():
	if request.args.get('state') == "vk":
		code = request.args.get('code')
		success, token = getAcessToken(code)
		if success:
			success, user_data = getUserInformation(token)
			logger.info(user_data)
			return 200
		else:
			abort(400, token)
	else:
		abort(501)	

if __name__ == "__main__":
	app.run(host='0.0.0.0')