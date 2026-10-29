import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { catchError, forkJoin, map, of } from 'rxjs';
import { AuthService } from '../../core/auth.service';
import { DentalApiService } from '../../core/dental-api.service';
import { ApiRecord } from '../../core/models';
import {
  FieldOption,
  ResourceConfig,
  ResourceField,
  RESOURCE_CONFIG_BY_KEY,
  recordLabel,
} from './resource-config';

type FormValue = string | number | boolean | null;
type ReferenceResult =
  | { endpoint: string; records: ApiRecord[] }
  | { endpoint: string; error: unknown };

interface SessionLine {
  treatment_detail: number | null;
  quantity: number;
  materials_used: string;
}

@Component({
  imports: [FormsModule],
  selector: 'app-resource-page',
  templateUrl: './resource-page.html',
  styleUrl: './resource-page.css',
})
export class ResourcePage {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(DentalApiService);

  protected readonly auth = inject(AuthService);
  protected readonly resource = signal<ResourceConfig | null>(null);
  protected readonly records = signal<ApiRecord[]>([]);
  protected readonly referenceOptions = signal<Record<string, FieldOption[]>>({});
  protected readonly referenceErrors = signal<string[]>([]);
  protected readonly referenceErrorSummary = signal('');
  protected readonly loading = signal(true);
  protected readonly saving = signal(false);
  protected readonly deletingId = signal<number | null>(null);
  protected readonly query = signal('');
  protected readonly errorMessage = signal('');
  protected readonly successMessage = signal('');
  protected readonly dialogOpen = signal(false);
  protected readonly editingId = signal<number | null>(null);
  protected readonly formValues = signal<Record<string, FormValue>>({});
  protected readonly formError = signal('');
  protected readonly sessionLines = signal<SessionLine[]>([]);
  protected readonly evolutionHistoryId = signal<number | null>(null);
  protected readonly evolutionValues = signal<Record<string, string>>({
    findings: '',
    procedures: '',
    materials_used: '',
    consent_signed_at: '',
  });
  protected readonly evolutionError = signal('');
  protected readonly filteredRecords = computed(() => {
    const search = this.query().trim().toLocaleLowerCase();
    const config = this.resource();
    if (!search || !config) {
      return this.records();
    }
    return this.records().filter((record) =>
      config.columns.some((column) =>
        this.displayValue(record, column).toLocaleLowerCase().includes(search),
      ),
    );
  });

  constructor() {
    this.route.paramMap.subscribe((params) => {
      const key = params.get('resource') ?? '';
      const config = RESOURCE_CONFIG_BY_KEY.get(key);
      if (!config) {
        void this.router.navigateByUrl('/dashboard');
        return;
      }
      this.resource.set(config);
      this.query.set('');
      this.reload();
    });
  }

