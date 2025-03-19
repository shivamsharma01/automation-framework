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
    'Grant ID',
    'Organization Name',
    'Title',
    'Category',
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
          org: 'Org 1',
          title: 'Grant 1',
          category: 'Category 1',
          funds: 1000,
        },
        {
          id: 2,
          org: 'Org 2',
          title: 'Grant 2',
          category: 'Category 2',
          funds: 2000,
        },
      ];
    }
  }
}
