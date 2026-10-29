import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { AuthService } from './auth.service';
import { AccessGrant, UserProfile } from './models';

describe('AuthService', () => {
  let service: AuthService;
  let http: HttpTestingController;

  beforeEach(() => {
    sessionStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    sessionStorage.clear();
  });

  it('stores the JWT session and effective permissions after login', () => {
    const user: UserProfile = {
      id: 8,
      username: 'clinic-user',
      email: 'clinic@example.test',
      first_name: 'Clinic',
      last_name: 'User',
      is_superuser: false,
    };
    const grant: AccessGrant = {
      resource: 'pacientes',
      method: '*',
      path: '/api/pacientes/',
      roleId: 2,
      roleName: 'Recepción',
    };
    let result: UserProfile | undefined;

    service.login({ username: user.username, password: 'secure-password' }).subscribe((value) => {
      result = value;
    });
    http.expectOne('/api/auth/login/').flush({
      access: 'access-token',
      refresh: 'refresh-token',
      user,
    });
    http.expectOne('/api/auth/profile/').flush(user);
    http.expectOne('/api/auth/permissions/').flush({ permissions: [grant] });

    expect(result).toEqual(user);
    expect(service.canResource('pacientes')).toBe(true);
    expect(service.canResource('pagos')).toBe(false);
    expect(sessionStorage.getItem('odontonova.access')).toBe('access-token');
    expect(sessionStorage.getItem('odontonova.refresh')).toBe('refresh-token');
  });

  it('rotates and persists the refresh token', () => {
    sessionStorage.setItem('odontonova.refresh', 'old-refresh-token');
    let access: string | undefined;

    service.refreshAccess().subscribe((value) => {
      access = value;
    });
    http.expectOne('/api/auth/refresh/').flush({
      access: 'new-access-token',
      refresh: 'new-refresh-token',
    });

    expect(access).toBe('new-access-token');
    expect(sessionStorage.getItem('odontonova.access')).toBe('new-access-token');
    expect(sessionStorage.getItem('odontonova.refresh')).toBe('new-refresh-token');
  });
});
