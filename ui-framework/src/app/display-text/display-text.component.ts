import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-display-text',
  templateUrl: './display-text.component.html',
  styleUrl: './display-text.component.css'
})
export class DisplayTextComponent {
  @Input() text: string = '';
  @Input() keyword: string = '';

  ngOnInit() {
    if (!this.text || !this.keyword) return;
    this.text = this.findAndHighlightKeywordInString();
  }

  findAndHighlightKeywordInString(): string {
    let textInpLower = this.text.toLowerCase();
    const keyword = this.keyword.toLowerCase();
    let startIdx = -1, mainStrStartIdx = 0;
    let output = '';
    while (textInpLower && (startIdx = textInpLower.indexOf(keyword)) != -1) {
      if (startIdx > 0) {
        output += this.text.substring(mainStrStartIdx, mainStrStartIdx+startIdx);
      }
      mainStrStartIdx += startIdx;
      output += '<span class="highlight">' + this.text.substring(mainStrStartIdx, mainStrStartIdx + keyword.length) + '</span>';
      mainStrStartIdx += keyword.length;
      textInpLower = textInpLower.substring(startIdx + keyword.length);
    }
    if (mainStrStartIdx != this.text.length) {
      output += this.text.substring(mainStrStartIdx, this.text.length);
    }
    return output;
  }
}
