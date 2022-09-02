# -*- coding: utf-8 -*-
from flask import *
from logger import *

init_logger()

app = Flask(__name__)

@app.route("/") 
def index():
	return send_file("index.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0')