  protected reload(): void {
    const config = this.resource();
    if (!config) {
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');
    this.api.list(config.endpoint).subscribe({
      next: (records) => {
        this.records.set(records);
        this.loading.set(false);
        this.loadReferences(config);
      },
      error: (error: unknown) => {
        this.loading.set(false);
        this.records.set([]);
        this.errorMessage.set(this.apiError(error, `No fue posible cargar ${config.title.toLocaleLowerCase()}.`));
      },
    });
  }

  protected openCreate(): void {
    const config = this.resource();
    if (!config || !this.auth.canPermission('POST', `/api/${config.endpoint}/`)) {
      return;
    }
    this.editingId.set(null);
    this.formError.set('');
    this.formValues.set(this.defaultValues(config.fields));
    this.sessionLines.set([]);
    this.dialogOpen.set(true);
  }

  protected openEdit(record: ApiRecord): void {
    const config = this.resource();
    if (!config || !this.auth.canPermission('PATCH', `/api/${config.endpoint}/`)) {
      return;
    }
    this.editingId.set(Number(record['id']));
    this.formError.set('');
    const values: Record<string, FormValue> = {};
    for (const field of config.fields) {
      if (field.type === 'session-lines' || field.type === 'password') {
        values[field.key] = '';
        continue;
      }
      values[field.key] = this.toFormValue(field, record[field.key]);
    }
    this.formValues.set(values);
    this.sessionLines.set([]);
    this.dialogOpen.set(true);
  }

  protected closeDialog(): void {
    if (!this.saving()) {
      this.dialogOpen.set(false);
      this.formError.set('');
    }
  }

  protected setField(key: string, value: FormValue): void {
    this.formValues.update((values) => ({ ...values, [key]: value }));
  }

  protected fieldValue(field: ResourceField): FormValue {
    return this.formValues()[field.key] ?? '';
  }

  protected hasReferenceError(endpoint: string): boolean {
    return this.referenceErrors().includes(endpoint);
  }

  protected referenceList(endpoint: string): FieldOption[] {
    return this.referenceOptions()[endpoint] ?? [];
  }

  protected displayValue(record: ApiRecord, column: ResourceConfig['columns'][number]): string {
    const raw = record[column.key];
    if (column.source) {
      const option = this.referenceList(column.source).find(
        (item) => String(item.value) === String(raw),
      );
      return option?.label ?? (raw === null || raw === undefined ? '—' : `#${String(raw)}`);
    }
    if (column.key === 'evolutions' && Array.isArray(raw)) {
      return String(raw.length);
    }
    if (typeof raw === 'boolean') {
      return raw ? 'Activo' : 'Inactivo';
    }
    if (raw === null || raw === undefined || raw === '') {
      return '—';
    }
    const field = this.resource()?.fields.find((item) => item.key === column.key);
    const choice = field?.options?.find((item) => String(item.value) === String(raw));
    if (choice) {
      return choice.label;
    }
    if (field?.type === 'datetime-local' || column.key.endsWith('_at')) {
      const date = new Date(String(raw));
      return Number.isNaN(date.getTime())
        ? String(raw)
        : new Intl.DateTimeFormat('es', { dateStyle: 'medium', timeStyle: 'short' }).format(date);
    }
    if (column.key === 'total_amount' || column.key === 'paid_amount' || column.key === 'balance_due' ||
        column.key === 'unit_price' || column.key === 'total' || column.key === 'amount') {
      return new Intl.NumberFormat('es', { style: 'currency', currency: 'USD' }).format(Number(raw));
    }
    return String(raw);
  }

  protected statusClass(record: ApiRecord, key: string): string {
    const value = record[key];
    if (key === 'is_active') {
      return value ? 'active' : 'inactive';
    }
    return typeof value === 'string' ? value : '';
  }

  protected clearSuccess(): void {
    this.successMessage.set('');
  }

  protected parseNumber(value: unknown): number | null {
    if (value === '' || value === null || value === undefined) {
      return null;
    }
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }

  protected canCreate(): boolean {
    const config = this.resource();
    return Boolean(config && this.auth.canPermission('POST', `/api/${config.endpoint}/`));
  }

  protected canEdit(): boolean {
    const config = this.resource();
    return Boolean(config && this.auth.canPermission('PATCH', `/api/${config.endpoint}/`));
  }

  protected canDelete(): boolean {
    const config = this.resource();
    return Boolean(config?.canDelete && this.auth.canPermission('DELETE', `/api/${config.endpoint}/`));
  }

  protected canAddEvolution(): boolean {
    return this.auth.canPermission('POST', '/api/historias/');
  }

  protected formUnavailable(): boolean {
    const config = this.resource();
    if (!config) {
      return true;
    }
    return config.fields.some(
      (field) =>
        field.required &&
        field.source &&
        (this.hasReferenceError(field.source) || this.referenceList(field.source).length === 0),
    );
  }

  protected save(): void {
    const config = this.resource();
    if (!config || this.saving()) {
      return;
    }

    const payload = this.buildPayload(config);
    if (this.formUnavailable()) {
      this.formError.set('Faltan catálogos relacionados o no tienes permiso para consultarlos. Revisa los avisos antes de guardar.');
      return;
    }

    this.saving.set(true);
    this.formError.set('');
    const editingId = this.editingId();
    const request = editingId === null
      ? this.api.create(config.endpoint, payload)
      : this.api.update(config.endpoint, editingId, payload);
    request.subscribe({
      next: () => {
        this.saving.set(false);
        this.dialogOpen.set(false);
        this.successMessage.set(`${config.singular} ${editingId === null ? 'creado' : 'actualizado'} correctamente.`);
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.formError.set(this.apiError(error, 'No fue posible guardar los cambios.'));
      },
    });
  }

  protected deleteRecord(record: ApiRecord): void {
    const config = this.resource();
    const id = Number(record['id']);
    if (!config || !this.canDelete() || this.deletingId() !== null) {
      return;
    }
    if (!window.confirm(`¿Eliminar este registro de ${config.singular}? Esta acción no se puede deshacer.`)) {
      return;
    }

    this.deletingId.set(id);
    this.api.remove(config.endpoint, id).subscribe({
      next: () => {
        this.deletingId.set(null);
        this.successMessage.set(`${config.singular} eliminado correctamente.`);
        this.reload();
      },
      error: (error: unknown) => {
        this.deletingId.set(null);
        this.errorMessage.set(this.apiError(error, 'No se pudo eliminar el registro.'));
      },
    });
  }

  protected addSessionLine(): void {
    this.sessionLines.update((lines) => [
      ...lines,
      { treatment_detail: null, quantity: 1, materials_used: '' },
    ]);
  }

  protected updateSessionLine(index: number, patch: Partial<SessionLine>): void {
    this.sessionLines.update((lines) =>
      lines.map((line, position) => position === index ? { ...line, ...patch } : line),
    );
  }

  protected removeSessionLine(index: number): void {
    this.sessionLines.update((lines) => lines.filter((_, position) => position !== index));
  }

  protected availableTreatmentDetails(): FieldOption[] {
    const selectedPlan = Number(this.formValues()['treatment_plan']);
    return this.referenceList('detalles-tratamiento').filter((option) => {
      const record = this.recordsForReference('detalles-tratamiento').find(
        (item) => Number(item['id']) === Number(option.value),
      );
      return record &&
        Number(record['treatment_plan']) === selectedPlan &&
        Number(record['approved_quantity']) > 0;
    });
  }

  protected openEvolution(record: ApiRecord): void {
    this.evolutionHistoryId.set(Number(record['id']));
    this.evolutionValues.set({
      findings: '',
      procedures: '',
      materials_used: '',
      consent_signed_at: '',
    });
    this.evolutionError.set('');
  }

  protected closeEvolution(): void {
    this.evolutionHistoryId.set(null);
  }

  protected setEvolutionField(key: string, value: string): void {
    this.evolutionValues.update((values) => ({ ...values, [key]: value }));
  }

  protected saveEvolution(): void {
    const historyId = this.evolutionHistoryId();
    const values = this.evolutionValues();
    if (historyId === null || !values['findings'].trim()) {
      this.evolutionError.set('Registra los hallazgos antes de guardar.');
      return;
    }
    const consent = values['consent_signed_at'];
    const payload: ApiRecord = {
      findings: values['findings'],
      procedures: values['procedures'],
      materials_used: values['materials_used'],
      consent_signed_at: consent ? this.toIsoDate(consent) : null,
    };
    this.api.createEvolution(historyId, payload).subscribe({
      next: () => {
        this.evolutionHistoryId.set(null);
        this.successMessage.set('Evolución clínica registrada correctamente.');
        this.reload();
      },
      error: (error: unknown) => {
        this.evolutionError.set(this.apiError(error, 'No fue posible registrar la evolución.'));
      },
    });
  }

  protected recordId(record: ApiRecord): number {
    return Number(record['id']);
  }

  protected formTitle(): string {
    const config = this.resource();
    return `${this.editingId() === null ? 'Nuevo' : 'Editar'} ${config?.singular ?? 'registro'}`;
  }

  private loadReferences(config: ResourceConfig): void {
    const endpoints = [
      ...new Set([
        ...config.fields.flatMap((field) => field.source ? [field.source] : []),
        ...config.columns.flatMap((column) => column.source ? [column.source] : []),
      ]),
    ];
    if (endpoints.length === 0) {
      this.referenceOptions.set({});
      this.referenceErrors.set([]);
      this.referenceErrorSummary.set('');
      return;
    }

    const requests = endpoints.map((endpoint) =>
      this.api.list(endpoint).pipe(
        map((records): ReferenceResult => ({ endpoint, records })),
        catchError((error: unknown) => of({ endpoint, error } as ReferenceResult)),
      ),
    );
    forkJoin(requests).subscribe((results) => {
      const options: Record<string, FieldOption[]> = {};
      const errors: string[] = [];
      const errorMessages: string[] = [];
      for (const result of results) {
        if ('error' in result) {
          errors.push(result.endpoint);
          errorMessages.push(`${result.endpoint}: ${this.apiError(result.error, 'no se pudo cargar')}`);
          continue;
        }
        this.referenceRecordsCache[result.endpoint] = result.records;
        options[result.endpoint] = result.records.map((record) => ({
          label: recordLabel(record, result.endpoint),
          value: Number(record['id']),
        }));
      }
      this.referenceOptions.set(options);
      this.referenceErrors.set(errors);
      this.referenceErrorSummary.set(errorMessages.join('; '));
    });
  }

  private recordsForReference(endpoint: string): ApiRecord[] {
    const config = RESOURCE_CONFIG_BY_KEY.get(endpoint);
    if (config?.endpoint === this.resource()?.endpoint) {
      return this.records();
    }
    return this.referenceRecordsCache[endpoint] ?? [];
  }

  private readonly referenceRecordsCache: Record<string, ApiRecord[]> = {};

  private defaultValues(fields: ResourceField[]): Record<string, FormValue> {
    const values: Record<string, FormValue> = {};
    for (const field of fields) {
      if (field.type === 'session-lines') {
        continue;
      }
      if (field.type === 'checkbox') {
        values[field.key] = true;
      } else if (field.options?.length) {
        values[field.key] = field.options[0].value;
      } else if (field.type === 'number') {
        values[field.key] = field.min ?? 0;
      } else if (field.type === 'datetime-local') {
        values[field.key] = field.required ? this.localDateTime(new Date()) : '';
      } else {
        values[field.key] = '';
      }
    }
    return values;
  }

  private toFormValue(field: ResourceField, value: unknown): FormValue {
    if (field.type === 'datetime-local' && typeof value === 'string' && value) {
      return this.localDateTime(new Date(value));
    }
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
      return value;
    }
    return null;
  }

