import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { GrantResponse } from '../grant-response.dto';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grant-details',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './grant-details.component.html',
  styleUrl: './grant-details.component.css',
})
export class GrantDetailsComponent {
  grant: GrantResponse;
  grantForm: FormGroup;

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    this.grant = navigation?.extras.state?.['grant'];
  }

  ngOnInit() {
    this.grantForm = new FormGroup({
      fullName: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      organizationName: new FormControl(''),
      projectName: new FormControl('', [Validators.required]),
      purpose: new FormControl('', [Validators.required]),
      fundingAmount: new FormControl('', [Validators.required]),
      expectedOutcomes: new FormControl(''),
      targetAudience: new FormControl(''),
    });
  }

  onSubmit() {
    if (this.grantForm.valid) {
      const applicationData = {
        ...this.grantForm.value,
        grantId: this.grant.id,
      };

      console.log('Submitting application:', applicationData);
      // Call API or AI model to generate report here
    }
  }
}
