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
  OngoingTouches: Input[]; // Object storing touch events. Gets translated into MessageQueue.
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
    this.OngoingTouches = [];

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
    this.OngoingTouches.push(this.Input);
    this.Joystick.addEventListener("pointermove", this.handleMove, false);
    const thing = setTimeout(this.emitTimeout, 500);
  }

  handleMove = (event) => {
    this.Input = {
      x: event.pageX - (this.offset.x + 100),
      y: -(event.pageY - (this.offset.y + 100) - 137)
    }
    console.log("move: " + JSON.stringify(this.Input));
    this.OngoingTouches.push(this.Input);

    if(this.OngoingTouches.length > 10) {
      console.log("sending from length");
      this.msgTimer = setInterval(this.socketService.send(this.OngoingTouches), 500);
      this.OngoingTouches = [];
    }

    // Checking to see if the last touch is within five of the last one. If it is, do nothing, else add it into the queue.
    // This can be removed if it causes too much lag.
    // if( Math.abs(this.Input.x - this.OngoingTouches[this.OngoingTouches.length-1].x) < 5 && Math.abs(this.Input.y - this.OngoingTouches[this.OngoingTouches.length-1].y) < 5 ) {}
    // else { this.OngoingTouches.push(this.Input); }
    // console.log("this.OngoingTouches: " + JSON.stringify(this.OngoingTouches));
   }

   handleEnd = (event) => {
     this.Joystick.removeEventListener("pointermove", this.handleMove, false);
     this.socketService.send(this.OngoingTouches);
     this.OngoingTouches = [];
     this.socketService.send(this.OngoingTouches);
     clearInterval(this.msgTimer);
     console.log("lifted");
  }

  handleCancel = (event) => {
    this.Joystick.removeEventListener("pointermove", this.handleMove, false);
    this.OngoingTouches = [];
    this.socketService.send(this.OngoingTouches);
    clearInterval(this.msgTimer);
    console.log("canceled");
  }

  emitTimeout() {
    this.timeout = true;
  }
}
