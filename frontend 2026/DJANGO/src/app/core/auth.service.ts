import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, finalize, forkJoin, map, Observable, of, switchMap, tap, throwError } from 'rxjs';
import { AccessGrant, AuthResponse, PermissionsResponse, UserProfile } from './models';

const ACCESS_KEY = 'odontonova.access';
const REFRESH_KEY = 'odontonova.refresh';
const USER_KEY = 'odontonova.user';
const PERMISSIONS_KEY = 'odontonova.permissions';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly userState = signal<UserProfile | null>(this.readUser());
  private readonly permissionState = signal<AccessGrant[]>(this.readPermissions());
  private readonly sessionRestoreError = signal('');

  readonly user = this.userState.asReadonly();
  readonly permissions = this.permissionState.asReadonly();
  readonly isAuthenticated = computed(() => Boolean(this.accessToken()));

  login(credentials: { username: string; password: string }): Observable<UserProfile> {
    return this.http.post<AuthResponse>('/api/auth/login/', credentials).pipe(
      tap((response) => this.saveTokens(response)),
      switchMap(() =>
        forkJoin({
          user: this.http.get<UserProfile>('/api/auth/profile/'),
          permissions: this.http.get<PermissionsResponse>('/api/auth/permissions/'),
        }),
      ),
      tap(({ user, permissions }) => this.saveSession(user, permissions.permissions)),
      map(({ user }) => user),
      catchError((error: unknown) => {
        this.clearSession();
        return throwError(() => error);
      }),
    );
  }

  takeSessionRestoreError(): string {
    const message = this.sessionRestoreError();
    this.sessionRestoreError.set('');
    return message;
  }

  restoreSession(): Observable<boolean> {
    if (!this.isAuthenticated()) {
      return of(false);
    }
    if (this.userState() && sessionStorage.getItem(PERMISSIONS_KEY) !== null) {
      return of(true);
    }
    return forkJoin({
      user: this.http.get<UserProfile>('/api/auth/profile/'),
      permissions: this.http.get<PermissionsResponse>('/api/auth/permissions/'),
    }).pipe(
      tap(({ user, permissions }) => this.saveSession(user, permissions.permissions)),
      map(() => true),
      catchError((error: unknown) => {
        this.clearSession();
        this.sessionRestoreError.set('No se pudo restaurar la sesión y los permisos. Inicia sesión nuevamente.');
        return throwError(() => error);
      }),
    );
  }

  refreshAccess(): Observable<string> {
    const refresh = sessionStorage.getItem(REFRESH_KEY);
    if (!refresh) {
      return throwError(() => new Error('No hay refresh token disponible.'));
    }

    return this.http
      .post<{ access: string; refresh?: string }>('/api/auth/refresh/', { refresh })
      .pipe(
        tap((tokens) => {
          sessionStorage.setItem(ACCESS_KEY, tokens.access);
          if (tokens.refresh) {
            sessionStorage.setItem(REFRESH_KEY, tokens.refresh);
          }
        }),
        map((tokens) => tokens.access),
      );
  }

  refreshPermissions(): Observable<AccessGrant[]> {
    return this.http.get<PermissionsResponse>('/api/auth/permissions/').pipe(
      map((response) => response.permissions),
      tap((permissions) => {
        this.permissionState.set(permissions);
        sessionStorage.setItem(PERMISSIONS_KEY, JSON.stringify(permissions));
      }),
    );
  }

  updateEmail(email: string): Observable<UserProfile> {
    return this.http.patch<UserProfile>('/api/auth/profile/', { email }).pipe(
      tap((user) => {
        this.userState.set(user);
        sessionStorage.setItem(USER_KEY, JSON.stringify(user));
      }),
    );
  }

  canResource(resource: string): boolean {
    return Boolean(
      this.userState()?.is_superuser ||
        this.permissionState().some((grant) => grant.resource === '*' || grant.resource === resource),
    );
  }

  canPermission(method: string, path: string): boolean {
    if (this.userState()?.is_superuser) {
      return true;
    }
    return this.permissionState().some(
      (grant) =>
        (grant.method === '*' || grant.method.toUpperCase() === method.toUpperCase()) &&
        (grant.path === '/api/' ||
          path === grant.path ||
          (grant.path.endsWith('/') && path.startsWith(grant.path))),
    );
  }

  logout(): Observable<void> {
    const refresh = sessionStorage.getItem(REFRESH_KEY);
    if (!refresh) {
      this.clearSession();
      void this.router.navigateByUrl('/login');
      return of(undefined);
    }

    return this.http
      .post<void>('/api/auth/logout/', { refresh })
      .pipe(
        finalize(() => {
          this.clearSession();
          void this.router.navigateByUrl('/login');
        }),
      );
  }

  accessToken(): string | null {
    return sessionStorage.getItem(ACCESS_KEY);
  }

  expireSession(): void {
    this.clearSession();
    void this.router.navigateByUrl('/login');
  }

  private saveTokens(response: AuthResponse): void {
    sessionStorage.setItem(ACCESS_KEY, response.access);
    sessionStorage.setItem(REFRESH_KEY, response.refresh);
  }

  private saveSession(user: UserProfile, permissions: AccessGrant[]): void {
    this.userState.set(user);
    this.permissionState.set(permissions);
    sessionStorage.setItem(USER_KEY, JSON.stringify(user));
    sessionStorage.setItem(PERMISSIONS_KEY, JSON.stringify(permissions));
  }

  private readUser(): UserProfile | null {
    const value = sessionStorage.getItem(USER_KEY);
    if (!value) {
      return null;
    }
    try {
      return JSON.parse(value) as UserProfile;
    } catch {
      sessionStorage.removeItem(USER_KEY);
      return null;
    }
  }

  private readPermissions(): AccessGrant[] {
    const value = sessionStorage.getItem(PERMISSIONS_KEY);
    if (!value) {
      return [];
    }
    try {
      return JSON.parse(value) as AccessGrant[];
    } catch {
      sessionStorage.removeItem(PERMISSIONS_KEY);
      return [];
    }
  }

  private clearSession(): void {
    sessionStorage.removeItem(ACCESS_KEY);
    sessionStorage.removeItem(REFRESH_KEY);
    sessionStorage.removeItem(USER_KEY);
    sessionStorage.removeItem(PERMISSIONS_KEY);
    this.userState.set(null);
    this.permissionState.set([]);
  }
}
