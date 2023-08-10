from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../frontend/')

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')