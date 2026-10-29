import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { Appointment, Patient } from '../../core/models';
import { DentalApiService } from '../../core/dental-api.service';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.html',
})
export class Appointments {
  private readonly api = inject(DentalApiService);

  protected readonly patients = signal<Patient[]>([]);
  protected readonly appointments = signal<Appointment[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal('');
  protected readonly sortedAppointments = computed(() =>
    [...this.appointments()].sort((left, right) => left.start_time.localeCompare(right.start_time)),
  );

  constructor() {
    this.load();
  }

  protected patientName(patientId: number): string {
    const patient = this.patients().find((item) => item.id === patientId);
    return patient ? `${patient.first_name} ${patient.last_name}` : `Paciente #${patientId}`;
  }

  protected formatDate(value: string): string {
    return new Intl.DateTimeFormat('es', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));
  }

  protected statusLabel(status: Appointment['status']): string {
    const labels: Record<Appointment['status'], string> = {
      scheduled: 'Programada',
      confirmed: 'Confirmada',
      completed: 'Completada',
      cancelled: 'Cancelada',
      no_show: 'No asistió',
    };
    return labels[status];
  }

  protected reload(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.api.getAppointments().subscribe({
      next: (appointments) => {
        this.appointments.set(appointments);
        this.api.getPatients().subscribe({
          next: (patients) => {
            this.patients.set(patients);
            this.loading.set(false);
          },
          error: (error: HttpErrorResponse) => {
            this.errorMessage.set(
              error.status === 0
                ? 'No se pudo conectar con Django. Verifica que el servidor esté activo.'
                : 'No fue posible cargar los nombres de los pacientes.',
            );
            this.loading.set(false);
          },
        });
      },
      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          error.status === 0
            ? 'No se pudo conectar con Django. Verifica que el servidor esté activo.'
            : error.status === 401
              ? 'Tu sesión venció. Inicia sesión nuevamente.'
              : 'No fue posible cargar las citas.',
        );
        this.loading.set(false);
      },
    });
  }
}
