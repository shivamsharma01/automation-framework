import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../api.service';
import { ShowResponse } from '../dto/show-response.dto';

@Component({
  selector: 'app-user-input',  
  templateUrl: './user-input.component.html',
  styleUrl: './user-input.component.css'
})
export class UserInputComponent {
  @Output() fileResponseEvent = new EventEmitter<ShowResponse>();

  inputForm: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService) {}

  ngOnInit() {
    this.inputForm = this.fb.group({
      question: this.fb.control('', Validators.required),
      answer: this.fb.control('', Validators.required),
      keyword: this.fb.control('', Validators.required),
    })
  }

  submit() {
    if (this.inputForm.valid) {
      const input = this.inputForm.value;
      const question = input.question;
      const answer = input.answer;
      const keyword = input.keyword;
      this.apiService.getUserInputResponse(question, answer, keyword).subscribe(resp => {
        this.fileResponseEvent.emit(resp);
      })
    }
  }

}
