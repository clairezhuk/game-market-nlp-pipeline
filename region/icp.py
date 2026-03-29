import pandas as pd

market_data = {
    "United States": {"cpi": 1.50, "ecpm": 18.00},
    "United Kingdom": {"cpi": 1.20, "ecpm": 12.00},
    "Canada": {"cpi": 1.10, "ecpm": 11.00},
    "Australia": {"cpi": 1.30, "ecpm": 13.00},
    "Germany": {"cpi": 0.90, "ecpm": 9.00},
    "France": {"cpi": 0.80, "ecpm": 8.00},
    "Japan": {"cpi": 1.40, "ecpm": 14.00},
    "South Korea": {"cpi": 1.20, "ecpm": 10.00},
    "Brazil": {"cpi": 0.15, "ecpm": 1.50},
    "India": {"cpi": 0.05, "ecpm": 0.50},
    "Indonesia": {"cpi": 0.10, "ecpm": 1.00},
    "Mexico": {"cpi": 0.20, "ecpm": 2.00},
    "Tier 1": {"cpi": 1.20, "ecpm": 14.00},
    "Tier 2": {"cpi": 0.70, "ecpm": 7.00},
    "Tier 3": {"cpi": 0.15, "ecpm": 1.20}
}

def get_tier(country, region):
    tier_1 = ["United States", "United Kingdom", "Canada", "Australia", "New Zealand", "Switzerland", "Norway"]
    tier_2 = ["Germany", "France", "Italy", "Spain", "Japan", "South Korea", "Sweden", "Netherlands"]
    
    if country in tier_1: return "Tier 1"
    if country in tier_2: return "Tier 2"
    if "europe" in str(region).lower(): return "Tier 2"
    return "Tier 3"

def update_financials():
    df = pd.read_excel("Region_analysis.xlsx")
    
    cpi_list = []
    ecpm_list = []
    
    for _, row in df.iterrows():
        country = str(row['Country'])
        region = str(row['Region'])
        
        if country in market_data:
            cpi = market_data[country]["cpi"]
            ecpm = market_data[country]["ecpm"]
        else:
            tier = get_tier(country, region)
            cpi = market_data[tier]["cpi"]
            ecpm = market_data[tier]["ecpm"]
            
        cpi_list.append(cpi)
        ecpm_list.append(ecpm)
        
    df['Estimated CPI'] = cpi_list
    df['Estimated eCPM'] = ecpm_list
    df.to_excel("Region_analysis.xlsx", index=False)
    print("Done")

if __name__ == "__main__":
    update_financials()