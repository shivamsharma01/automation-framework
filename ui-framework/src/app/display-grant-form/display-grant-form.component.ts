import { Component, Input } from '@angular/core';
import { GrantTextToHtmlPipe } from '../GrantTextToHtmlPipe';

@Component({
  selector: 'app-display-grant-form',
  standalone: true,
  imports: [GrantTextToHtmlPipe],
  templateUrl: './display-grant-form.component.html',
  styleUrl: './display-grant-form.component.css',
})
export class DisplayGrantFormComponent {
  @Input() response: string;
}
