import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Patient } from '../../core/models';
import { DentalApiService } from '../../core/dental-api.service';

@Component({
  imports: [FormsModule],
  selector: 'app-patients',
  templateUrl: './patients.html',
})
export class Patients {
  private readonly api = inject(DentalApiService);

  protected readonly patients = signal<Patient[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal('');
  protected readonly query = signal('');
  protected readonly filteredPatients = computed(() => {
    const search = this.query().trim().toLocaleLowerCase();
    if (!search) {
      return this.patients();
    }
    return this.patients().filter((patient) =>
      `${patient.first_name} ${patient.last_name} ${patient.document_number ?? ''} ${patient.email} ${patient.phone}`
        .toLocaleLowerCase()
        .includes(search),
    );
  });

  constructor() {
    this.load();
  }

  protected reload(): void {
    this.load();
  }

  protected fullName(patient: Patient): string {
    return `${patient.first_name} ${patient.last_name}`;
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.api.getPatients().subscribe({
      next: (patients) => {
        this.patients.set(patients);
        this.loading.set(false);
      },
      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          error.status === 0
            ? 'No se pudo conectar con Django. Verifica que el servidor esté activo.'
            : error.status === 401
              ? 'Tu sesión venció. Inicia sesión nuevamente.'
              : 'No fue posible cargar los pacientes.',
        );
        this.loading.set(false);
      },
    });
  }
}
