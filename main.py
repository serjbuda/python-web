from flask import Flask, render_template, request, redirect, url_for, abort
import os
import socket
import json
from datetime import datetime
import threading

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/message", methods=["POST"])
def send_message():
    username = request.form.get("username")
    message = request.form.get("message")
    if username and message:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                data = {"username": username, "message": message}
                serialized_data = json.dumps(data).encode()
                sock.sendto(serialized_data, ("localhost", 5000))
        except socket.error:
            return abort(500)
    return redirect(url_for("index"))

@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(path):
        return app.send_static_file(path)
    else:
        return render_template('error.html'), 404

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        data = {'username': username, 'message': message}
        data_str = json.dumps(data).encode()
        sock.sendto(data_str, (HOST, PORT))
        return render_template('message_sent.html')
    else:
        return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 5000
    BUFFER_SIZE = 1024
    DATA_FILE = 'storage/data.json'
    http_server_thread = threading.Thread(target=app.run, kwargs={'host': 'localhost', 'port': 3000})
    http_server_thread.start()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            data_dict = json.loads(data)
            now = str(datetime.now())
            data_dict['timestamp'] = now
            with open(DATA_FILE, 'a') as f:
                json.dump({now: data_dict}, f)
                f.write('\n')


