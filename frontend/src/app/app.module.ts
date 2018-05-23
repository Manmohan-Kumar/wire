import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';

import { AppComponent } from './app.component';
import {CountryApiService} from './countries/country.service';
import { CountriesComponent } from './countries/countries.component'; 
import { FormsModule } from '@angular/forms'; 
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {
  MatAutocompleteModule,
  MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatCheckboxModule,
  MatChipsModule,
  MatDatepickerModule,
  MatDialogModule,
  MatExpansionModule,
  MatFormFieldModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatMenuModule,
  MatNativeDateModule,
  MatPaginatorModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatRippleModule,
  MatSelectModule,
  MatSidenavModule,
  MatSliderModule,
  MatSlideToggleModule,
  MatSnackBarModule,
  MatSortModule,
  MatTableModule,
  MatTabsModule,
  MatToolbarModule,
  MatTooltipModule,
  MatStepperModule,
  MatOptionModule,  
  MatBadgeModule,
  MatBottomSheetModule,  
  MatDividerModule,  
  MatTreeModule,
} from '@angular/material';
import { SidebarComponent } from './sidebar/sidebar.component';
import { ContactApiService } from './sidebar/contacts.service';
import { ChatComponent } from './chat/chat.component';
import { ConversationsComponent } from './conversations/conversations.component';
import { ConversationApiService } from './conversations/conversation.service';

@NgModule({
  declarations: [
    AppComponent,
    CountriesComponent,
    SidebarComponent,
    ChatComponent,
    ConversationsComponent
  ],
  imports: [
    BrowserModule, FormsModule,
    HttpClientModule,  
    BrowserAnimationsModule,    
    HttpClientModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDatepickerModule,
    MatDialogModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatMenuModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatRippleModule,
    MatSelectModule,
    MatSidenavModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatSnackBarModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTooltipModule,
    MatStepperModule,
    MatOptionModule,    
    MatBadgeModule,
    MatBottomSheetModule,
    MatDividerModule,
    MatTreeModule,    
  ],
  providers: [CountryApiService, ContactApiService, ConversationApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
