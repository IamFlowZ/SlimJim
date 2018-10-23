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
#rm.remote_gpio_init()


@socketio.on('message')
def handle(msg):
    print(msg)
    print()

    for i in range(len(msg)): #For every value recieved from the client
        msg_obj = MessageModel(msg[i]['x'], msg[i]['y'])
        print("x: " + str(msg_obj.input['x']) + " y: " + str(msg_obj.input['y']))
        
        if msg_ojb.input['x'] >= 0: # Assigning motor priority to be used later
            msg_obj.output['prm_mtr'] = 'left'
            msg_obj.output['sec_mtr'] = 'right'
        else:
            msg_obj.output['prm_mtr'] = 'right'
            msg_obj.output['sec_mtr'] = 'left'

        # To make clear what each part does, I've included the parts of the circle that are solved with each condition.
        if abs(msg_obj.input['x']) <= abs(msg_obj.input['y']): # D. 2,3,6,7
            msg_obj.output['prm_mtr_spd'] = msg_obj.input['y']
            msg_obj.output['sec_mtr_spd'] = msg_obj.input['y'] - msg_obj.input['x']
        else:
            if msg_obj.input['y'] >= 0: #D. 1,4
                msg_obj.output['prm_mtr_spd'] = msg_obj.input['y']
                msg_obj.output['sec_mtr_spd'] = abs(msg_obj.input['x'])
            else:
                if msg_obj.input['x'] >= 0: #D. 8
                    msg_obj.output['prm_mtr_spd'] = msg_obj.input['y']
                    msg_obj.output['sec_mtr_spd'] = -(msg_obj.input['x'])
                else: #D. 5
                    msg_obj.output['prm_mtr_spd'] = msg_obj.input['y']
                    msg_obj.output['sec_mtr_spd'] = msg_obj.input['x']

        print("prm_mtr: " + str(msg_obj.output['prm_mtr_spd']) + " sec_mtr: " + str(msg_obj.output['sec_mtr_spd'])) 

        #print(str())
    #value = int(msg['velocity']) / 100
    #print(value)
    #if msg['heading'] == 'left':
        #rm.left(value)
    #elif msg['heading'] == 'right':
        #rm.right(value)
    #elif msg['heading'] == 'forward':
        #rm.forward(value)
    #elif msg['heading'] == 'backward':
        #rm.backward(value)
    #elif msg['heading'] == 'ping':
        #socketio.send('pong')
    #else:
        #print('Recieved something other than a direction: ' + msg)
        #return
        
    
socketio.run(app, port=9999)

    
