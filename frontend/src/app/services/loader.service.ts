import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class LoaderService {
  // @ts-ignore
  private isLoadingSubject: Subject<boolean> = new BehaviorSubject(false);
  public isLoading$: Observable<boolean> = this.isLoadingSubject
    .asObservable()
    .pipe(distinctUntilChanged(), debounceTime(50));

  constructor() {}

  public setNewLoadingStatus(isLoading: boolean) {
    this.isLoadingSubject.next(isLoading);
  }
}
