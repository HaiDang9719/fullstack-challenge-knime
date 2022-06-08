import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {map} from "rxjs/operators";
import {TransformationService} from "./transformation.service";
import {InfoNode} from "../interfaces/node";

@Injectable({
  providedIn: 'root'
})
export class SearchNodeService {
  private testAPI = environment.apiURL;
  constructor(private http: HttpClient, private transformationService: TransformationService,) { }

  /**
   * Get all node information
   */
  getAllNodeInformation(): any {
    return this.http.post<string>(this.testAPI + '/search/get_all_node_info',
      {});
      // .pipe(map((corr) => this.transformationService.parseJsonObjectFromString(corr)));
  }
  searchNodeByValue(value: string): any {
    return this.http.post<string>(this.testAPI + '/search/search_node',
      {searchValue: value});
  }
  addNode(nodeInfo: InfoNode): any {
    return this.http.post<string>(this.testAPI + '/search/add_new_node',
      {nodeInfo: nodeInfo});
  }
  updateNodeInfo(nodeInfo: InfoNode, recordID: string): any {
    return this.http.post<string>(this.testAPI + '/search/update_node_info',
      {nodeInfo: {name: nodeInfo.name, tag: nodeInfo.tag, group: nodeInfo.group, description: nodeInfo.description}, recordID: recordID});
  }
  deleteNode(recordID: string): any {
    return this.http.post<string>(this.testAPI + '/search/delete_node_info',
      {recordID: recordID});
  }
}
