import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-user-input',  
  templateUrl: './user-input.component.html',
  styleUrl: './user-input.component.css'
})
export class UserInputComponent {

  inputForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.inputForm = this.fb.group({
      question: this.fb.control('', Validators.required),
      answer: this.fb.control('', Validators.required),
      keyword: this.fb.control('', Validators.required),
    })
  }

  submit() {
    console.log(this.inputForm.value);
    
  }

}
