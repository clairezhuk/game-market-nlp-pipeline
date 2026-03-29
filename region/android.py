import pandas as pd
import unicodedata
import re

def normalize_name(name):
    if not isinstance(name, str):
        return ""
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[^a-z0-9]', '', name.lower())
    return name

def update_android_share():
    try:
        df_excel = pd.read_excel("Region_analysis.xlsx")
        df_csv = pd.read_csv("os_combined-ww-monthly-202512-202602-map.csv")
        
        aliases = {
            "usa": "unitedstates",
            "us": "unitedstates",
            "unitedstatesofamerica": "unitedstates",
            "uk": "unitedkingdom",
            "uae": "unitedarabemirates",
            "russia": "russianfederation",
            "southkorea": "koreasouth"
        }
        
        df_excel['norm_country'] = df_excel['Country'].apply(normalize_name)
        df_excel['norm_country'] = df_excel['norm_country'].replace(aliases)
        
        df_csv['norm_country'] = df_csv['Continent'].apply(normalize_name)
        df_csv['norm_country'] = df_csv['norm_country'].replace(aliases)
        
        android_map = dict(zip(df_csv['norm_country'], df_csv['Android']))
        
        mapped_values = df_excel['norm_country'].map(android_map)
        matches = mapped_values.notna().sum()
        
        print(f"Matched {matches} countries out of {len(df_excel)}")
        
        if matches == 0:
            print("Excel sample:", df_excel['norm_country'].head(5).tolist())
            print("CSV sample:", df_csv['norm_country'].head(5).tolist())
            
        df_excel["Android Share"] = mapped_values.fillna(df_excel["Android Share"])
        df_excel = df_excel.drop(columns=['norm_country'])
        
        df_excel.to_excel("Region_analysis.xlsx", index=False)
        print("Saved to Region_analysis.xlsx")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_android_share()