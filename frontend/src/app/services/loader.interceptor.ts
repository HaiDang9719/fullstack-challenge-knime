import { Injectable } from '@angular/core';
import {
  HttpErrorResponse,
  HttpResponse,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { LoaderService } from './loader.service';
import { catchError, retry } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material';

@Injectable()
export class LoaderInterceptor implements HttpInterceptor {
  private requests: HttpRequest<any>[] = [];

  constructor(private loaderService: LoaderService, private snackBar: MatSnackBar) {}

  removeRequest(req: HttpRequest<any>) {
    const i = this.requests.indexOf(req);
    if (i >= 0) {
      this.requests.splice(i, 1);
    }
    if (this.requests.length === 0) {
      this.loaderService.setNewLoadingStatus(false);
    }
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // new request is coming
    this.requests.push(req);
    this.loaderService.setNewLoadingStatus(true);

    return Observable.create((observer: any) => {
      const subscription = next
        .handle(req)
        .pipe(
          // catch error similarly for each HTTP request
          retry(3),
          catchError((error: HttpErrorResponse) => {
            if (error.error instanceof ErrorEvent) {
              // A client-side or network error occurred. Handle it accordingly.
              console.error('An error occurred:', error.error.message);
            } else {
              // The backendAddress returned an unsuccessful response code.
              // The response body may contain clues as to what went wrong,
              console.error('Backend returned code', error.status, 'body was ', error.error);
            }

            this.snackBar.open('An error occurred. Please check logs for details.', 'Close');

            // return an observable with a user-facing error message
            return throwError(error);
          })
        )
        .subscribe(
          (event) => {
            // new valid response
            if (event instanceof HttpResponse) {
              this.removeRequest(req);
              observer.next(event);
            }
          },
          (err) => {
            // new response with errors
            this.removeRequest(req);
            observer.error(err);
          },
          () => {
            this.removeRequest(req);
            observer.complete();
          }
        );
      // remove request from queue when cancelled
      return () => {
        this.removeRequest(req);
        subscription.unsubscribe();
      };
    });
  }
}
