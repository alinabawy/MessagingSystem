
import socketio

sio = socketio.Client()
username = input("Enter your username: ")

@sio.event
def connect():
    print("Successfully connected to the server!")

    sio.emit("register", {"username": username})
    


@sio.on("receive_message")
def handle_message(data):
    print(f"{data['sender']} says: {data['message']}")

@sio.event
def disconnect():
    print("Disconnected from the server.")


sio.connect("http://192.168.100.28:5000")

while True:
    recipient = input("Who do you want to message? ")
    message = input("Enter your message: ")

    sio.emit("send_message", {
        "recipient": recipient,
        "message": message
    })