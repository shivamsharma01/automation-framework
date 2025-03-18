import { Component } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, HeaderComponent, RouterOutlet],
})
export class AppComponent {
  title = 'ui-framework';
}
