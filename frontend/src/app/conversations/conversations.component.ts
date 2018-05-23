import { Component, OnInit } from '@angular/core';
import { ConversationApiService } from './conversation.service';
import { Conversation } from './conversation.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-conversations',
  templateUrl: './conversations.component.html',
  styleUrls: ['./conversations.component.css']
})
export class ConversationsComponent implements OnInit {

  constructor(private convoApi: ConversationApiService) { }

  messageList: Conversation[];
  messageListSubs: Subscription;

  ngOnInit() {
    this.getConversationList();
  }
  
  ngOnDestroy(){
    this.messageListSubs.unsubscribe();
  }

  getConversationList(){
    this.messageListSubs = this.convoApi.getConversations().
    subscribe(res => {this.messageList = res;}, console.error);
  }

}
