import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {InfoNode} from "../interfaces/node";

@Component({
  selector: 'app-node-cell',
  templateUrl: './node-cell.component.html',
  styleUrls: ['./node-cell.component.css']
})
export class NodeCellComponent implements OnInit {
  @Input() infoNode: InfoNode | undefined;
  @Output() cModelChange = new EventEmitter<string>();
  constructor() { }

  ngOnInit() {
  }
  splitName(stringValue: string): string[] {
    return stringValue.split(',')
  }

  deleteNode() {
    this.cModelChange.emit('delete');
  }

  editNode() {
    this.cModelChange.emit('edit')
  }
}
