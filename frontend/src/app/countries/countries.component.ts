import { Component, OnInit, OnDestroy } from '@angular/core';
import { Country } from './country.model';
import { Subscription } from 'rxjs';
import { CountryApiService } from './country.service';

@Component({
  selector: 'app-countries',
  templateUrl: './countries.component.html',
  styleUrls: ['./countries.component.css']
})
export class CountriesComponent implements OnInit, OnDestroy   {

  constructor(private countryApi: CountryApiService) { }

  countryList: Country[];
  countryListSubs: Subscription;

  ngOnInit() {
    this.getCountryList();
  }

  ngOnDestroy(){
    this.countryListSubs.unsubscribe();
  }

  getCountryList(){
    this.countryListSubs = this.countryApi.getCountries().
    subscribe(res => {this.countryList = res;}, console.error);
  }

}
