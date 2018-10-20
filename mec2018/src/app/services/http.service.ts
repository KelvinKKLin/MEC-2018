import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private BACKEND_URL: string = "http://127.0.0.1:5000/";

  constructor(private http: HttpClient) { }

  public sendMessage(message: string) : Observable<string> {
    return this.http.post<string>(this.BACKEND_URL, message);
  }

}
