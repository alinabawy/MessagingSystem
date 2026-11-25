
import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Successfully connected to the server!")

    sio.emit("send_message", {
        "message": "Hello server!"
    })

    
@sio.on("receive_message")
def handle_message(data):
    print("Server says:", data["message"])

@sio.event
def disconnect():
    print("Disconnected from the server.")


sio.connect("http://192.168.100.28:5000")

sio.wait()
