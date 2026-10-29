import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiRecord, Appointment, Patient } from './models';

@Injectable({ providedIn: 'root' })
export class DentalApiService {
  private readonly http = inject(HttpClient);

  getPatients(): Observable<Patient[]> {
    return this.http.get<Patient[]>('/api/pacientes/');
  }

  getAppointments(): Observable<Appointment[]> {
    return this.http.get<Appointment[]>('/api/citas/');
  }

  list(endpoint: string): Observable<ApiRecord[]> {
    return this.http.get<ApiRecord[]>(`/api/${endpoint}/`);
  }

  create(endpoint: string, value: ApiRecord): Observable<ApiRecord> {
    return this.http.post<ApiRecord>(`/api/${endpoint}/`, value);
  }

  update(endpoint: string, id: number, value: ApiRecord): Observable<ApiRecord> {
    return this.http.patch<ApiRecord>(`/api/${endpoint}/${id}/`, value);
  }

  remove(endpoint: string, id: number): Observable<void> {
    return this.http.delete<void>(`/api/${endpoint}/${id}/`);
  }

  createEvolution(historyId: number, value: ApiRecord): Observable<ApiRecord> {
    return this.http.post<ApiRecord>(
      `/api/historias/${historyId}/evoluciones/`,
      value,
    );
  }
}
