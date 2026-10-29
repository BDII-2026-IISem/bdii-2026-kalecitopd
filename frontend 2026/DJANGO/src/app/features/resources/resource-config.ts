import { ApiRecord } from '../../core/models';

export type FieldType =
  | 'text'
  | 'email'
  | 'password'
  | 'date'
  | 'datetime-local'
  | 'number'
  | 'textarea'
  | 'select'
  | 'checkbox'
  | 'session-lines';

export interface FieldOption {
  label: string;
  value: string | number;
}

export interface ResourceField {
  key: string;
  label: string;
  type: FieldType;
  required?: boolean;
  step?: string;
  min?: number;
  source?: string;
  options?: FieldOption[];
  help?: string;
}

export interface ResourceColumn {
  key: string;
  label: string;
  source?: string;
}

export interface ResourceConfig {
  key: string;
  endpoint: string;
  resource: string;
  title: string;
  singular: string;
  description: string;
  icon: string;
  columns: ResourceColumn[];
  fields: ResourceField[];
  canDelete: boolean;
  nestedEvolution?: boolean;
}

const appointmentStatuses: FieldOption[] = [
  { label: 'Programada', value: 'scheduled' },
  { label: 'Confirmada', value: 'confirmed' },
  { label: 'Completada', value: 'completed' },
  { label: 'Cancelada', value: 'cancelled' },
  { label: 'No asistió', value: 'no_show' },
];

const planStatuses: FieldOption[] = [
  { label: 'Borrador', value: 'draft' },
  { label: 'Activo', value: 'active' },
  { label: 'Completado', value: 'completed' },
  { label: 'Cancelado', value: 'cancelled' },
];

const sessionStatuses: FieldOption[] = [
  { label: 'Programada', value: 'scheduled' },
  { label: 'En curso', value: 'in_progress' },
  { label: 'Completada', value: 'completed' },
  { label: 'Cancelada', value: 'cancelled' },
];

const paymentStatuses: FieldOption[] = [
  { label: 'Pendiente', value: 'pending' },
  { label: 'Confirmado', value: 'confirmed' },
  { label: 'Cancelado', value: 'cancelled' },
];

const paymentMethods: FieldOption[] = [
  { label: 'Efectivo', value: 'cash' },
  { label: 'Tarjeta', value: 'card' },
  { label: 'Transferencia', value: 'transfer' },
  { label: 'Otro', value: 'other' },
];

