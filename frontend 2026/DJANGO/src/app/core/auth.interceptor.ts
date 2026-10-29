import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable, catchError, finalize, shareReplay, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth.service';

let refreshRequest: Observable<string> | null = null;

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  const token = auth.accessToken();
  const isAuthRequest = /\/api\/auth\/(login|refresh)\//.test(request.url);
  const authorizedRequest =
    token && !isAuthRequest
      ? request.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
      : request;

  return next(authorizedRequest).pipe(
    catchError((error: unknown) => {
      if (
        !(error instanceof HttpErrorResponse) ||
        error.status !== 401 ||
        !token ||
        isAuthRequest
      ) {
        return throwError(() => error);
      }

      if (!refreshRequest) {
        refreshRequest = auth.refreshAccess().pipe(
          shareReplay({ bufferSize: 1, refCount: false }),
          finalize(() => {
            refreshRequest = null;
          }),
        );
      }

      return refreshRequest.pipe(
        switchMap((access) =>
          next(
            request.clone({
              setHeaders: { Authorization: `Bearer ${access}` },
            }),
          ),
        ),
        catchError((refreshError: unknown) => {
          auth.expireSession();
          return throwError(() => refreshError);
        }),
      );
    }),
  );
};
