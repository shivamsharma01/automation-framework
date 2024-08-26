import { Component } from '@angular/core';
import { ShowResponse } from './dto/show-response.dto';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'ui-framework';
  choice: string;
  resp: ShowResponse | null;
  
  fileResponse(resp: ShowResponse) {
    this.resp = resp;
  }
  
  choiceEvent(event: string) {
    this.choice = event;
    this.resp = null;
  }

  cancel() {
    this.choice = '';
    this.resp = null;
  }
}
