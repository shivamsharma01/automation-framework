export class GrantListResponse {
  id: number;
  org: string;
  title: string;
  category: string;
  funds: number;
  constructor(
    id: number,
    org: string,
    title: string,
    category: string,
    funds: number
  ) {
    this.id = id;
    this.org = org;
    this.title = title;
    this.category = category;
    this.funds = funds;
  }
}
