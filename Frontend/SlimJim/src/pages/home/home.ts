import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import { NavController } from 'ionic-angular';
import { SocketService } from '../services/socketservice';
import { Input } from '../models/Input';

/*
     _    _  ____  __  __ ______
    | |  | |/ __ \|  \/  |  ____|
    | |__| | |  | | \  / | |__
    |  __  | |  | | |\/| |  __|
    | |  | | |__| | |  | | |____
    |_|  |_|\____/|_|  |_|______|

*/

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage implements OnInit{

  //Velocity: number = 0; // Test value for Input objects
  Input: Input;// Object used to generate an Input value.
  TouchBuffer: Input[]; // Object storing touch events. Gets translated into MessageQueue.
  Joystick: any; // Object housing the html svg element
  offset: any; // Object used for Calculating touch event coordinates
  msgTimer: any;
  timeout: boolean;


  constructor(public navCtrl: NavController, private socketService:SocketService) {

    this.socketService.initSocket();

  }

  ngAfterContentInit() {
    this.Joystick = document.getElementById("JoystickBackground");

    // Calculating the Joystick elements offset. Heavily inspired by https://stackoverflow.com/a/11396681
    let rect = this.Joystick.getBoundingClientRect();
    let body = document.body.getBoundingClientRect();
    let offset_x = rect.left - body.left;
    let offset_y = rect.top - body.top;
    this.offset = {
      x: offset_x,
      y: offset_y
    }
    console.log("offset: " + JSON.stringify(this.offset));

    // Adding the joystick event listeners
    this.Joystick.addEventListener("pointerdown", this.handleStart, false);
    this.Joystick.addEventListener("pointerup", this.handleEnd, false);
    this.Joystick.addEventListener("pointercancel", this.handleCancel, false);

    //Init for Queue(s)
    this.TouchBuffer = [];

  }

  // Someone said this might be useful. Leaving it here for now.
  // public copyTouch(touch) {
  //   return { identifier: touch.identifier, pageX: touch.pageX, pageY: touch.pageY };
  // }

   handleStart = (event) => {
    this.Input = {
      x: event.pageX - (this.offset.x + 100),
      y: -(event.pageY - (this.offset.y + 100) - 137)
    }
    this.TouchBuffer.push(this.Input);
    this.Joystick.addEventListener("pointermove", this.handleMove, false);
    const thing = setTimeout(this.emitTimeout, 500);
  }

  handleMove = (event) => {
    this.Input = {
      x: event.pageX - (this.offset.x + 100),
      y: -(event.pageY - (this.offset.y + 100) - 137)
    }
    console.log("move: " + JSON.stringify(this.Input));
    this.TouchBuffer.push(this.Input);

    if(this.TouchBuffer.length > 10) {
      console.log("Sending from buffer length");
      this.msgTimer = setInterval(this.socketService.send(this.TouchBuffer), 500);
      this.TouchBuffer = [];
    }

    // Checking to see if the last touch is within five of the last one. If it is, do nothing, else add it into the queue.
    // This can be removed if it causes too much lag.
    // if( Math.abs(this.Input.x - this.TouchBuffer[this.TouchBuffer.length-1].x) < 5 && Math.abs(this.Input.y - this.TouchBuffer[this.TouchBuffer.length-1].y) < 5 ) {}
    // else { this.TouchBuffer.push(this.Input); }
    // console.log("this.TouchBuffer: " + JSON.stringify(this.TouchBuffer));
   }

   handleEnd = (event) => {
     this.Joystick.removeEventListener("pointermove", this.handleMove, false);
     console.log("Sending leftovers in TouchBuffer");
     this.socketService.send(this.TouchBuffer);
     this.TouchBuffer = [];
     console.log("Sending empty buffer to stop actions");
     this.socketService.send(this.TouchBuffer);
     clearInterval(this.msgTimer);
     console.log("lifted");
  }

  handleCancel = (event) => {
    this.Joystick.removeEventListener("pointermove", this.handleMove, false);
    this.TouchBuffer = [];
    this.socketService.send(this.TouchBuffer);
    clearInterval(this.msgTimer);
    console.log("canceled");
  }

  emitTimeout() {
    this.timeout = true;
  }
}
