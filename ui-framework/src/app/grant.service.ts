import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GrantResponse } from './grant-response.dto';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GrantService {
  private apiUrl = 'http://localhost/api/grants';

  constructor(private http: HttpClient) {}

  fetchGrants(data: any): Observable<GrantResponse[]> {
    return this.http.post<GrantResponse[]>(this.apiUrl, data);
  }
}
