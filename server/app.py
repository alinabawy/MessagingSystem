
from flask import Flask
from flask_socketio import SocketIO
from flask import Flask, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging-system-secret"

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return "hello, I am Ali and I'm testing if this works."

@socketio.on("connect")
def handle_connect():
    print("A client has connected!")


@socketio.on("disconnect")
def handle_disconnect():
    print("A client has disconnected.")

@socketio.on("send_message")
def handle_message(data):
    print("Message received:", data["message"])
    
    socketio.emit("receive_message", {
    "message": "Your message was received!"
}, to=request.sid)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
