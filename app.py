from flask import Flask, request, json
from settings import *
import messageHandler

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello from Flask!"


@app.route(config['app']['vk']['posturi'], methods=["POST"])
def vk():
    data = json.loads(request.data)
    if "type" not in data.keys():
        return "not vk"
    if data["type"] == "confirmation":
        return config['confirmation_token']
    elif data["type"] == "message_new":
        messageHandler.create_answer(data["object"], config['token'], 0)
        return "ok"
    return "nothing"


@app.route(config['app']['tg']['posturi'], methods=["POST"])
def telegram():
    data = json.loads(request.data)
    if data.get("message"):
        messageHandler.create_answer(data["message"], config['app']['tg']['token'], 1)
        return "ok"
    return "nothing"


app.run(config['app']['host'], config['app']['port'])