export const RESOURCE_CONFIGS: ResourceConfig[] = [
  {
    key: 'pacientes',
    endpoint: 'pacientes',
    resource: 'pacientes',
    title: 'Pacientes',
    singular: 'paciente',
    description: 'Administra los datos y el contacto de cada paciente.',
    icon: 'pi pi-users',
    canDelete: true,
    columns: [
      { key: 'first_name', label: 'Nombres' },
      { key: 'last_name', label: 'Apellidos' },
      { key: 'document_number', label: 'Documento' },
      { key: 'phone', label: 'Teléfono' },
      { key: 'email', label: 'Correo' },
    ],
    fields: [
      { key: 'document_type', label: 'Tipo de documento', type: 'text', required: true },
      { key: 'document_number', label: 'Número de documento', type: 'text' },
      { key: 'first_name', label: 'Nombres', type: 'text', required: true },
      { key: 'last_name', label: 'Apellidos', type: 'text', required: true },
      { key: 'email', label: 'Correo electrónico', type: 'email', required: true },
      { key: 'phone', label: 'Teléfono', type: 'text', required: true },
      { key: 'address', label: 'Dirección', type: 'textarea' },
      { key: 'date_of_birth', label: 'Fecha de nacimiento', type: 'date' },
    ],
  },
  {
    key: 'odontologos',
    endpoint: 'odontologos',
    resource: 'odontologos',
    title: 'Odontólogos',
    singular: 'odontólogo',
    description: 'Gestiona el equipo odontológico de la clínica.',
    icon: 'pi pi-heart',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Nombre' },
      { key: 'description', label: 'Descripción' },
      { key: 'is_active', label: 'Estado' },
    ],
    fields: [
      { key: 'name', label: 'Nombre', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
      { key: 'is_active', label: 'Activo', type: 'checkbox' },
    ],
  },
  {
    key: 'sillones',
    endpoint: 'sillones',
    resource: 'sillones',
    title: 'Sillones',
    singular: 'sillón',
    description: 'Controla los sillones disponibles para la agenda.',
    icon: 'pi pi-stop',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Nombre' },
      { key: 'description', label: 'Descripción' },
      { key: 'is_active', label: 'Estado' },
    ],
    fields: [
      { key: 'name', label: 'Nombre', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
      { key: 'is_active', label: 'Activo', type: 'checkbox' },
    ],
  },
  {
    key: 'citas',
    endpoint: 'citas',
    resource: 'citas',
    title: 'Citas',
    singular: 'cita',
    description: 'Organiza y actualiza la agenda de atención.',
    icon: 'pi pi-calendar',
    canDelete: false,
    columns: [
      { key: 'start_time', label: 'Fecha y hora' },
      { key: 'patient', label: 'Paciente', source: 'pacientes' },
      { key: 'odontologist', label: 'Odontólogo', source: 'odontologos' },
      { key: 'chair', label: 'Sillón', source: 'sillones' },
      { key: 'motive', label: 'Motivo' },
      { key: 'status', label: 'Estado' },
    ],
    fields: [
      { key: 'patient', label: 'Paciente', type: 'select', required: true, source: 'pacientes' },
      { key: 'odontologist', label: 'Odontólogo', type: 'select', required: true, source: 'odontologos' },
      { key: 'chair', label: 'Sillón', type: 'select', required: true, source: 'sillones' },
      { key: 'start_time', label: 'Inicio', type: 'datetime-local', required: true },
      { key: 'end_time', label: 'Fin', type: 'datetime-local', required: true },
      { key: 'motive', label: 'Motivo', type: 'text', required: true },
      { key: 'status', label: 'Estado', type: 'select', required: true, options: appointmentStatuses },
    ],
  },
  {
    key: 'historias',
    endpoint: 'historias',
    resource: 'historias',
    title: 'Historias clínicas',
    singular: 'historia clínica',
    description: 'Consulta historias y registra evoluciones clínicas.',
    icon: 'pi pi-file-edit',
    canDelete: false,
    nestedEvolution: true,
    columns: [
      { key: 'name', label: 'Historia' },
      { key: 'patient', label: 'Paciente', source: 'pacientes' },
      { key: 'is_active', label: 'Estado' },
      { key: 'evolutions', label: 'Evoluciones' },
    ],
    fields: [
      { key: 'patient', label: 'Paciente', type: 'select', required: true, source: 'pacientes' },
      { key: 'name', label: 'Nombre de historia', type: 'text', required: true },
      { key: 'description', label: 'Antecedentes y observaciones', type: 'textarea' },
      { key: 'is_active', label: 'Activa', type: 'checkbox' },
    ],
  },
  {
    key: 'tratamientos',
    endpoint: 'tratamientos',
    resource: 'tratamientos',
    title: 'Planes de tratamiento',
    singular: 'plan',
    description: 'Define el plan clínico y consulta su saldo.',
    icon: 'pi pi-list-check',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Plan' },
      { key: 'patient', label: 'Paciente', source: 'pacientes' },
      { key: 'status', label: 'Estado' },
      { key: 'total_amount', label: 'Total' },
      { key: 'paid_amount', label: 'Pagado' },
      { key: 'balance_due', label: 'Saldo' },
    ],
    fields: [
      { key: 'patient', label: 'Paciente', type: 'select', required: true, source: 'pacientes' },
      { key: 'name', label: 'Nombre del plan', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
      { key: 'status', label: 'Estado', type: 'select', required: true, options: planStatuses },
    ],
  },
  {
    key: 'procedimientos',
    endpoint: 'procedimientos',
    resource: 'procedimientos',
    title: 'Procedimientos',
    singular: 'procedimiento',
    description: 'Mantén actualizado el catálogo de procedimientos odontológicos.',
    icon: 'pi pi-wrench',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Nombre' },
      { key: 'description', label: 'Descripción' },
      { key: 'is_active', label: 'Estado' },
    ],
    fields: [
      { key: 'name', label: 'Nombre', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
      { key: 'is_active', label: 'Activo', type: 'checkbox' },
    ],
  },
  {
    key: 'detalles-tratamiento',
    endpoint: 'detalles-tratamiento',
    resource: 'detalles-tratamiento',
    title: 'Detalles de tratamiento',
    singular: 'detalle',
    description: 'Asigna procedimientos, cantidades aprobadas y valores a cada plan.',
    icon: 'pi pi-clipboard',
    canDelete: true,
    columns: [
      { key: 'treatment_plan', label: 'Plan', source: 'tratamientos' },
      { key: 'procedure', label: 'Procedimiento', source: 'procedimientos' },
      { key: 'quantity', label: 'Cantidad' },
      { key: 'approved_quantity', label: 'Aprobados' },
      { key: 'unit_price', label: 'Valor unitario' },
      { key: 'total', label: 'Total' },
    ],
    fields: [
      { key: 'treatment_plan', label: 'Plan de tratamiento', type: 'select', required: true, source: 'tratamientos' },
      { key: 'procedure', label: 'Procedimiento', type: 'select', required: true, source: 'procedimientos' },
      { key: 'quantity', label: 'Cantidad planeada', type: 'number', required: true, min: 1, step: '1' },
      { key: 'approved_quantity', label: 'Cantidad aprobada', type: 'number', required: true, min: 0, step: '1' },
      { key: 'unit_price', label: 'Valor unitario', type: 'number', required: true, min: 0, step: '0.01' },
      { key: 'observations', label: 'Observaciones', type: 'textarea' },
    ],
  },
  {
    key: 'sesiones',
    endpoint: 'sesiones',
    resource: 'sesiones',
    title: 'Sesiones clínicas',
    singular: 'sesión',
    description: 'Registra la atención y los procedimientos ejecutados.',
    icon: 'pi pi-clock',
    canDelete: false,
    columns: [
      { key: 'start_time', label: 'Inicio' },
      { key: 'appointment', label: 'Cita', source: 'citas' },
      { key: 'treatment_plan', label: 'Plan', source: 'tratamientos' },
      { key: 'status', label: 'Estado' },
      { key: 'total', label: 'Total ejecutado' },
    ],
    fields: [
      { key: 'appointment', label: 'Cita', type: 'select', required: true, source: 'citas' },
      { key: 'treatment_plan', label: 'Plan de tratamiento', type: 'select', required: true, source: 'tratamientos' },
      { key: 'start_time', label: 'Inicio', type: 'datetime-local', required: true },
      { key: 'end_time', label: 'Fin', type: 'datetime-local' },
      { key: 'status', label: 'Estado', type: 'select', required: true, options: sessionStatuses },
      { key: 'observations', label: 'Observaciones', type: 'textarea' },
      {
        key: 'treatment_details',
        label: 'Procedimientos ejecutados',
        type: 'session-lines',
        source: 'detalles-tratamiento',
        help: 'Solo se pueden registrar procedimientos aprobados del plan elegido.',
      },
    ],
  },
  {
    key: 'pagos',
    endpoint: 'pagos',
    resource: 'pagos',
    title: 'Pagos',
    singular: 'pago',
    description: 'Registra abonos y consulta el estado de cartera.',
    icon: 'pi pi-wallet',
    canDelete: false,
    columns: [
      { key: 'treatment_plan', label: 'Plan', source: 'tratamientos' },
      { key: 'amount', label: 'Monto' },
      { key: 'method', label: 'Método' },
      { key: 'paid_at', label: 'Fecha' },
      { key: 'status', label: 'Estado' },
    ],
    fields: [
      { key: 'treatment_plan', label: 'Plan', type: 'select', required: true, source: 'tratamientos' },
      { key: 'method', label: 'Método de pago', type: 'select', required: true, options: paymentMethods },
      { key: 'amount', label: 'Monto', type: 'number', required: true, min: 0.01, step: '0.01' },
      { key: 'paid_at', label: 'Fecha de pago', type: 'datetime-local', required: true },
      { key: 'status', label: 'Estado', type: 'select', required: true, options: paymentStatuses },
    ],
  },
  {
    key: 'users',
    endpoint: 'users',
    resource: 'users',
    title: 'Usuarios',
    singular: 'usuario',
    description: 'Administra las cuentas de acceso y su estado.',
    icon: 'pi pi-user',
    canDelete: true,
    columns: [
      { key: 'username', label: 'Usuario' },
      { key: 'first_name', label: 'Nombres' },
      { key: 'last_name', label: 'Apellidos' },
      { key: 'email', label: 'Correo' },
      { key: 'is_active', label: 'Estado' },
    ],
    fields: [
      { key: 'username', label: 'Nombre de usuario', type: 'text', required: true },
      { key: 'password', label: 'Contraseña', type: 'password', required: true, help: 'Al editar, deja este campo vacío para mantener la contraseña actual.' },
      { key: 'first_name', label: 'Nombres', type: 'text' },
      { key: 'last_name', label: 'Apellidos', type: 'text' },
      { key: 'email', label: 'Correo electrónico', type: 'email' },
      { key: 'phone', label: 'Teléfono', type: 'text' },
      { key: 'is_active', label: 'Cuenta activa', type: 'checkbox' },
    ],
  },
  {
    key: 'roles',
    endpoint: 'roles',
    resource: 'roles',
    title: 'Roles',
    singular: 'rol',
    description: 'Define los perfiles de acceso de la clínica.',
    icon: 'pi pi-shield',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Rol' },
      { key: 'description', label: 'Descripción' },
    ],
    fields: [
      { key: 'name', label: 'Nombre del rol', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
    ],
  },
  {
    key: 'role-users',
    endpoint: 'role-users',
    resource: 'role-users',
    title: 'Asignación de roles',
    singular: 'asignación',
    description: 'Asigna uno o más roles a las cuentas de usuario.',
    icon: 'pi pi-user-plus',
    canDelete: true,
    columns: [
      { key: 'user', label: 'Usuario', source: 'users' },
      { key: 'role', label: 'Rol', source: 'roles' },
    ],
    fields: [
      { key: 'user', label: 'Usuario', type: 'select', required: true, source: 'users' },
      { key: 'role', label: 'Rol', type: 'select', required: true, source: 'roles' },
    ],
  },
  {
    key: 'resources',
    endpoint: 'resources',
    resource: 'resources',
    title: 'Recursos del sistema',
    singular: 'recurso',
    description: 'Administra los recursos que protegen los endpoints de la API.',
    icon: 'pi pi-database',
    canDelete: true,
    columns: [
      { key: 'name', label: 'Recurso' },
      { key: 'description', label: 'Descripción' },
    ],
    fields: [
      { key: 'name', label: 'Nombre de recurso', type: 'text', required: true },
      { key: 'description', label: 'Descripción', type: 'textarea' },
    ],
  },
  {
    key: 'resource-roles',
    endpoint: 'resource-roles',
    resource: 'resource-roles',
    title: 'Permisos por rol',
    singular: 'permiso',
    description: 'Concede a cada rol acceso a los recursos definidos.',
    icon: 'pi pi-lock',
    canDelete: true,
    columns: [
      { key: 'role', label: 'Rol', source: 'roles' },
      { key: 'resource', label: 'Recurso', source: 'resources' },
    ],
    fields: [
      { key: 'role', label: 'Rol', type: 'select', required: true, source: 'roles' },
      { key: 'resource', label: 'Recurso', type: 'select', required: true, source: 'resources' },
    ],
  },
];

