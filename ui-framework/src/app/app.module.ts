import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { DisplayTableComponent } from './display-table/display-table.component';
import { DisplayTextComponent } from './display-text/display-text.component';
import { HeaderComponent } from './header/header.component';
import { UploadComponent } from './upload/upload.component';
import { UserInputComponent } from './user-input/user-input.component';
import { AppRoutingModule } from './app.routes';
import { ChooseComponent } from "./choose/choose.component";
import { provideHttpClient } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    DisplayTableComponent,
    DisplayTextComponent,
    HeaderComponent,
    UploadComponent,
    UserInputComponent
  ],
  imports: [
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    ChooseComponent
],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent]
})
export class AppModule { }