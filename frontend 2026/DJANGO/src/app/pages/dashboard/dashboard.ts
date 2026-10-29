import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { AuthService } from '../../core/auth.service';
import { Appointment, Patient } from '../../core/models';
import { DentalApiService } from '../../core/dental-api.service';

@Component({
  imports: [RouterLink],
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
})
export class Dashboard {
  private readonly api = inject(DentalApiService);
  private readonly auth = inject(AuthService);

  protected readonly patients = signal<Patient[]>([]);
  protected readonly appointments = signal<Appointment[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal('');
  protected readonly todayAppointments = computed(() => {
    const today = new Date().toDateString();
    return this.appointments()
      .filter((appointment) => new Date(appointment.start_time).toDateString() === today)
      .sort((left, right) => left.start_time.localeCompare(right.start_time));
  });
  protected readonly activeAppointments = computed(() =>
    this.appointments().filter((appointment) => appointment.status === 'scheduled' || appointment.status === 'confirmed').length,
  );

  constructor() {
    this.load();
  }

  protected patientName(patientId: number): string {
    const patient = this.patients().find((item) => item.id === patientId);
    return patient ? `${patient.first_name} ${patient.last_name}` : `Paciente #${patientId}`;
  }

  protected formatTime(value: string): string {
    return new Intl.DateTimeFormat('es', { hour: '2-digit', minute: '2-digit' }).format(new Date(value));
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
    forkJoin({
      patients: this.auth.canResource('pacientes') ? this.api.getPatients() : of([]),
      appointments: this.auth.canResource('citas') ? this.api.getAppointments() : of([]),
    }).subscribe({
      next: ({ patients, appointments }) => {
        this.patients.set(patients);
        this.appointments.set(appointments);
        this.loading.set(false);
      },
      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          error.status === 0
            ? 'No se pudo conectar con Django. Verifica que el servidor esté activo.'
            : error.status === 401
              ? 'Tu sesión venció. Inicia sesión nuevamente.'
              : 'No fue posible cargar el resumen de la clínica.',
        );
        this.loading.set(false);
      },
    });
  }
}
