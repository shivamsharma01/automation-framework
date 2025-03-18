import { Component, OnInit } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { FormDataService } from '../form-data.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { GrantService } from '../grant.service';
import { GrantListResponse } from '../grant-list-response.dto';

@Component({
  selector: 'app-grant-request',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './grant-request.component.html',
  styleUrl: './grant-request.component.css',
})
export class GrantRequestComponent implements OnInit {
  grantForm: FormGroup;
  eligibilityTypes: string[];
  categories: string[];
  states: string[];

  constructor(
    private formDataService: FormDataService,
    private grantService: GrantService,
    private router: Router
  ) {}

  ngOnInit() {
    this.grantForm = new FormGroup({
      organizationName: new FormControl('', [Validators.required]),
      category: new FormControl('All', [Validators.required]),
      eligibility: new FormControl('All', [Validators.required]),
      location: new FormControl('All', [Validators.required]),
      fundingAmount: new FormControl(null, [Validators.required]),
    });
    this.eligibilityTypes = this.formDataService.getEligibilityOptions();
    this.categories = this.formDataService.getCategoryOptions();
    this.states = this.formDataService.getStates();
  }

  onSubmit() {
    console.log(this.grantForm.value);
    console.log(this.grantForm.valid);

    const requestData = { category: 'Education', minFunds: 1000 };

    this.grantService.fetchGrants(requestData).subscribe({
      next: (grants: GrantListResponse[]) =>
        this.router.navigate(['/homepage/grant-list'], { state: { grants } }),
      error: (error: any) => {
        this.router.navigate(['/homepage/grant-list'], { state: {} }),
          console.error('Error fetching grants', error);
      },
    });
  }
}
