from flask import Flask, render_template
from flask_socketio import SocketIO

class socketIO:
    def __init__(self):
        app = Flask()
        app.config['SECRET_KEY'] = 'mysecret'
        socketio = SocketIO(app)

        @socketio.on('message')
        def handle(msg):
            print('Message: ' + msg)
   
        socketio.run(app)
