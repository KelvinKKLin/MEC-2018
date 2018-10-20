import { Component, OnInit } from '@angular/core';
import { KeyboardOptions } from 'virtual-keyboard';
//import * as $ from 'jquery';

const $ = jQuery;
const options: KeyboardOptions = {
  type: "text",
  css: {
    container: 'ui-keyboard'
  }
};

@Component({
  selector: 'keyboard',
  templateUrl: './keyboard.component.html',
  styleUrls: ['./keyboard.component.css']
})
export class KeyboardComponent implements OnInit {

  constructor() { }

  ngOnInit() {
    $("#keyboard").keyboard(options);
  }

}
