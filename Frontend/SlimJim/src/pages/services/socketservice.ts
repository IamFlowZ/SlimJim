import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {Observer} from 'rxjs/Observer';

import * as socketIO from 'socket.io-client';

/*
*  _________                 __              __     _________
* /   _____/  ____    ____  |  | __  ____  _/  |_  /   _____/___  __  ____
* \_____  \  /  _ \ _/ ___\ |  |/ /_/ __ \ \   __\ \_____  \ \  \/ /_/ ___\
* /        \(  <_> )\  \___ |    < \  ___/  |  |   /        \ \   / \  \___
* /________/ \____/  \_____>|__|__\ \_____> |__|  /_________/  \_/   \_____>
*
*/

/*
* Cross origin isn't working, and I suspect it's coming from here. Because when both sides are local, everything checks out.
*  Switch the backend onto the rpi, can't make a connection. Python's implementation allows CORS by default, soooo...
* const SERVER_URL = "http://10.0.0.212:9999"; is a no-go.
*/

  const SERVER_URL = "http://10.0.0.212:8080";

@Injectable()
export class SocketService {

  private socket;

  initSocket() {
    this.socket = socketIO(SERVER_URL);
    //this.socket.set('origins', 'http://10.0.0.212:9999');
    //this.socket.

  }

  send(message) {
    this.socket.emit('message', message);
  }

  onMsg() {
    this.socket.on('message', (message) => {
      console.log(message.data);
    })
  }

  onCamFtg() {
    this.socket.on('cam data', (data) => {
      return data;
    })
  }

}
