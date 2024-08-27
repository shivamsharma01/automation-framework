import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { ShowResponse } from './dto/show-response.dto';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  uploadFile(file: File): Observable<string> {
    const formData: FormData = new FormData();
    formData.append('file', file);

    return this.http
      .put<{ uuid: string }>(`${this.apiUrl}/uploadcsv`, formData)
      .pipe(map((response) => response.uuid.replaceAll('"', '')));
  }

  getStatus(uuid: string): Observable<{ status: string; percent: number }> {
    return this.http.get<{ status: string; percent: number }>(
      `${this.apiUrl}/status/${uuid}`
    );
  }

  downloadFile(uuid: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/download/${uuid}`, {
      responseType: 'blob',
    });
  }

  getResponse(uuid: string): Observable<ShowResponse> {
    return this.http.get<ShowResponse>(`${this.apiUrl}/show/${uuid}`);
  }

  getUserInputResponse(
    question: string,
    answer: string,
    keyword: string
  ): Observable<ShowResponse> {
    return this.http.post<ShowResponse>(`${this.apiUrl}/user/input`, {
      question,
      expected: answer,
      keyword,
    });
  }
}
