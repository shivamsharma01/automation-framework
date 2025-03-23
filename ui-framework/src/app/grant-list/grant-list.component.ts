import { Component } from '@angular/core';
import { GrantResponse } from '../grant-response.dto';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-grant-list',
  standalone: true,
  imports: [RouterLink],
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

  grants: GrantResponse[] = [];

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      this.grants = navigation.extras.state['grants'];
    }
  }

  ngOnInit() {
  }
}
