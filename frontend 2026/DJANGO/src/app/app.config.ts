import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeuix/themes/aura';
import { routes } from './app.routes';
import { authInterceptor } from './core/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withInterceptors([authInterceptor])),
    provideRouter(routes),
    providePrimeNG({
       license: 'eyJpZCI6IjVkZDAyOTE4LTBjZWYtNDc4Ny04OTMwLTc5MmZkZWYwNmE3NiIsInByb2R1Y3QiOiJwcmltZXVpIiwidGllciI6ImNvbW11bml0eSIsInR5cGUiOiJkZXYiLCJpYXQiOjE3OTM4OTU1NDUsImV4cCI6MTgyNTQzMTU0NX0.eGTOCaO2vV9Cf9_2r8xWp-RHtX4FjMJXI5cL8g5XSFBbvDkKzUbEeO1EcLAX-OqnKaakZevAnY5NF3bHLNnDBw',
      theme: {
        preset: Aura,
        options: { darkModeSelector: false },
      },
    }),
  ],
};