export const RESOURCE_CONFIG_BY_KEY = new Map(
  RESOURCE_CONFIGS.map((resource) => [resource.key, resource]),
);

export const REFERENCE_LABELS: Record<string, (record: ApiRecord) => string> = {
  pacientes: (record) => `${record['first_name'] ?? ''} ${record['last_name'] ?? ''}`.trim(),
  odontologos: (record) => String(record['name'] ?? ''),
  sillones: (record) => String(record['name'] ?? ''),
  citas: (record) => {
    const appointment = record as ApiRecord;
    return `#${appointment['id']} · ${appointment['motive'] ?? ''}`;
  },
  tratamientos: (record) => String(record['name'] ?? ''),
  procedimientos: (record) => String(record['name'] ?? ''),
  'detalles-tratamiento': (record) =>
    `Detalle #${record['id']} · ${record['approved_quantity'] ?? 0} aprobados`,
  roles: (record) => String(record['name'] ?? ''),
  resources: (record) => String(record['name'] ?? ''),
  users: (record) => `${record['username'] ?? ''} · ${record['first_name'] ?? ''} ${record['last_name'] ?? ''}`.trim(),
};

export function recordLabel(record: ApiRecord, source: string): string {
  return REFERENCE_LABELS[source]?.(record) ?? String(record['id'] ?? '');
}
