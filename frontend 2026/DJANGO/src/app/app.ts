import { Component, computed, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';
import { AuthService } from './core/auth.service';

interface NavigationItem {
  label: string;
  icon: string;
  resource: string;
  url: string;
}

interface NavigationGroup {
  label: string;
  items: NavigationItem[];
}

@Component({
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  private readonly router = inject(Router);
  protected readonly auth = inject(AuthService);
  protected readonly pageTitle = signal('Resumen');
  protected readonly logoutMessage = signal('');
  protected readonly refreshingPermissions = signal(false);
  protected readonly permissionMessage = signal('');
  protected readonly todayLabel = new Intl.DateTimeFormat('es', {
    dateStyle: 'full',
  }).format(new Date());
  private readonly allNavigation: NavigationGroup[] = [
    {
      label: 'ATENCIÓN',
      items: [
        { label: 'Pacientes', icon: 'pi pi-users', resource: 'pacientes', url: '/resources/pacientes' },
        { label: 'Citas', icon: 'pi pi-calendar', resource: 'citas', url: '/resources/citas' },
        { label: 'Odontólogos', icon: 'pi pi-heart', resource: 'odontologos', url: '/resources/odontologos' },
        { label: 'Sillones', icon: 'pi pi-stop', resource: 'sillones', url: '/resources/sillones' },
        { label: 'Historias clínicas', icon: 'pi pi-file-edit', resource: 'historias', url: '/resources/historias' },
      ],
    },
    {
      label: 'TRATAMIENTOS',
      items: [
        { label: 'Planes', icon: 'pi pi-list-check', resource: 'tratamientos', url: '/resources/tratamientos' },
        { label: 'Procedimientos', icon: 'pi pi-wrench', resource: 'procedimientos', url: '/resources/procedimientos' },
        { label: 'Detalles', icon: 'pi pi-clipboard', resource: 'detalles-tratamiento', url: '/resources/detalles-tratamiento' },
        { label: 'Sesiones', icon: 'pi pi-clock', resource: 'sesiones', url: '/resources/sesiones' },
        { label: 'Pagos', icon: 'pi pi-wallet', resource: 'pagos', url: '/resources/pagos' },
      ],
    },
    {
      label: 'ADMINISTRACIÓN',
      items: [
        { label: 'Usuarios', icon: 'pi pi-user', resource: 'users', url: '/resources/users' },
        { label: 'Roles', icon: 'pi pi-shield', resource: 'roles', url: '/resources/roles' },
        { label: 'Usuarios por rol', icon: 'pi pi-user-plus', resource: 'role-users', url: '/resources/role-users' },
        { label: 'Recursos', icon: 'pi pi-database', resource: 'resources', url: '/resources/resources' },
        { label: 'Permisos', icon: 'pi pi-lock', resource: 'resource-roles', url: '/resources/resource-roles' },
      ],
    },
  ];
  protected readonly navigationGroups = computed(() =>
    this.allNavigation
      .map((group) => ({
        ...group,
        items: group.items.filter((item) => this.auth.canResource(item.resource)),
      }))
      .filter((group) => group.items.length > 0),
  );
  protected readonly userInitials = computed(() => {
    const user = this.auth.user();
    const name = user?.first_name || user?.username || 'O';
    const surname = user?.last_name || '';
    return `${name.charAt(0)}${surname.charAt(0)}`.toUpperCase();
  });

  constructor() {
    this.router.events
      .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
      .subscribe((event) => {
        const resource = event.urlAfterRedirects.match(/^\/resources\/([^/?]+)/)?.[1];
        this.pageTitle.set(
          (resource && this.resourceTitles[resource]) ||
            (event.urlAfterRedirects === '/dashboard' ? 'Resumen' : 'OdontoNova'),
        );
        this.logoutMessage.set('');
        this.permissionMessage.set('');
      });
  }

  private readonly resourceTitles: Record<string, string> = {
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
    'role-users': 'Asignación de roles',
    resources: 'Recursos del sistema',
    'resource-roles': 'Permisos por rol',
  };

  protected logout(): void {
    this.auth.logout().subscribe({
      error: () => this.logoutMessage.set('La sesión se cerró en este navegador, pero no se pudo revocar en el servidor.'),
    });
  }

  protected refreshPermissions(): void {
    if (this.refreshingPermissions()) {
      return;
    }
    this.refreshingPermissions.set(true);
    this.auth.refreshPermissions().subscribe({
      next: () => {
        this.permissionMessage.set('Permisos actualizados.');
        const resource = this.router.url.match(/^\/resources\/([^/?]+)/)?.[1];
        if (resource && !this.auth.canResource(resource)) {
          void this.router.navigateByUrl('/forbidden');
        }
      },
      error: () => this.permissionMessage.set('No se pudieron actualizar los permisos. Verifica tu sesión y vuelve a intentar.'),
    }).add(() => this.refreshingPermissions.set(false));
  }
}
