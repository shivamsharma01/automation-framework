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
import { GrantService } from '../grant.service';
import { DisplayGrantFormComponent } from '../display-grant-form/display-grant-form.component';

@Component({
  selector: 'app-grant-details',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, DisplayGrantFormComponent],
  templateUrl: './grant-details.component.html',
  styleUrl: './grant-details.component.css',
})
export class GrantDetailsComponent {
  grant: GrantResponse;
  grantForm: FormGroup;
  isError: boolean;
  submitted: boolean;
  errorStr: string;
  response: string;
  isLoading: boolean;

  constructor(private router: Router, private grantService: GrantService) {
    const navigation = this.router.getCurrentNavigation();
    this.grant = navigation?.extras.state?.['grant'];
  }

  ngOnInit() {
    this.isError = false;

    this.grantForm = new FormGroup({
      fullName: new FormControl('Shivam Sharma', [Validators.required]),
      email: new FormControl('shivam@gmail.com', [
        Validators.required,
        Validators.email,
      ]),
      organizationName: new FormControl('Okta', [Validators.required]),
      projectName: new FormControl(
        'Okta for Good’s Nonprofit Technology Initiative',
        [Validators.required]
      ),
      purpose: new FormControl(
        'The initiative aims to support nonprofits by providing secure identity and access management solutions, facilitating digital transformation, and enhancing cybersecurity.',
        [Validators.required]
      ),
      fundingAmount: new FormControl(
        '$10,000,000 (philanthropic funding) + $10,000,000 (in-kind donations)',
        [Validators.required]
      ),
      expectedOutcomes: new FormControl(
        'Nonprofits will gain access to secure authentication and authorization solutions, improved data security, and seamless cloud migration support.'
      ),
      targetAudience: new FormControl(
        'Nonprofit organizations seeking technology improvements, cybersecurity, and digital transformation.'
      ),
    });
  }

  onSubmit() {
    if (this.grantForm.valid) {
      const applicationData = {
        ...this.grantForm.value,
      };
      this.grantForm.disable();
      this.isLoading = true;
      this.grantService
        .fetchGrantApplicationForm(this.grant.id, applicationData)
        .subscribe((resp) => {
          this.isLoading = false;
          this.submitted = true;
          this.response = resp.data;
          this.isError = resp.status !== 200;
        });
    }
  }
}
