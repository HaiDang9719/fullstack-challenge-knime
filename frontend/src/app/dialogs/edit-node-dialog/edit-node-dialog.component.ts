import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {SearchNodeService} from "../../services/search-node.service";
import {InfoNode} from "../../interfaces/node";

@Component({
  selector: 'app-edit-node-dialog',
  templateUrl: './edit-node-dialog.component.html',
  styleUrls: ['./edit-node-dialog.component.css']
})
export class EditNodeDialogComponent implements OnInit {
  nodeName: string = '';
  nodeTag: string = '';
  nodeGroup: string = '';
  nodeDescription: string = '';
  nodeRecordID: string = '1';
  constructor(private dialogRef: MatDialogRef<EditNodeDialogComponent>, private searchNodeService: SearchNodeService,
              @Inject(MAT_DIALOG_DATA) public data: InfoNode) { }

  ngOnInit() {
    if (this.data) {
      this.nodeName = this.data.name;
      this.nodeTag = this.data.tag;
      this.nodeGroup = this.data.group;
      this.nodeDescription = this.data.description;
      this.nodeRecordID = this.data.record_id;
    }
  }

  onNoClick() {
    this.dialogRef.close();
  }

  addNewNode() {
    if (this.data) {
      this.searchNodeService.updateNodeInfo( {name: this.nodeName, tag: this.nodeTag, group: this.nodeGroup, description: this.nodeDescription, record_id: this.nodeRecordID},  this.nodeRecordID)
        .subscribe(() => {
          this.dialogRef.close({name: this.nodeName, tag: this.nodeTag, group: this.nodeGroup, description: this.nodeDescription, record_id: this.nodeRecordID});
        })
    } else {
      this.searchNodeService.addNode({name: this.nodeName, tag: this.nodeTag, group: this.nodeGroup, description: this.nodeDescription, record_id: this.nodeRecordID})
        .subscribe(() => {
          this.dialogRef.close({name: this.nodeName, tag: this.nodeTag, group: this.nodeGroup, description: this.nodeDescription, record_id: this.nodeRecordID});
          window.location.reload();
        })
    }

  }
}
