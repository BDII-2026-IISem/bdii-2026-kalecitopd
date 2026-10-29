import { HttpErrorResponse } from '@angular/common/http';
import { Component, effect, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';
import { AuthService } from '../../core/auth.service';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-profile',
  template: `
    <div class="page-heading">
      <div>
        <span class="eyebrow">CUENTA PERSONAL</span>
        <h1>Mi perfil</h1>
        <p>Consulta tus datos y actualiza tu correo de contacto.</p>
      </div>
    </div>
    <section class="panel profile-panel">
      <div class="profile-heading">
        <span class="profile-avatar">{{ initials() }}</span>
        <div>
          <h2>{{ auth.user()?.first_name || auth.user()?.username }} {{ auth.user()?.last_name }}</h2>
          <p>{{ auth.user()?.is_superuser ? 'Superusuario' : 'Personal de OdontoNova' }}</p>
        </div>
      </div>
      <form [formGroup]="form" (ngSubmit)="save()">
        <label>Nombre de usuario<input type="text" [value]="auth.user()?.username" readonly /></label>
        <label>Correo electrónico<input type="email" formControlName="email" autocomplete="email" /></label>
        @if (message()) {<p class="success-message" role="status">{{ message() }}</p>}
        @if (errorMessage()) {<p class="error-message" role="alert">{{ errorMessage() }}</p>}
        <button type="submit" class="primary-link" [disabled]="form.invalid || saving()">
          @if (saving()) {<i class="pi pi-spin pi-spinner"></i>} @else {<i class="pi pi-check"></i>}
          Guardar perfil
        </button>
      </form>
    </section>
  `,
  styles: `
    .profile-panel { max-width: 650px; padding: 24px; }
    .profile-heading { display:flex; align-items:center; gap:14px; padding-bottom:21px; border-bottom:1px solid #edf1f3; }
    .profile-avatar { display:grid; width:48px; height:48px; place-items:center; border-radius:50%; color:#164650; background:#b7e5dc; font-weight:800; }
    .profile-heading h2 { margin:0 0 5px; color:#24414b; font-size:16px; }
    .profile-heading p { margin:0; color:#82939b; font-size:11px; }
    form { display:grid; max-width:420px; gap:15px; padding-top:21px; }
    label { display:grid; gap:7px; color:#36505a; font-size:11px; font-weight:700; }
    input { min-height:40px; padding:9px 11px; border:1px solid #dfe7ea; border-radius:7px; color:#28434d; font:inherit; font-size:12px; }
    input:focus { border-color:#54b5a3; outline:0; box-shadow:0 0 0 3px rgb(84 181 163 / 14%); }
    input[readonly] { background:#f7f9fa; }
    .primary-link { width:fit-content; min-height:38px; border:0; cursor:pointer; font-size:11px; }
    .primary-link:disabled { opacity:.55; cursor:not-allowed; }
    .success-message { margin:0; color:#247364; font-size:12px; }
    .error-message { margin:0; color:#a63831; font-size:12px; }
  `,
})
export class Profile {
  private readonly formBuilder = inject(FormBuilder);
  protected readonly auth = inject(AuthService);
  protected readonly saving = signal(false);
  protected readonly message = signal('');
  protected readonly errorMessage = signal('');
  protected readonly form = this.formBuilder.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
  });
  protected readonly initials = signal('O');

  constructor() {
    effect(() => {
      const user = this.auth.user();
      this.form.controls.email.setValue(user?.email ?? '');
      const first = user?.first_name || user?.username || 'O';
      this.initials.set(`${first.charAt(0)}${user?.last_name?.charAt(0) ?? ''}`.toUpperCase());
    });
  }

  protected save(): void {
    if (this.form.invalid || this.saving()) {
      this.form.markAllAsTouched();
      return;
    }
    this.message.set('');
    this.errorMessage.set('');
    this.saving.set(true);
    this.auth
      .updateEmail(this.form.controls.email.value)
      .pipe(finalize(() => this.saving.set(false)))
      .subscribe({
        next: () => this.message.set('El correo del perfil se actualizó correctamente.'),
        error: (error: HttpErrorResponse) =>
          this.errorMessage.set(
            error.status === 401
              ? 'Tu sesión expiró. Inicia sesión nuevamente.'
              : error.error?.email?.[0] ?? 'No fue posible actualizar el perfil.',
          ),
      });
  }
}
