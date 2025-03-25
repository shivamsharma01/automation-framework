import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GrantResponse } from './grant-response.dto';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GrantService {
  private apiUrl = 'http://localhost/api';

  constructor(private http: HttpClient) {}

  fetchGrants(data: any): Observable<GrantResponse[]> {
    return this.http.post<GrantResponse[]>(this.apiUrl + '/grants', data);
  }

  fetchGrantApplicationForm(
    grantId: number,
    data: any
  ): Observable<{ data: string; status: number }> {
    return this.http.post<any>(
      this.apiUrl + `/generate/grant/${grantId}/form`,
      data
    );
  }
}
