import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import {API_URL} from '../env';
import {Country} from './country.model';

@Injectable()
export class CountryApiService {

  private countryUrl = API_URL;

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getCountries(): Observable<Country[]> {
    return this.http.get<Country[]>(`${API_URL}/getCountries`);
  }
}