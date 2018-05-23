import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import {API_URL} from '../env';
import {Conversation} from './conversation.model';

@Injectable()
export class ConversationApiService {

//   private baseUri = API_URL;

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getConversations(): Observable<Conversation[]> {
    return this.http.get<Conversation[]>(`${API_URL}/getChatHistory`);
  }
}