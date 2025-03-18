import { Component } from '@angular/core';
import { GrantListResponse } from '../grant-list-response.dto';
import { Router } from '@angular/router';

@Component({
  selector: 'app-grant-list',
  standalone: true,
  imports: [],
  templateUrl: './grant-list.component.html',
  styleUrl: './grant-list.component.css',
})
export class GrantListComponent {
  headers: string[] = [
    'S No.',
    'Title',
    'Category',
    'Start Date',
    'End Date',
    'Funds Available',
  ];

  grants: GrantListResponse[] = [];

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      this.grants = navigation.extras.state['grants'];
    }
  }

  ngOnInit() {
    if (!this.grants || this.grants.length === 0) {
      this.grants = [
        {
          id: 1,
          title: 'Grant 1',
          category: 'Category 1',
          startDate: '2021-01-01',
          endDate: '2021-12-31',
          fundsAvailable: 1000,
        },
        {
          id: 2,
          title: 'Grant 2',
          category: 'Category 2',
          startDate: '2021-01-01',
          endDate: '2021-12-31',
          fundsAvailable: 2000,
        },
      ];
    }
  }
}
