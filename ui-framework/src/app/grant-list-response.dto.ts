export class GrantListResponse {
  id: number;
  title: string;
  category: string;
  startDate: string;
  endDate: string;
  fundsAvailable: number;
  constructor(
    id: number,
    title: string,
    category: string,
    startDate: string,
    endDate: string,
    fundsAvailable: number
  ) {
    this.id = id;
    this.title = title;
    this.category = category;
    this.startDate = startDate;
    this.endDate = endDate;
    this.fundsAvailable = fundsAvailable;
  }
}
