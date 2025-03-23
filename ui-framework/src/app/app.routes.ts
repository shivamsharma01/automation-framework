import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { GrantRequestComponent } from './grant-request/grant-request.component';
import { GrantListComponent } from './grant-list/grant-list.component';
import { GrantDetailsComponent } from './grant-details/grant-details.component';
import { GrantApplicationComponent } from './grant-application/grant-application.component';
import { GrantResponse } from './grant-response.dto';

export const routes: Routes = [
  {
    path: 'homepage',
    component: HomeComponent,
    children: [
      {
        path: 'grant-request',
        component: GrantRequestComponent,
      },
      {
        path: 'grant-list',
        component: GrantListComponent,
      },
      {
        path: 'grant-details/:id',
        component: GrantDetailsComponent,
        data: GrantResponse,
      },
      {
        path: 'grant-application',
        component: GrantApplicationComponent,
      },
      {
        path: '',
        redirectTo: 'grant-request',
        pathMatch: 'full',
      },
    ],
  },
  {
    path: '',
    redirectTo: '/homepage',
    pathMatch: 'full',
  },
];

// @NgModule({
//   imports: [RouterModule.forRoot(routes)],
//   exports: [RouterModule],
// })
// export class AppRoutingModule {}
