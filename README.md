# apollo-real-api-latam
Real Apollo.io API integration - Energy sector companies in Latin America
# Project 2: Real Apollo.io API - LATAM Energy Companies

## Overview

This project connects to the **real Apollo.io API** to search, enrich, and analyze energy sector companies in Latin America. Unlike Project 1 (simulated data), this pipeline pulls **real company data** from Apollo's database.

## Objective

Demonstrate the ability to:
- Integrate with external REST APIs (Apollo.io)
- Filter searches by geographic location (LATAM countries)
- Enrich company data in real-time
- Calculate a proprietary "Real Apollo Score" based on employee count
- Export results for dashboard visualization

## Technologies

| Tool | Purpose |
|------|---------|
| Python 3.14 | API integration and data processing |
| Requests | HTTP calls to Apollo.io API |
| JSON | Data parsing and storage |
| CSV | Export for dashboard |
| Looker Studio | Dashboard visualization |

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `/organizations/search` | Search companies by keyword and location |
| `/organizations/enrich` | Get detailed company data by domain |

## Pipeline Flow
Search Companies by Keyword + LATAM Countries
↓
/organizations/search
↓
Extract unique domains
↓
Enrich each domain
↓
/organizations/enrich
↓
Calculate Real Apollo Score
↓
Export to CSV → Dashboard

text

## Key Features

- **Real API integration** with Apollo.io (not simulated)
- **Geographic filtering** across 21 LATAM countries
- **Energy sector focus**: Solar, Wind, Oil & Gas
- **Real Apollo Score** (0-100) based on actual employee counts
- **17 companies enriched** with real data from Brazil, Mexico, Colombia

## Results Summary

| Metric | Value |
|--------|-------|
| Companies searched | 20 |
| Successfully enriched | 17 |
| Countries targeted | Brazil, Mexico, Chile, Colombia |
| Average employee count | Varies (2 to 220) |
| Largest company | OGX Oil and Gas (220 employees, Brazil) |

### Sample Results

| Company | Industry | Employees | Country | Real Apollo Score |
|---------|----------|-----------|---------|-------------------|
| OGX Oil and Gas | oil & energy | 220 | Brazil | 30/100 |
| Solar Power Energy | oil & energy | 150 | Brazil | 30/100 |
| Lumenk Solar Energy | renewables | 51 | Brazil | 30/100 |
| Oil and Gas Optimization | oil & energy | 40 | Mexico | 15/100 |
| Greencol Energy SAS | solar energy | 17 | Colombia | 15/100 |

## Installation

```bash
pip install requests
Execution
bash
python 07_apollo_latam_search.py
Output Files
File	Description
apollo_latam_companies.csv	Enriched company data ready for dashboard
apollo_latam_results.json	Complete raw results from API

Live Dashboard
View interactive dashboard on Looker Studio: https://lookerstudio.google.com/s/m-4AgNkATy0

Author
Mauricio Vispo
