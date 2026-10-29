export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: UserProfile;
}

export interface Patient {
  id: number;
  document_type: string;
  document_number: string | null;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: string | null;
  date_of_birth: string | null;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: number;
  patient: number;
  odontologist: number;
  chair: number;
  start_time: string;
  end_time: string;
  motive: string;
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled' | 'no_show';
  created_at: string;
  updated_at: string;
}

export interface AccessGrant {
  resource: string;
  method: string;
  path: string;
  roleId: number | null;
  roleName: string;
}

export interface PermissionsResponse {
  permissions: AccessGrant[];
}

export type ApiRecord = Record<string, unknown>;

export interface ApiErrorResponse {
  detail?: string;
  [key: string]: unknown;
}
