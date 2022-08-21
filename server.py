from flask import * 
app = Flask(__name__)

@app.route("/") 
def index():
   return send_file("index.html")

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
  
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')
