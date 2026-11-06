import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { forkJoin, map, Observable, of } from 'rxjs';
import { ApiRecord } from '../../core/models';
import { AuthService } from '../../core/auth.service';
import { DentalApiService } from '../../core/dental-api.service';

type RbacTab = 'roles' | 'users' | 'resources';
type CrudKey = 'can_create' | 'can_read' | 'can_update' | 'can_delete';

interface CrudPermissions {
  can_create: boolean;
  can_read: boolean;
  can_update: boolean;
  can_delete: boolean;
}

const EMPTY_PERMISSIONS: CrudPermissions = {
  can_create: false,
  can_read: false,
  can_update: false,
  can_delete: false,
};

@Component({
  imports: [FormsModule],
  selector: 'app-rbac-page',
  templateUrl: './rbac-page.html',
  styleUrl: './rbac-page.css',
})
export class RbacPage {
  private readonly api = inject(DentalApiService);
  protected readonly auth = inject(AuthService);

  protected readonly activeTab = signal<RbacTab>('roles');
  protected readonly roles = signal<ApiRecord[]>([]);
  protected readonly users = signal<ApiRecord[]>([]);
  protected readonly resources = signal<ApiRecord[]>([]);
  protected readonly roleUsers = signal<ApiRecord[]>([]);
  protected readonly grants = signal<ApiRecord[]>([]);
  protected readonly selectedRoleId = signal<number | null>(null);
  protected readonly selectedUserId = signal<number | null>(null);
  protected readonly roleName = signal('');
  protected readonly roleDescription = signal('');
  protected readonly resourceName = signal('');
  protected readonly resourceDescription = signal('');
  protected readonly assignmentOptionId = signal<number | null>(null);
  protected readonly permissionDraft = signal<Record<number, CrudPermissions>>({});
  protected readonly search = signal('');
  protected readonly loading = signal(true);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly successMessage = signal('');

  protected readonly selectedRole = computed(
    () => this.roles().find((role) => this.recordId(role) === this.selectedRoleId()) ?? null,
  );
  protected readonly filteredRoles = computed(() => {
    const query = this.search().trim().toLocaleLowerCase();
    return this.roles().filter((role) =>
      `${this.text(role, 'name')} ${this.text(role, 'description')}`.toLocaleLowerCase().includes(query),
    );
  });
  protected readonly selectedUser = computed(
    () => this.users().find((user) => this.recordId(user) === this.selectedUserId()) ?? null,
  );
  protected readonly userRoleAssignments = computed(() =>
    this.roleUsers().filter((assignment) => Number(assignment['user']) === this.selectedUserId()),
  );
  constructor() {
    this.reload();
  }

