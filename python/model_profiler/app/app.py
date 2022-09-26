from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

from model_profiler.app.views.time_record import time_profile_blue
app.register_blueprint(time_profile_blue)

if __name__ == '__main__':
    app.run(debug=True, host='133.133.135.71', port=8088)