import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GrantListResponse } from './grant-list-response.dto';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GrantService {
  private apiUrl = 'http://localhost/api/grants';

  constructor(private http: HttpClient) {}

  fetchGrants(data: any): Observable<GrantListResponse[]> {
    return this.http.post<GrantListResponse[]>(this.apiUrl, data);
  }
}
