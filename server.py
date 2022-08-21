from flask import * 
app = Flask(__name__) 
@app.route("/") 
def index():
   return "Hello l9labs"
  
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')
