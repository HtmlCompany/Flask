import  socket
import json
from datetime import datetime
from pathlib import Path
from threading import Thread
from flask import  Flask, render_template, request


SERVER_IP = '127.0.0.2'
SERVER_PORT = 3000
STORAGE = Path(r"E:\WEB\HW4\front-init\storage\data.json")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html', title="Home")


@app.route("/message", methods=['POST', 'GET'])
def message():
    if request.method == "POST":
        print(request.form['username'])
        print(request.form['message'])
        data = str(request.form['username']) + "," + str(request.form['message'])
        sent_to_server(data.encode())

    return render_template('message.html', title="Send message")


@app.errorhandler(404)
def error(e):
    return render_template("error.html")

def sent_to_server(data):
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.sendto(data, (SERVER_IP, SERVER_PORT))
    srv.close()

def start_server(ip=SERVER_IP, port=SERVER_PORT):
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.bind((ip, port))
    try:
        while True:
            connect, address = srv.recvfrom(1024)
            save_to_json(connect)
    except KeyboardInterrupt:
        srv.close()

def save_to_json(data):
    parser = data.decode()
    parser = parser.split(",")

    try:
        with open(STORAGE, 'r') as file:
            storage = json.load(file)
    except ValueError:
        storage = {}
    storage.update({str(datetime.now()): {"username": parser[0], 'message': parser[1]}})
    with open(STORAGE, "w") as file:
        json.dump(storage, file)

def main():
    if not STORAGE.exists():
        with open(STORAGE, 'w') as f:
            json.dump({}, f)
    thread_client = Thread(target=app.run)
    thread_server = Thread(target=start_server)
    thread_client.start()
    thread_server.start()


if __name__ == "__main__":
    main()
