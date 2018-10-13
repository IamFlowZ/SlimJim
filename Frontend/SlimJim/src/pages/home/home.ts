import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import { NavController } from 'ionic-angular';
import { SocketService } from '../services/socketservice';
import { Input } from '../models/Input';
import { Output } from '../models/Output';

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
  Message: Output;// Object formatted for output
  Input: Input;// Object used to generate an Input value.
  OngoingTouches: Input[]; // Object storing touch events. Gets translated into MessageQueue.
  MessageQueue: Output[]; // Object that stores the collection of Inputs to be sent out.
  Joystick: any; // Object housing the html svg element
  offset: any; // Object used for Calculating touch event coordinates

  constructor(public navCtrl: NavController, private socketService:SocketService) {

    this.socketService.initSocket();

  }

  ngAfterContentInit() {
    this.Joystick = document.getElementById("JoystickBackground");

    // Calculating the Joystick elements offset
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
    this.MessageQueue = [];
  }

  public sendMessage(direction: string) { // Method that prepares and emits User Input to send to the relay server.
    console.log(direction);
    this.Message = {
      velocity: this.Velocity,
      heading: direction
    }
    console.log(JSON.stringify(this.Message));
    this.socketService.send(this.Message);
  }

  public setVelo(number: number) { // Method used by the ngForm for setting the velocity value
    this.Velocity = number;
    console.log(this.Velocity);
  }

  public copyTouch(touch) {
    return { identifier: touch.identifier, pageX: touch.pageX, pageY: touch.pageY };
  }

   handleStart = (event) => {
    this.Joystick.addEventListener("pointermove", this.handleMove, false);
  }

  handleMove = (event) => {
    this.Input = {
      x: event.pageX - (this.offset.x + 100),
      y: -(event.pageY - (this.offset.y + 100) - 137)
    }
    console.log("move: " + JSON.stringify(this.Input));
    this.OngoingTouches.push(this.Input);
    // console.log("OngoingTouches: " + JSON.stringify(this.OngoingTouches));
   }

   handleEnd = (event) => {
     this.Joystick.removeEventListener("pointermove", this.handleMove, false);
     console.log("lifted");


  }

  handleCancel = (event) => {
    this.Joystick.removeEventListener("pointermove", this.handleMove, false);
    console.log("canceled");

  }


}
