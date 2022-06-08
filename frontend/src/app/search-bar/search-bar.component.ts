import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl} from "@angular/forms";
import {forkJoin, Observable, ReplaySubject, Subject} from "rxjs";
import {map, startWith, take} from "rxjs/operators";
import {InfoNode} from "../interfaces/node";
import {SearchNodeService} from "../services/search-node.service";
import {MatAutocompleteTrigger} from "@angular/material/autocomplete";
import {MatDialog} from "@angular/material/dialog";
import {EditNodeDialogComponent} from "../dialogs/edit-node-dialog/edit-node-dialog.component";

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent implements OnInit {
  // @ts-ignore
  myControl = new FormControl<string | User>('');
  optionTexts: string[] = [];
  optionTags: string[] = [];
  optionNodes: InfoNode[] = [];
  testOptions: InfoNode[] = [{name: 'Mary', tag: 'abc', group: 'bcd', description: 'test', record_id: '1'}];
  allOptions$:  Subject<any> = new ReplaySubject<any>();
  filteredOptionsObservable: Observable<string> | undefined;
  filteredOptions$: Subject<any> = new ReplaySubject<any>(1);
  filteredOptions:  InfoNode[] = [];
  searchValue: string = '';
  @ViewChild('autoTrigger', {static: false, read: MatAutocompleteTrigger }) autoTrigger: MatAutocompleteTrigger | undefined;
  constructor(private searchNodeService: SearchNodeService, public dialog: MatDialog) { }

  ngOnInit() {
    this.searchNodeService.getAllNodeInformation().subscribe((res: any) => {
      this.allOptions$.next(res);
      this.filteredOptions$.next(res);
      res.map((r: any) => r.tag.split(',')).forEach((tagList: string[]) => {
        this.optionTexts = [...this.optionTexts, ...tagList];
        this.optionTags =  [...this.optionTags, ...tagList];
      })
      this.optionTexts = [...new Set([...res.map((r: any) => r.name), ...this.optionTexts])];
      this.optionNodes = res;
      this.filteredOptions = res;
    })

    // @ts-ignore
    this.filteredOptionsObservable = this.myControl.valueChanges.pipe(
      startWith(''),
      // // @ts-ignore
      // map(value => (typeof value === 'string' ? value : value.name)),
      // @ts-ignore
      map(name => (name ? this._filterNormal(name) : this.optionTexts.slice())),
    );
  }
  displayFn(user: InfoNode): string {
    return user && user.name ? user.name : '';
  }
  private _filterNormal(name: string): string[] {
    const filterValue = name.toLowerCase();
    return this.optionTexts.filter(option => option.toLowerCase().includes(filterValue));
  }

  private _filter(name: string): Promise<InfoNode[]> {
    return new Promise(resolve => {
      const filterValue = name.toLowerCase();
      const filteredResult = this.optionNodes.filter(option => option.name.toLowerCase().includes(filterValue) || option.tag.toLowerCase().includes(filterValue));
      // resolve(filteredResult);
      this.searchNodeService.searchNodeByValue(name).subscribe((res: any) => {
        resolve(res)
      })
      // if (filteredResult.length > 0) {
      //   resolve(filteredResult);
      // } else {
      //   this.searchNodeService.searchNodeByValue(name).subscribe((res: any) => {
      //     resolve(res)
      //   })
      // }
    })
  }

  onSearchTrigger(option: string): void {
    this.searchValue = option;
    const filterValue = option.toLowerCase();
    if (this.optionTags.includes(option)) {
      this.filteredOptions$.next( this.optionNodes.filter(optNode => optNode.tag.toLowerCase().includes(filterValue)));
      this.filteredOptions = this.optionNodes.filter(optNode => optNode.tag.toLowerCase().includes(filterValue));
    } else {
      this.filteredOptions$.next( this.optionNodes.filter(optNode => optNode.name.toLowerCase().includes(filterValue)));
      this.filteredOptions = this.optionNodes.filter(optNode => optNode.name.toLowerCase().includes(filterValue));
    }


  }

  onInputChange() {
    this._filter(this.searchValue).then((res: any) => {
      this.filteredOptions$.next(res);
      this.filteredOptions = res;
      this.optionTexts = [];
      this.optionTags = [];
      res.map((r: any) => r.tag.split(',')).forEach((tagList: string[]) => {
        this.optionTexts = [...this.optionTexts, ...tagList];
        this.optionTags =  [...this.optionTags, ...tagList];
      })
      this.optionTexts = [...new Set([...res.map((r: any) => r.name), ...this.optionTexts])];
      this.optionNodes = res;
      this.myControl.patchValue(this.searchValue);
    })

  }

  onTriggerAutoPanel() {
    // @ts-ignore
    this.autoTrigger.openPanel();
  }

  addNewNode() {
    this.dialog.open(EditNodeDialogComponent);
  }

  modifyNode($event: string, option: InfoNode) {
    console.log($event, option)
    if ($event === 'edit') {
      const editDialogResult = this.dialog.open(EditNodeDialogComponent, {data: option});
      editDialogResult.afterClosed().subscribe(res => {
        if (!res) {
          return;
        }
        this.optionNodes.forEach((re, ind) => {
          if (re.record_id === res.record_id) {
            this.optionNodes[ind] = res;
          }
        });
        this.filteredOptions.forEach((re, ind) => {
          if (re.record_id === res.record_id) {
            this.filteredOptions[ind] = res;
          }
        });
        console.log(this.filteredOptions)
        this.filteredOptions$.next(this.filteredOptions);
      })
    } else if ($event === 'delete') {
      this.searchNodeService.deleteNode(option.record_id).subscribe((res1: InfoNode) => {
        this.optionNodes = this.optionNodes.filter(re => re.record_id !== option.record_id);
        this.filteredOptions = this.filteredOptions.filter(re => re.record_id !== option.record_id);
        this.filteredOptions$.next(this.filteredOptions);
      })
    }

  }
}
