import { Component, EventEmitter, Output } from '@angular/core';
import { FileService } from '../file.service';
import { interval, switchMap, takeWhile } from 'rxjs';
import { ShowResponse } from '../dto/show-response.dto';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadComponent {
  @Output() fileResponseEvent = new EventEmitter<ShowResponse>();
  selectedFile: File | null = null;
  uploadStatus: string = 'Idle';
  processing: boolean = false;
  uuid: string = '';

  constructor(private fileService: FileService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onUpload() {
    if (this.selectedFile) {
      this.uploadStatus = 'Uploading...';
      this.processing = true;

      this.fileService.uploadFile(this.selectedFile).subscribe({
        next: (uuid) => {
          this.uuid = uuid;
          this.uploadStatus = 'File uploaded successfully. Processing...';
          this.pollStatus();
        },
        error: (err) => {
          this.uploadStatus = `Upload failed: ${err.message}`;
          this.processing = false;
        }
      });
    }
  }

  pollStatus() {
    interval(250)
      .pipe(
        switchMap(() => this.fileService.getStatus(this.uuid)),
        takeWhile(resp => resp.status !== 'complete' && resp.status !== 'failed', true)
      )
      .subscribe({
        next: (resp) => {
          this.uploadStatus = `Processing status: ${resp.status} ${resp.percent}%`;
          if (resp.status === 'complete') {
            this.downloadFile();
            this.getResponse()
            this.processing = false;
          } else if (resp.status === 'failed') {
            this.uploadStatus = 'Processing failed.';
            this.processing = false;
          }
        },
        error: (err) => {
          this.uploadStatus = `Status check failed: ${err.message}`;
          this.processing = false;
        }
      });
  }

  getResponse() {
    this.fileService.getResponse(this.uuid).subscribe({
      next: (resp: ShowResponse) => {
        this.fileResponseEvent.emit(resp);
      },
      error: (err) => {
        //;
      }
    });
  }

  downloadFile() {
    this.fileService.downloadFile(this.uuid).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.uuid}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        this.uploadStatus = 'Download complete.';
      },
      error: (err) => {
        this.uploadStatus = `Download failed: ${err.message}`;
      }
    });
  }
}
