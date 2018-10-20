import { Component } from '@angular/core';
import { HttpService } from './services/http.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'MEC 2018 - Group 94';

  constructor(private httpService: HttpService) {}

  private send(message: string) {
    this.httpService.sendMessage(message);

  }

}
