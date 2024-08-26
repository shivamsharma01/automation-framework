import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-display-table',
  templateUrl: './display-table.component.html',
  styleUrl: './display-table.component.css'
})
export class DisplayTableComponent {
  @Input() header: string[] = ['Question', 'Expected Response', 'Actual Response', 'Keyword', 'Fuzz Score', 'Spacy Cosine Score', 'Sentence Transformer Cosine Score'];
  @Input() response: string[][] = [['Q.2', 'EA.2 sdjsa ad sajaagds aka djada iuadh aka akj hdak daakjd hakdjhasdka', 'AA.2 aka kjaka hdkja akaa iuayiue aka iugdha 1231u 24 t87181 g31 13 187 313 1731', 'aka', '92', '91', '85']];

  hasKeyWordColumn: boolean;
  keywordColumnIdx: number;
  ngOnInit() {
    const idx = this.header && this.header.findIndex(col => 'keyword' === col.toLowerCase()) || -1;
    if (idx > -1) {
      this.hasKeyWordColumn = true;
      this.keywordColumnIdx = idx;
    } else {
      this.hasKeyWordColumn = false;
      this.keywordColumnIdx = -1;
    }
  }

}
