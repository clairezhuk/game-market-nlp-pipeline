import pandas as pd
import requests

def get_data():
    url = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def create_df(data):
    cols = [
        "Country", "Region", "Languages", 
        "Android Share", "Potential Player Volume", 
        "Estimated CPI", "Estimated eCPM"
    ]
    
    if not data:
        return pd.DataFrame(columns=cols)
        
    rows = []
    for item in data:
        country = item.get("name", {}).get("common", "Unknown")
        region = item.get("region", "Unknown")
        subregion = item.get("subregion", "Unknown")
        
        langs = item.get("languages", {})
        languages = ", ".join(langs.values()) if isinstance(langs, dict) else "Unknown"
        
        rows.append({
            "Country": country,
            "Region": f"{region} - {subregion}",
            "Languages": languages,
            "Android Share": "",
            "Potential Player Volume": "",
            "Estimated CPI": "",
            "Estimated eCPM": ""
        })
        
    return pd.DataFrame(rows, columns=cols)

def main():
    data = get_data()
    df = create_df(data)
    df.to_excel("localization_analysis/Region_analysis.xlsx", index=False)
    print("Done")

if __name__ == "__main__":
    main()