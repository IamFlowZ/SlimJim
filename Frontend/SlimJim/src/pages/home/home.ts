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

  Velocity: number = 0; // Test value for input objects
  message: Output;// Object formatted for output
  input: Input;// Object used to generate an input value.
  OngoingTouches: Input[] = [this.input]; // Object storing touch events. Gets translated into MessageQueue.
  MessageQueue: Output[] = [this.message]; // Object that stores the collection of inputs to be sent out.
  Joystick: any;

  constructor(public navCtrl: NavController, private socketService:SocketService) {

    this.socketService.initSocket();

  }

  ngAfterContentInit() {
    this.jsTouch();
    console.log(this.OngoingTouches);
  }

  public sendMessage(direction: string) { // Method that prepares and emits User input to send to the relay server.
    console.log(direction);
    this.message = {
      velocity: this.Velocity,
      heading: direction
    }
    console.log(JSON.stringify(this.message));
    this.socketService.send(this.message);
  }

  public setVelo(number: number) { // Method used by the ngForm for setting the velocity value
    this.Velocity = number;
    console.log(this.Velocity);
  }

  public copyTouch(touch) {
    return { identifier: touch.identifier, pageX: touch.pageX, pageY: touch.pageY };
  }

  public jsTouch() {
    this.Joystick = document.getElementById("JoystickBackground");
    console.log(this.Joystick);
    this.Joystick.addEventListener("pointerdown", this.handleStart, false);
    this.Joystick.addEventListener("pointermove", this.handleMove, false);
    this.Joystick.addEventListener("pointerup", this.handleEnd, false);
    this.Joystick.addEventListener("pointercancel", this.handleCancel, false);
  }

  public handleStart(event) {
    let touches = event.change;
    console.log("touch: " + JSON.stringify(this.input));
    this.input = {
      x: event.pageX,
      y: event.pageY
    }
    console.log(this.input);
    for(var i = 0; i < touches.length; i++) {
        this.OngoingTouches.push(this.copyTouch(touches[i]));
    }

    // touches.push(this.input);
    // console.log(JSON.stringify(this.OngoingTouches));
    // console.log(HomePage.OngoingTouches.length);

  }

  public handleEnd(event) {
    console.log("lifted");


  }

  public handleCancel(event) {
    console.log("cancelled");

  }

  public handleMove(event) {
    console.log("moved");

  }
}
