import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { catchError, map, of } from 'rxjs';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }
  return auth.restoreSession().pipe(
    map((restored) => restored || router.createUrlTree(['/login'])),
    catchError(() => of(router.createUrlTree(['/login']))),
  );
};

export const guestGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return !auth.isAuthenticated() || inject(Router).createUrlTree(['/dashboard']);
};

export const permissionGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const resource = route.paramMap.get('resource') ?? '';
  return auth.canResource(resource) || inject(Router).createUrlTree(['/forbidden']);
};
