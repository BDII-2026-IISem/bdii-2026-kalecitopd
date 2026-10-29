import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { finalize } from 'rxjs';
import { AuthService } from '../../core/auth.service';

@Component({
  imports: [ReactiveFormsModule, ButtonModule, RouterLink],
  selector: 'app-login',
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private readonly formBuilder = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly form = this.formBuilder.nonNullable.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
  });

  constructor() {
    const restoreError = this.auth.takeSessionRestoreError();
    if (restoreError) {
      this.errorMessage.set(restoreError);
    }
  }

  protected submit(): void {
    if (this.form.invalid || this.loading()) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage.set('');
    this.loading.set(true);
    this.auth
      .login(this.form.getRawValue())
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: () => void this.router.navigateByUrl('/dashboard'),
        error: (error: HttpErrorResponse) => {
          const detail = error.error?.detail;
          this.errorMessage.set(
            error.status === 0
              ? 'No se pudo conectar con el servidor. Verifica que Django esté ejecutándose.'
              : error.status === 401
                ? 'Usuario o contraseña incorrectos.'
                : typeof detail === 'string'
                  ? detail
                  : 'No fue posible iniciar sesión. Intenta de nuevo.',
          );
        },
      });
  }
}
