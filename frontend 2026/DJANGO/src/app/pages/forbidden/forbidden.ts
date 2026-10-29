import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  imports: [RouterLink],
  selector: 'app-forbidden',
  template: `
    <main class="forbidden-page">
      <span class="forbidden-icon"><i class="pi pi-lock"></i></span>
      <span class="eyebrow">ACCESO RESTRINGIDO</span>
      <h1>No tienes permiso para este módulo</h1>
      <p>Solicita al administrador de OdontoNova que revise los roles asignados a tu usuario.</p>
      <a routerLink="/dashboard" class="primary-link"><i class="pi pi-arrow-left"></i> Volver al resumen</a>
    </main>
  `,
  styles: `
    .forbidden-page { display:grid; min-height:65vh; justify-items:center; align-content:center; text-align:center; }
    .forbidden-icon { display:grid; width:58px; height:58px; margin-bottom:22px; place-items:center; border-radius:17px; color:#a56d24; background:#fff4dc; font-size:21px; }
    h1 { margin:12px 0 7px; color:#1d3943; font-size:27px; }
    p { max-width:440px; margin:0 0 22px; color:#82939b; font-size:13px; line-height:1.6; }
  `,
})
export class Forbidden {}
