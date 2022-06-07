import { Component, OnInit } from '@angular/core';
import {FormControl} from "@angular/forms";
import {Observable} from "rxjs";
import {User} from "../app.component";
import {map, startWith} from "rxjs/operators";

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent implements OnInit {
  // @ts-ignore
  myControl = new FormControl<string | User>('');
  options: User[] = [{name: 'Mary'}, {name: 'Shelley'}, {name: 'Igor'}];
  filteredOptions: Observable<User[]> | undefined;
  abc = 'sabsdasd'
  constructor() { }

  ngOnInit() {
    // @ts-ignore
    this.filteredOptions = this.myControl.valueChanges.pipe(
      startWith(''),
      // @ts-ignore
      map(value => (typeof value === 'string' ? value : value.name)),
      // @ts-ignore
      map(name => (name ? this._filter(name) : this.options.slice())),
    );
  }
  displayFn(user: User): string {
    return user && user.name ? user.name : '';
  }

  private _filter(name: string): User[] {
    const filterValue = name.toLowerCase();

    return this.options.filter(option => option.name.toLowerCase().includes(filterValue));
  }

}
