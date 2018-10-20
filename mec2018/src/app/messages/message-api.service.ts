import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import {Message} from './message.model';
import { Observable } from 'rxjs';

@Injectable()
export class MessageApiService{
    constructor(private http: HttpClient) {
        
    }

    private static _handleError(err: HttpErrorResponse | any) {
        return Observable.throw(err.message || 'Error: Unable to complete request.');
    }

    sendMessage(to_number: string, text: string): Observable<Message[]> {
        const header = new HttpHeaders({
            'Content-Type': 'application/json'
        });

        return this.http.post<any>(
            "http://127.0.0.1:5000/send_text",
            JSON.stringify({"to":to_number, "text":text}),
            {headers: header}
          )
    }
}