# 07_apollo_latam_search.py
import requests
import json
import time
import csv
from datetime import datetime

# ============================================
# CONFIGURATION - API KEY
# ============================================

API_KEY = "DByOjV1e2izo4j7CXaFOkg"

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

BASE_URL = "https://api.apollo.io/api/v1"

# ============================================
# LATAM COUNTRIES
# ============================================

LATAM_COUNTRIES = [
    "Argentina",
    "Bolivia", 
    "Brazil",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Cuba",
    "Dominican Republic",
    "Ecuador",
    "El Salvador",
    "Guatemala",
    "Haiti",
    "Honduras",
    "Mexico",
    "Nicaragua",
    "Panama",
    "Paraguay",
    "Peru",
    "Puerto Rico",
    "Uruguay",
    "Venezuela"
]

# ============================================
# FUNCTION: Search organizations by keyword and location
# ============================================

def search_organizations_by_keyword_and_location(keyword, locations, per_page=10):
    """
    Search for organizations using /organizations/search endpoint.
    Filters by keyword and location (country/city/state).
    """
    print(f"\n🔎 Searching for '{keyword}' in {len(locations)} countries...")
    
    url = f"{BASE_URL}/organizations/search"
    payload = {
        "q_organization_name": keyword,
        "organization_locations": locations,  # ← FILTRO POR UBICACIÓN
        "per_page": per_page,
        "page": 1
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            organizations = data.get("organizations", [])
            
            results = []
            for org in organizations:
                domain = org.get("domain", "")
                if not domain:
                    website = org.get("website_url", "")
                    if website:
                        domain = website.replace("http://", "").replace("https://", "").replace("www.", "")
                
                results.append({
                    "name": org.get("name", "N/A"),
                    "domain": domain if domain else "N/A",
                    "industry": org.get("industry", "N/A"),
                    "employees": org.get("estimated_num_employees", "N/A"),
                    "country": org.get("country", "N/A"),
                    "city": org.get("city", "N/A"),
                    "linkedin_url": org.get("linkedin_url", "N/A")
                })
            return results
        else:
            print(f"  Error: HTTP {response.status_code}")
            if response.status_code == 403:
                print(f"  This endpoint may require a paid plan for location filtering")
            return []
    except Exception as e:
        print(f"  Error: {e}")
        return []

# ============================================
# FUNCTION: Enrich single company by domain
# ============================================

def enrich_company_by_domain(domain):
    """
    Enrich a single company using /organizations/enrich endpoint.
    """
    url = f"{BASE_URL}/organizations/enrich"
    payload = {"domain": domain}
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            org = data.get("organization", {})
            
            employees = org.get("estimated_num_employees", 0)
            
            # Calculate Real Apollo Score based on employees
            if isinstance(employees, (int, float)) and employees > 0:
                if employees >= 10000:
                    size_score = 100
                elif employees >= 5000:
                    size_score = 85
                elif employees >= 1000:
                    size_score = 70
                elif employees >= 250:
                    size_score = 50
                elif employees >= 50:
                    size_score = 30
                else:
                    size_score = 15
            else:
                size_score = 25
            
            return {
                "name": org.get("name", "N/A"),
                "domain": domain,
                "industry": org.get("industry", "N/A"),
                "employees": employees,
                "country": org.get("country", "N/A"),
                "city": org.get("city", "N/A"),
                "linkedin_url": org.get("linkedin_url", "N/A"),
                "real_apollo_score": size_score,
                "success": True
            }
        else:
            return {
                "domain": domain,
                "success": False,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "domain": domain,
            "success": False,
            "error": str(e)
        }

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 PROJECT 2: LATAM ENERGY COMPANIES")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Energy keywords to search
    energy_keywords = [
        "solar energy",
        "wind energy",
        "oil and gas"
    ]
    
    # Try with a smaller subset of LATAM countries first
    test_countries = ["Brazil", "Mexico", "Chile", "Colombia"]
    
    all_search_results = []
    
    for keyword in energy_keywords:
        results = search_organizations_by_keyword_and_location(keyword, test_countries, per_page=8)
        all_search_results.extend(results)
        print(f"\n  Found {len(results)} companies for '{keyword}' in LATAM")
        for company in results[:3]:
            print(f"    - {company['name']} | {company['country']}")
    
    # Collect unique domains
    unique_domains = list(set([r['domain'] for r in all_search_results if r['domain'] and r['domain'] != "N/A"]))
    print(f"\n📋 Unique domains to enrich: {len(unique_domains)}")
    
    # Enrich companies
    enriched_companies = []
    for domain in unique_domains[:20]:
        result = enrich_company_by_domain(domain)
        if result.get("success"):
            enriched_companies.append(result)
            print(f"  ✅ {result['name']}: {result['employees']} employees | {result['country']} | Score: {result['real_apollo_score']}")
        else:
            print(f"  ❌ {domain}: {result.get('error', 'Unknown error')}")
        time.sleep(0.3)
    
    # Save results
    print("\n" + "=" * 70)
    print("💾 Saving results...")
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "region": "Latin America",
        "countries_searched": test_countries,
        "keywords_searched": energy_keywords,
        "enriched_companies": enriched_companies
    }
    
    with open("apollo_latam_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # Create CSV for dashboard
    if enriched_companies:
        with open("apollo_latam_companies.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "industry", "employees", "country", "city", "real_apollo_score"])
            writer.writeheader()
            for company in enriched_companies:
                writer.writerow({
                    "name": company["name"],
                    "industry": company["industry"],
                    "employees": company["employees"],
                    "country": company["country"],
                    "city": company["city"],
                    "real_apollo_score": company["real_apollo_score"]
                })
        print("✅ CSV created: 'apollo_latam_companies.csv'")
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print(f"  Total companies found: {len(all_search_results)}")
    print(f"  Successfully enriched: {len(enriched_companies)}")
    print(f"  Countries targeted: {', '.join(test_countries)}")
    
    print("\n🏁 LATAM search completed.")