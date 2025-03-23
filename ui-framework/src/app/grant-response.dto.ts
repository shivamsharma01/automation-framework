export class GrantResponse {
  id: number;
  org: string;
  title: string;
  category: string;
  description: string;
  eligibility: string[];
  funds: number;
  constructor(
    id: number,
    org: string,
    title: string,
    category: string,
    description: string,
    eligibility: string[],
    funds: number
  ) {
    this.id = id;
    this.org = org;
    this.title = title;
    this.category = category;
    this.description = description;
    this.eligibility = eligibility;
    this.funds = funds;
  }
}
