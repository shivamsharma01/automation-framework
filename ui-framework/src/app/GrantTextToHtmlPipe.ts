import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'grantTextToHtml',
  standalone: true,
})
export class GrantTextToHtmlPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return '';
    let i = 0;
    let len = value.length;
    let out = '';
    let isSectionOpen: boolean = false;
    let isBoldOpen: boolean = false;
    while (i < len) {
      if (value[i] === '#') {
        if (i + 1 < len && value[i + 1] === '#') {
          out += '<h3>';
          isSectionOpen = true;
          i++;
        } else {
          out += value[i];
        }
      } else if (value[i] === '\n') {
        if (isSectionOpen) out += '</h3>';
        else out += '<br>';
        isSectionOpen = false;
      } else if (value[i] === '*') {
        if (i + 1 < len && value[i + 1] === '*') {
          if (isBoldOpen) out += '</b>';
          else out += '<b>';
          isBoldOpen = !isBoldOpen;
          i++;
        } else {
          out += value[i];
        }
      } else {
        out += value[i];
      }
      i++;
    }
    return out;
  }
}
