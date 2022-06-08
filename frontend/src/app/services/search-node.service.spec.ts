import { TestBed } from '@angular/core/testing';

import { SearchNodeService } from './search-node.service';

describe('SearchNodeService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SearchNodeService = TestBed.get(SearchNodeService);
    expect(service).toBeTruthy();
  });
});