  protected reload(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    forkJoin({
      roles: this.api.list('roles'),
      users: this.auth.canResource('users') ? this.api.list('users') : of([]),
      resources: this.auth.canResource('resources') ? this.api.list('resources') : of([]),
      roleUsers: this.auth.canResource('role-users') ? this.api.list('role-users') : of([]),
      grants: this.auth.canResource('resource-roles') ? this.api.list('resource-roles') : of([]),
    }).subscribe({
      next: (data) => {
        this.roles.set(data.roles);
        this.users.set(data.users);
        this.resources.set(data.resources);
        this.roleUsers.set(data.roleUsers);
        this.grants.set(data.grants);
        const selected = this.roles().some((role) => this.recordId(role) === this.selectedRoleId())
          ? this.selectedRoleId()
          : this.roles().length > 0 ? this.recordId(this.roles()[0]) : null;
        if (selected !== null) {
          this.selectRole(selected);
        } else {
          this.selectedRoleId.set(null);
          this.beginNewRole();
        }
        if (!this.users().some((user) => this.recordId(user) === this.selectedUserId())) {
          this.selectedUserId.set(this.users().length ? this.recordId(this.users()[0]) : null);
        }
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.loading.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected selectTab(tab: RbacTab): void {
    this.activeTab.set(tab);
    this.successMessage.set('');
    this.errorMessage.set('');
  }

  protected selectRole(id: number): void {
    const role = this.roles().find((item) => this.recordId(item) === id);
    if (!role) {
      return;
    }
    this.selectedRoleId.set(id);
    this.roleName.set(this.text(role, 'name'));
    this.roleDescription.set(this.text(role, 'description'));
    const draft: Record<number, CrudPermissions> = {};
    for (const resource of this.resources()) {
      const grant = this.grants().find(
        (item) => Number(item['role']) === id && Number(item['resource']) === this.recordId(resource),
      );
      draft[this.recordId(resource)] = grant ? this.readPermissions(grant) : { ...EMPTY_PERMISSIONS };
    }
    this.permissionDraft.set(draft);
  }

  protected beginNewRole(): void {
    this.selectedRoleId.set(null);
    this.roleName.set('');
    this.roleDescription.set('');
    const draft: Record<number, CrudPermissions> = {};
    for (const resource of this.resources()) {
      draft[this.recordId(resource)] = { ...EMPTY_PERMISSIONS };
    }
    this.permissionDraft.set(draft);
  }

  protected saveRole(): void {
    const name = this.roleName().trim();
    if (!name) {
      this.errorMessage.set('Escribe el nombre del rol.');
      return;
    }
    if (this.saving()) {
      return;
    }

    this.saving.set(true);
    this.errorMessage.set('');
    const currentId = this.selectedRoleId();
    const roleRequest = currentId === null
      ? this.api.create('roles', { name, description: this.roleDescription().trim() })
      : this.api.update('roles', currentId, { name, description: this.roleDescription().trim() });

    roleRequest.subscribe({
      next: (savedRole) => {
        const roleId = this.recordId(savedRole);
        const requests = currentId === null ? [] : this.permissionRequests(roleId);
        this.finishSave(requests, 'Rol y permisos guardados correctamente.', roleId);
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected deleteRole(): void {
    const id = this.selectedRoleId();
    const role = this.selectedRole();
    if (id === null || !role || !this.canDeleteRoles() || this.saving()) {
      return;
    }
    if (!window.confirm(`¿Eliminar el rol ${this.text(role, 'name')} y sus asignaciones? Esta acción no se puede deshacer.`)) {
      return;
    }
    this.saving.set(true);
    this.api.remove('roles', id).subscribe({
      next: () => {
        this.saving.set(false);
        this.successMessage.set('Rol eliminado correctamente.');
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected setPermission(resourceId: number, key: CrudKey, checked: boolean): void {
    this.permissionDraft.update((draft) => ({
      ...draft,
      [resourceId]: { ...(draft[resourceId] ?? EMPTY_PERMISSIONS), [key]: checked },
    }));
  }

  protected permission(resourceId: number, key: CrudKey): boolean {
    return this.permissionDraft()[resourceId]?.[key] ?? false;
  }

  protected markAllPermissions(checked: boolean): void {
    const draft: Record<number, CrudPermissions> = {};
    for (const resource of this.resources()) {
      draft[this.recordId(resource)] = {
        can_create: checked,
        can_read: checked,
        can_update: checked,
        can_delete: checked,
      };
    }
    this.permissionDraft.set(draft);
  }

  protected savePermissions(): void {
    const roleId = this.selectedRoleId();
    if (roleId === null || !this.canEditGrants() || this.saving()) {
      return;
    }
    this.saving.set(true);
    this.finishSave(this.permissionRequests(roleId), 'Permisos guardados correctamente.', roleId);
  }

  protected setSelectedUser(value: string | number | null): void {
    const id = Number(value);
    this.selectedUserId.set(Number.isFinite(id) && id > 0 ? id : null);
  }

  protected setAssignmentOption(value: string | number | null): void {
    const id = Number(value);
    this.assignmentOptionId.set(Number.isFinite(id) && id > 0 ? id : null);
  }

  protected assignRole(): void {
    const userId = this.activeTab() === 'roles' ? this.assignmentOptionId() : this.selectedUserId();
    const roleId = this.activeTab() === 'roles' ? this.selectedRoleId() : this.assignmentOptionId();
    if (userId === null || roleId === null || !this.auth.canPermission('POST', '/api/role-users/')) {
      return;
    }
    this.saving.set(true);
    this.api.create('role-users', { user: userId, role: roleId }).subscribe({
      next: () => {
        this.assignmentOptionId.set(null);
        this.saving.set(false);
        this.successMessage.set('Rol asignado al usuario.');
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected removeAssignment(assignment: ApiRecord): void {
    if (!this.auth.canPermission('DELETE', '/api/role-users/') || this.saving()) {
      return;
    }
    this.saving.set(true);
    this.api.remove('role-users', this.recordId(assignment)).subscribe({
      next: () => {
        this.saving.set(false);
        this.successMessage.set('Asignación de rol eliminada.');
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected createResource(): void {
    const name = this.resourceName().trim();
    if (!name || !this.auth.canPermission('POST', '/api/resources/')) {
      return;
    }
    this.saving.set(true);
    this.api.create('resources', { name, description: this.resourceDescription().trim() }).subscribe({
      next: () => {
        this.resourceName.set('');
        this.resourceDescription.set('');
        this.saving.set(false);
        this.successMessage.set('Recurso creado.');
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected deleteResource(resource: ApiRecord): void {
    if (!this.auth.canPermission('DELETE', '/api/resources/') || this.saving()) {
      return;
    }
    const name = this.text(resource, 'name');
    if (!window.confirm(`¿Eliminar el recurso ${name} y los permisos asociados?`)) {
      return;
    }
    this.saving.set(true);
    this.api.remove('resources', this.recordId(resource)).subscribe({
      next: () => {
        this.saving.set(false);
        this.successMessage.set('Recurso eliminado.');
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  protected canCreateRoles(): boolean {
    return this.auth.canPermission('POST', '/api/roles/');
  }

  protected canEditRoles(): boolean {
    return this.auth.canPermission('PATCH', '/api/roles/');
  }

  protected canDeleteRoles(): boolean {
    return this.auth.canPermission('DELETE', '/api/roles/');
  }

  protected canEditGrants(): boolean {
    return this.auth.canPermission('POST', '/api/resource-roles/') &&
      this.auth.canPermission('PATCH', '/api/resource-roles/') &&
      this.auth.canPermission('DELETE', '/api/resource-roles/');
  }

  protected canEditAssignments(): boolean {
    return this.auth.canPermission('POST', '/api/role-users/') ||
      this.auth.canPermission('DELETE', '/api/role-users/');
  }

  protected canCreateResources(): boolean {
    return this.auth.canPermission('POST', '/api/resources/');
  }

  protected canDeleteResources(): boolean {
    return this.auth.canPermission('DELETE', '/api/resources/');
  }

  protected canShowUsersTab(): boolean {
    return this.auth.canResource('users') && this.auth.canResource('role-users');
  }

  protected canShowResourcesTab(): boolean {
    return this.auth.canResource('resources') && this.auth.canResource('resource-roles');
  }

  protected userLabel(user: ApiRecord): string {
    const name = `${this.text(user, 'first_name')} ${this.text(user, 'last_name')}`.trim();
    return name || this.text(user, 'username');
  }

  protected hasRoleAssignment(roleId: number | null): boolean {
    return roleId !== null && this.roleUsers().some((item) => Number(item['role']) === roleId);
  }

  protected isAssignmentForRole(assignment: ApiRecord): boolean {
    return Number(assignment['role']) === this.selectedRoleId();
  }

  protected isUserAssignedToSelectedRole(userId: number): boolean {
    return this.roleUsers().some(
      (item) => Number(item['role']) === this.selectedRoleId() && Number(item['user']) === userId,
    );
  }

  protected userForAssignment(assignment: ApiRecord): ApiRecord | null {
    return this.users().find((user) => this.recordId(user) === Number(assignment['user'])) ?? null;
  }

  protected roleForAssignment(assignment: ApiRecord): ApiRecord | null {
    return this.roles().find((role) => this.recordId(role) === Number(assignment['role'])) ?? null;
  }

  protected selectedUserHasRole(roleId: number): boolean {
    return this.userRoleAssignments().some((item) => Number(item['role']) === roleId);
  }

  protected resourceLabel(resource: ApiRecord): string {
    const labels: Record<string, string> = {
      pacientes: 'Pacientes',
      odontologos: 'Odontólogos',
      sillones: 'Sillones',
      citas: 'Citas',
      historias: 'Historias clínicas',
      tratamientos: 'Planes de tratamiento',
      procedimientos: 'Procedimientos',
      'detalles-tratamiento': 'Detalles de tratamiento',
      sesiones: 'Sesiones clínicas',
      pagos: 'Pagos',
      users: 'Usuarios',
      roles: 'Roles',
      'role-users': 'Asignaciones de roles',
      resources: 'Recursos',
      'resource-roles': 'Permisos por rol',
    };
    const name = this.text(resource, 'name');
    return labels[name] ?? name.replaceAll('-', ' ').replace(/\b\w/g, (letter) => letter.toLocaleUpperCase());
  }

  protected recordId(record: ApiRecord): number {
    return Number(record['id']);
  }

  protected text(record: ApiRecord, key: string): string {
    const value = record[key];
    return typeof value === 'string' ? value : '';
  }

  private permissionRequests(roleId: number): Observable<void>[] {
    return this.resources().flatMap((resource) => {
      const resourceId = this.recordId(resource);
      const draft = this.permissionDraft()[resourceId] ?? EMPTY_PERMISSIONS;
      const current = this.grants().find(
        (grant) => Number(grant['role']) === roleId && Number(grant['resource']) === resourceId,
      );
      const hasAnyPermission = Object.values(draft).some(Boolean);
      if (current && !hasAnyPermission) {
        return [
          this.api.remove('resource-roles', this.recordId(current)).pipe(map(() => undefined)),
        ];
      }
      if (!current && hasAnyPermission) {
        return [
          this.api.create('resource-roles', { role: roleId, resource: resourceId, ...draft })
            .pipe(map(() => undefined)),
        ];
      }
      if (current && hasAnyPermission && !this.samePermissions(current, draft)) {
        return [
          this.api.update('resource-roles', this.recordId(current), { ...draft })
            .pipe(map(() => undefined)),
        ];
      }
      return [];
    });
  }

  private samePermissions(record: ApiRecord, permissions: CrudPermissions): boolean {
    return (['can_create', 'can_read', 'can_update', 'can_delete'] as CrudKey[])
      .every((key) => Boolean(record[key]) === permissions[key]);
  }

  private readPermissions(record: ApiRecord): CrudPermissions {
    return {
      can_create: Boolean(record['can_create']),
      can_read: Boolean(record['can_read']),
      can_update: Boolean(record['can_update']),
      can_delete: Boolean(record['can_delete']),
    };
  }

  private finishSave(requests: Observable<unknown>[], message: string, roleId: number): void {
    const operation = requests.length ? forkJoin(requests) : of([]);
    operation.subscribe({
      next: () => {
        this.saving.set(false);
        this.successMessage.set(message);
        this.selectedRoleId.set(roleId);
        this.reload();
      },
      error: (error: unknown) => {
        this.saving.set(false);
        this.errorMessage.set(this.apiError(error));
      },
    });
  }

  private apiError(error: unknown): string {
    const detail = (error as { error?: { detail?: unknown } })?.error?.detail;
    return typeof detail === 'string' ? detail : 'No fue posible completar la operación. Verifica tus permisos e intenta de nuevo.';
  }
}
