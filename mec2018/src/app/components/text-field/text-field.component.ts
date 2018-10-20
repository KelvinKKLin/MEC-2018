import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'text-field',
  templateUrl: './text-field.component.html',
  styleUrls: ['./text-field.component.css']
})
export class TextFieldComponent implements OnInit {

  @Input() enteredText: string;
  private NUM_CHARACTERS = 50;

  constructor() { }

  ngOnInit() {
  }

  private max(x, y) {
    if (x > y) return x;
    return y;
  }

  private getText(): string {
    let l = this.enteredText.length;
    return this.enteredText.substring(
      this.max(l-this.NUM_CHARACTERS,0),l
    );
  }
}
