###################################################################################
#                                                                                 #
# This is a relay server enabling clients to remotely connect to a raspberry pi   #
# configured with motors and a camera meant to be controlled by the gpio library  #
# inside of this application                                                      #
#                                                                                 #
###################################################################################


from flask import Flask, render_template
from flask_socketio import SocketIO, send
from remote_gpio import Remote_GPIO as rem_gpio
from MessageModel import *


# Main loop
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
rm = rem_gpio()
rm.remote_gpio_init()


@socketio.on('message')
def handle(msg):
    print(msg)
    print()
    #m_msg = MessageModel(msg['heading'], msg['velocity'])
    #heading = msg['heading']
    #value = int(msg['velocity']) / 100
    #print(value)
    #if heading == 'left':
        #rm.left(value)
    #elif heading == 'right':
        #rm.right(value)
    #elif heading == 'forward':
        #rm.forward(value)
    #elif heading == 'backward':
        #rm.backward(value)
    #elif heading == 'ping':
        #socketio.send('pong')
    #else:
        #print('Recieved something other than a direction: ' + msg)
        #return
        
    
socketio.run(app, port=9999)

    
