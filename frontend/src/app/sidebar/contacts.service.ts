import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import {API_URL} from '../env';
import {Contact} from './contact.model';

@Injectable()
export class ContactApiService {

  //private countryUrl = API_URL;

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getContacts(): Observable<Contact[]> {
    return this.http.get<Contact[]>(`${API_URL}/getContacts`);
  }
}