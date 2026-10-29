import { Routes } from '@angular/router';
import { authGuard, guestGuard, permissionGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then((module) => module.Login),
    canActivate: [guestGuard],
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard').then((module) => module.Dashboard),
    canActivate: [authGuard],
  },
  {
    path: 'appointments',
    pathMatch: 'full',
    redirectTo: 'resources/citas',
  },
  {
    path: 'patients',
    pathMatch: 'full',
    redirectTo: 'resources/pacientes',
  },
  {
    path: 'resources/:resource',
    loadComponent: () =>
      import('./features/resources/resource-page').then((module) => module.ResourcePage),
    canActivate: [authGuard, permissionGuard],
    data: { resource: 'resource' },
  },
  {
    path: 'forbidden',
    loadComponent: () => import('./pages/forbidden/forbidden').then((module) => module.Forbidden),
    canActivate: [authGuard],
  },
  {
    path: 'profile',
    loadComponent: () => import('./pages/profile/profile').then((module) => module.Profile),
    canActivate: [authGuard],
  },
  { path: '**', redirectTo: 'dashboard' },
];
