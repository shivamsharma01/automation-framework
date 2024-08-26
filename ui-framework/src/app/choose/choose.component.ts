import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-choose',
  standalone: true,
  imports: [],
  templateUrl: './choose.component.html',
  styleUrl: './choose.component.css'
})
export class ChooseComponent {
  @Output() choiceEvent: EventEmitter<string> = new EventEmitter();

  emit(choice: string) {
    this.choiceEvent.emit(choice);
  }
}
