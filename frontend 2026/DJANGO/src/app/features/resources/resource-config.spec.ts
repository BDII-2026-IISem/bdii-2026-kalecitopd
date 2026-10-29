import { describe, expect, it } from 'vitest';
import { RESOURCE_CONFIGS } from './resource-config';

describe('OdontoNova resource configuration', () => {
  it('covers every active clinical and security API resource', () => {
    expect(RESOURCE_CONFIGS.map((resource) => resource.endpoint)).toEqual([
      'pacientes',
      'odontologos',
      'sillones',
      'citas',
      'historias',
      'tratamientos',
      'procedimientos',
      'detalles-tratamiento',
      'sesiones',
      'pagos',
      'users',
      'roles',
      'role-users',
      'resources',
      'resource-roles',
    ]);
  });

  it('does not expose destructive deletion for protected business records', () => {
    expect(RESOURCE_CONFIGS.find((resource) => resource.key === 'citas')?.canDelete).toBe(false);
    expect(RESOURCE_CONFIGS.find((resource) => resource.key === 'historias')?.canDelete).toBe(false);
    expect(RESOURCE_CONFIGS.find((resource) => resource.key === 'sesiones')?.canDelete).toBe(false);
    expect(RESOURCE_CONFIGS.find((resource) => resource.key === 'pagos')?.canDelete).toBe(false);
  });
});
