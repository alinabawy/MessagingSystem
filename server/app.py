
from flask import Flask, request
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging-system-secret"

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return ":)"

connected_clients = {}


@socketio.on("connect")
def handle_connect():
    print("A client has connected!")
    print("Client ID:", request.sid)
    print(connected_clients)


@socketio.on("register")
def handle_register(data):
    username = data["username"]
    connected_clients[request.sid] = username

    print(f"{username} registered!")
    print(connected_clients)


@socketio.on("disconnect")
def handle_disconnect():
    print("A client has disconnected.")
    connected_clients.pop(request.sid, None)
    print(connected_clients)


@socketio.on("send_message")
def handle_message(data):
    recipient = data["recipient"]
    message = data["message"]
    recipient_sid = None #We need a variable to store the recipient sid in

    for sid, username in connected_clients.items(): #connected clients needs two variables in the for loop, because it is a dictionary which is stored in key:value entries. In thsi case: sid,username represents key:value
        if username == recipient: ##so when we find a username that matches with the recipient we have
            recipient_sid = sid ##we see the current sid we are standing on and then copy it into the variable we made earlier
            break
    if recipient_sid is None:
        print("Recipient not found!") #if recipient sid remains None, then we couldnt find any matching recipient name when looping through the connected clients dictionary
    else:
        socketio.emit("receive_message", { #else, if we found a match, we trigger the recieve message event
            "message": message, #and send the message 
            "sender": connected_clients[request.sid] #store the sender's sid
        }, to=recipient_sid) #to the reciepent with the matching sid

    print(f"Message from {connected_clients[request.sid]} to {recipient}: {message}") 

    #socketio.emit("receive_message", {
    #"message": "Your message was received!" 
#}, to=request.sid) //These three lines are now reduntant, since thye were only a test to see if the server can speak to the client, now we actually make two clients talk to each other using the server as the medium


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
