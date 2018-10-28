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
socketio = SocketIO(app, cors_allowed_origins="10.0.0.153")
rm = rem_gpio()
rm.remote_gpio_init()


@socketio.on('message')
def handle(msg):
    print(msg)
    print()

    # I know this is jank af. However I spent a lot of effort figuring out the above, before I knew of the forward AND backward commands
    # So this is my making due, before I drop this pos all together.
    # I might refactor this some day. But if you're a human other than me. Feel free to fix this shit.
    
    if len(msg) > 0:
        for i in range(len(msg)): #For every value recieved from the client
            msg_obj = MessageModel(msg[i]['x'], msg[i]['y'])
            print("x: " + str(msg_obj.input['x']) + " y: " + str(msg_obj.input['y']))
            
            if msg_obj.input['x'] >= 0: # Assigning motor priority to be used later
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

            
            if msg_obj.output['prm_mtr'] == 'left' and msg_obj.output['prm_mtr_spd'] > 0:
                rm.motor_left.forward(msg_obj.output['prm_mtr_spd'] / 100)
                rm.motor_right.forward(msg_obj.output['sec_mtr_spd'] / 100)
            elif msg_obj.output['prm_mtr'] == 'right' and msg_obj.output['prm_mtr_spd'] > 0:
                rm.motor_right.forward(msg_obj.output['prm_mtr_spd'] / 100)
                rm.motor_left.forward(msg_obj.output['sec_mtr_spd'] / 100)
            elif msg_obj.output['prm_mtr'] == 'left' and msg_obj.output['prm_mtr_spd'] < 0:
                rm.motor_left.backward(-(msg_obj.output['prm_mtr_spd']) / 100)
                rm.motor_right.backward(-(msg_obj.output['sec_mtr_spd']) / 100)
            elif msg_obj.output['prm_mtr'] == 'right' and msg_obj.output['prm_mtr_spd'] < 0:
                rm.motor_right.backward(-(msg_obj.output['prm_mtr_spd']) / 100)
                rm.motor_left.backward(-(msg_obj.output['sec_mtr_spd']) / 100)
    else:
        print("recieved lift")
        rm.motor_left.stop()
        rm.motor_right.stop()
        


        
    
socketio.run(app, port=9999)

    
