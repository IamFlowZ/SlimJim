import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Observer} from 'rxjs/Observer';

import * as socketIO from 'socket.io-client';

  /* Socket service for handling connection to python webserver.
  *
  * Currently, connection is working. Error logging is working. None of the other things are. Something to do with the backend.
  * Either way I need to look through some more projects on how to setup ts websockets.
  *
  */

const SERVER_URL = "http://localhost:5000";

@Injectable()
export class SocketService {

  private socket;

  public initSocket() {
    this.socket = socketIO(SERVER_URL);
  }

  public send(message) {
    this.socket.emit('message', message);
  }

  public onMsg() {
    this.socket.on('message', (message) => {
      console.log(message.data);
    })
  }


}
