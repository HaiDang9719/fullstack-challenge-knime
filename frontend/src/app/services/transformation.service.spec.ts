import { TestBed } from '@angular/core/testing';

import { TransformationService } from './transformation.service';

describe('TransformationService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TransformationService = TestBed.get(TransformationService);
    expect(service).toBeTruthy();
  });
});
