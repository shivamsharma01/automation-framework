import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class FormDataService {
  constructor() {}

  getEligibilityOptions() {
    return [
      'Legally recognized non-profit organizations',
      'Non-governmental organizations (NGOs)',
      'Think tanks and research institutions',
      'Academic institutions (universities, colleges, and schools) that comply with regional legal requirements',
      'Charitable foundations and trusts',
      'Community-based organizations (CBOs)',
      'Social enterprises and impact-driven businesses (if eligible under grant terms)',
      'Faith-based organizations (FBOs) engaged in social services',
      'Professional associations and advocacy groups',
      'Public benefit corporations',
      'Cooperatives and mutual aid societies',
      'Health and medical research institutions',
      'Environmental and conservation organizations',
      'Humanitarian aid and disaster relief organizations',
      'Arts, culture, and heritage organizations',
      'Youth and sports development organizations',
      'Indigenous and tribal organizations',
      'Public-private partnerships with a nonprofit or social mission',
      'Government-affiliated entities with non-profit missions (e.g., public hospitals, libraries)',
      'Other organizations meeting the eligibility criteria as specified by the grant',
      'All (if the grant is universally open to any entity meeting specific guidelines)',
    ];
  }

  getCategoryOptions() {
    return [
      'Nonprofit Capacity Building Grants',
      'Digital Transformation & Innovation Grants',
      'Fundraising Technology & CRM Grants',
      'Financial Management & Sustainability Grants',
      'Education & Scholarship Management Grants',
      'Social Impact & Corporate Philanthropy Grants',
      'Grantmaking Infrastructure Grants',
      'Diversity, Equity, and Inclusion (DEI) Grants',
      'Volunteer Management Grants',
      'Healthcare & Medical Research Grants',
      'Arts & Culture Grants',
      'Humanities Grants',
      'Disaster Relief & Humanitarian Aid Grants',
      'Faith-Based Organization Grants',
      'Mental Health & Well-Being Grants',
      'Community Development Grants',
      'Animal Welfare & Environmental Sustainability Grants',
      'STEM & Technology Education Grants',
      'Advocacy & Policy Change Grants',
      'International Development & Global Outreach Grants',
      'Youth & Early Childhood Development Grants',
      'All',
    ];
  }

}
