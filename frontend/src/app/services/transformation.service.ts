import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TransformationService {

  constructor() { }
  // tslint:disable-next-line:no-any
  parseJsonObjectFromString(rawData: string): any {
    try {
      return Object.values(JSON.parse(rawData));
    } catch {
      console.log(rawData);
    }
  }
}