  private buildPayload(config: ResourceConfig): ApiRecord {
    const payload: ApiRecord = {};
    for (const field of config.fields) {
      if (field.type === 'session-lines') {
        if (this.editingId() === null) {
          payload['treatment_details'] = this.sessionLines()
            .filter((line) => line.treatment_detail !== null)
            .map((line) => ({
              treatment_detail: line.treatment_detail,
              quantity: Number(line.quantity),
              materials_used: line.materials_used,
            }));
        }
        continue;
      }
      const value = this.formValues()[field.key];
      if (field.type === 'password' && !value) {
        continue;
      }
      if (field.type === 'datetime-local') {
        payload[field.key] = value ? this.toIsoDate(String(value)) : null;
      } else if (field.type === 'date') {
        payload[field.key] = value || null;
      } else if (field.type === 'number' || (field.type === 'select' && field.source)) {
        payload[field.key] = value === '' || value === null ? null : Number(value);
      } else {
        payload[field.key] = value;
      }
    }
    return payload;
  }

  private localDateTime(date: Date): string {
    if (Number.isNaN(date.getTime())) {
      return '';
    }
    const local = new Date(date.getTime() - date.getTimezoneOffset() * 60_000);
    return local.toISOString().slice(0, 16);
  }

  private toIsoDate(value: string): string {
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toISOString();
  }

  private apiError(error: unknown, fallback: string): string {
    if (!(error instanceof HttpErrorResponse)) {
      return fallback;
    }
    if (error.status === 0) {
      return 'No se pudo conectar con Django. Verifica que el servidor esté ejecutándose.';
    }
    if (error.status === 401) {
      return 'Tu sesión expiró. Inicia sesión nuevamente.';
    }
    if (error.status === 403) {
      return 'Tu usuario no tiene permisos para esta operación.';
    }
    const body: unknown = error.error;
    if (typeof body === 'string') {
      return body;
    }
    if (body && typeof body === 'object') {
      const values = Object.values(body as Record<string, unknown>)
        .flatMap((value) => Array.isArray(value) ? value : [value])
        .filter((value): value is string => typeof value === 'string');
      if (values.length) {
        return values.join(' ');
      }
    }
    return fallback;
  }
}
