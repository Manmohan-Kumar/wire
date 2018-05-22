import { Component, OnInit, OnDestroy } from '@angular/core';
import {Contact} from './contact.model';
import { Subscription } from 'rxjs';
import { ContactApiService } from './contacts.service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {

  constructor(private contactApi : ContactApiService) { }

  contactList : Contact [];
  contactListSubs : Subscription;

  ngOnInit() {
    this.getContactList();
  }

  ngOnDestroy(){
    this.contactListSubs.unsubscribe();
  }

  getContactList(){
    this.contactListSubs = this.contactApi.getContacts().
    subscribe(res => {this.contactList = res;}, console.error);
  }

}
