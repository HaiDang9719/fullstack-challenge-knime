import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatInputModule} from "@angular/material/input";
import {ReactiveFormsModule} from "@angular/forms";
import { FormsModule } from '@angular/forms';
import {MatButtonModule} from "@angular/material/button";
import { SearchBarComponent } from './search-bar/search-bar.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatIconModule} from "@angular/material/icon";
import { NodeCellComponent } from './node-cell/node-cell.component';
import {MatGridListModule} from "@angular/material/grid-list";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {LoaderInterceptor} from "./services/loader.interceptor";
import {MatCardModule} from "@angular/material/card";
import { EditNodeDialogComponent } from './dialogs/edit-node-dialog/edit-node-dialog.component';
import {MatDialogModule} from "@angular/material/dialog";
@NgModule({
  declarations: [
    AppComponent,
    SearchBarComponent,
    NodeCellComponent,
    EditNodeDialogComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    MatInputModule,
    ReactiveFormsModule,
    FormsModule,
    MatButtonModule,
    MatIconModule,
    MatGridListModule,
    MatCardModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [
    EditNodeDialogComponent,
    ]
})
export class AppModule { }
