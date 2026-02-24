import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';

console.log('main.ts loading with Zone.js...');

bootstrapApplication(AppComponent).then(() => {
  console.log('Angular application bootstrapped successfully with Zone.js!');
}).catch(err => {
  console.error('Bootstrap error:', err);
});
