import pandas as pd
from countryinfo import CountryInfo

def get_gamer_pct(region):
    r = str(region).lower()
    if 'northern america' in r: return 0.45
    if 'europe' in r: return 0.40
    if 'oceania' in r: return 0.40
    if 'asia' in r: return 0.35
    if 'america' in r: return 0.30
    if 'africa' in r: return 0.15
    return 0.25

def get_population(country_name):
    aliases = {
        "USA": "United States",
        "UK": "United Kingdom",
        "UAE": "United Arab Emirates",
        "Russian Federation": "Russia",
        "South Korea": "South Korea",
        "Republic of Korea": "South Korea"
    }
    name = aliases.get(country_name, country_name)
    try:
        pop = CountryInfo(name).population()
        return pop if pop else 0
    except Exception:
        return 0

def update_volumes():
    df = pd.read_excel("Region_analysis.xlsx")
    volumes = []
    
    for _, row in df.iterrows():
        pop = get_population(str(row['Country']))
        pct = get_gamer_pct(row['Region'])
        
        val = row.get('Android Share', 0)
        try:
            andr = 0.0 if pd.isna(val) or val == "" else float(str(val).replace('%', '').strip()) / 100.0
        except ValueError:
            andr = 0.0
            
        volumes.append(round(pop * pct * andr))
        
    df['Potential Player Volume'] = volumes
    df.to_excel("Region_analysis.xlsx", index=False)
    print("Done")

if __name__ == "__main__":
    update_volumes()