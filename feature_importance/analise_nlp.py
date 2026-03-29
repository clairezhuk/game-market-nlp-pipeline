import os
import json
import pandas as pd
from transformers import pipeline


def analyze_reviews_dynamic():
    extractor = pipeline("text2text-generation", model="google/flan-t5-base")
    df = pd.read_csv("competitors_usa_v2.csv")
    analyzed_data = []
    
    for _, row in df.iterrows():
        app_id = row['App_ID']
        pros_text = ""
        cons_text = ""
        
        rev_path = f"reviews_v2/{app_id}.json"
        if os.path.exists(rev_path):
            with open(rev_path, "r", encoding="utf-8") as f:
                reviews = json.load(f)
                
            good_revs = [r['text'] for r in reviews.get('star_5', [])[:5] + reviews.get('star_4', [])[:5]]
            bad_revs = [r['text'] for r in reviews.get('star_1', [])[:5] + reviews.get('star_2', [])[:5]]
            
            if good_revs:
                good_combined = " ".join(good_revs)[:800]
                prompt = f"Extract key positive features from these game reviews as a short comma-separated list: {good_combined}"
                res = extractor(prompt, max_length=50, do_sample=False)
                pros_text = res[0]['generated_text']
                
            if bad_revs:
                bad_combined = " ".join(bad_revs)[:800]
                prompt = f"Extract key complaints and negative issues from these game reviews as a short comma-separated list: {bad_combined}"
                res = extractor(prompt, max_length=50, do_sample=False)
                cons_text = res[0]['generated_text']
        
        total_reviews = sum([row.get(f"{i}_star", 0) for i in range(1, 6)])
        
        analyzed_data.append({
            "App_ID": app_id,
            "Title": row['Title'],
            "Installs": row['Installs'],
            "Rating": row['Rating'],
            "Total_Reviews": total_reviews,
            "Pros_Keywords": pros_text,
            "Cons_Keywords": cons_text
        })
        
    res_df = pd.DataFrame(analyzed_data)
    res_df.to_csv("competitors_nlp_dynamic.csv", index=False)
    print(f"Processed {len(res_df)} games and saved to competitors_nlp_dynamic.csv")


def analyze_reviews_gpt2():
    extractor = pipeline("text-generation", model="openai-community/gpt2")
    df = pd.read_csv("competitors_usa_v2.csv")
    analyzed_data = []
    
    for _, row in df.iterrows():
        app_id = row['App_ID']
        pros_text = ""
        cons_text = ""
        
        rev_path = f"reviews_v2/{app_id}.json"
        if os.path.exists(rev_path):
            with open(rev_path, "r", encoding="utf-8") as f:
                reviews = json.load(f)
                
            good_revs = [r['text'] for r in reviews.get('star_5', [])[:5] + reviews.get('star_4', [])[:5]]
            bad_revs = [r['text'] for r in reviews.get('star_1', [])[:5] + reviews.get('star_2', [])[:5]]
            
            if good_revs:
                good_combined = " ".join(good_revs)[:600]
                prompt = f"Reviews: {good_combined}\nKey positive features: 1."
                res = extractor(prompt, max_new_tokens=30, num_return_sequences=1, pad_token_id=50256)
                pros_text = res[0]['generated_text'].replace(prompt, "1.").strip()
                
            if bad_revs:
                bad_combined = " ".join(bad_revs)[:600]
                prompt = f"Reviews: {bad_combined}\nKey negative issues: 1."
                res = extractor(prompt, max_new_tokens=30, num_return_sequences=1, pad_token_id=50256)
                cons_text = res[0]['generated_text'].replace(prompt, "1.").strip()
        
        total_reviews = sum([row.get(f"{i}_star", 0) for i in range(1, 6)])
        
        analyzed_data.append({
            "App_ID": app_id,
            "Title": row['Title'],
            "Installs": row['Installs'],
            "Rating": row['Rating'],
            "Total_Reviews": total_reviews,
            "Pros_Keywords": pros_text,
            "Cons_Keywords": cons_text
        })
        
    res_df = pd.DataFrame(analyzed_data)
    res_df.to_csv("competitors_nlp_dynamic.csv", index=False)
    print("Done")


def extract_unique_features():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    
    def get_unique(column):
        items = set()
        for text in df[column].dropna():
            lines = str(text).split('\n')
            for line in lines:
                clean = line.strip(' 1234567890.-*,')
                if clean:
                    items.add(clean)
        return sorted(list(items))
        
    unique_pros = get_unique('Pros_Keywords')
    unique_cons = get_unique('Cons_Keywords')
    
    print("UNIQUE PROS:")
    for p in unique_pros:
        print(p)
        
    print("\nUNIQUE CONS:")
    for c in unique_cons:
        print(c)



def categorize_features():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    
    def get_unique(column):
        items = set()
        for text in df[column].dropna():
            lines = str(text).split('\n')
            for line in lines:
                clean = line.strip(' 1234567890.-*,')
                if clean:
                    items.add(clean)
        return list(items)
        
    unique_pros = get_unique('Pros_Keywords')
    unique_cons = get_unique('Cons_Keywords')
    
    with open("raw_unique_features.txt", "w", encoding="utf-8") as f:
        f.write("PROS:\n" + "\n".join(unique_pros) + "\n\nCONS:\n" + "\n".join(unique_cons))
        
    classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")
    
    pro_cats = ["good graphics", "smooth controls", "fun gameplay", "good story", "customization options", "free to play", "offline play", "easy to learn", "good music", "multiplayer"]
    con_cats = ["too many ads", "bad controls", "bugs and glitches", "repetitive", "pay to win", "boring", "bad audio", "bad graphics", "too short", "too hard", "connection issues", "battery drain", "lacks content"]
    
    mapping = {"pros": {}, "cons": {}}
    
    for pro in unique_pros:
        if len(pro) > 3:
            res = classifier(pro, pro_cats)
            mapping["pros"][pro] = res['labels'][0]
            
    for con in unique_cons:
        if len(con) > 3:
            res = classifier(con, con_cats)
            mapping["cons"][con] = res['labels'][0]
            
    with open("feature_categories_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)
        
    print("Done")

def apply_categories_from_mapping():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    
    with open("feature_categories_mapping.json", "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    def get_mapped_categories(text, map_dict):
        if pd.isna(text) or str(text).strip() == "":
            return ""
        cats = set()
        lines = str(text).split('\n')
        for line in lines:
            clean = line.strip(' 1234567890.-*,')
            if clean in map_dict:
                cats.add(map_dict[clean])
        return ", ".join(list(cats))
        
    df['Categorized_Pros'] = df['Pros_Keywords'].apply(lambda x: get_mapped_categories(x, mapping.get('pros', {})))
    df['Categorized_Cons'] = df['Cons_Keywords'].apply(lambda x: get_mapped_categories(x, mapping.get('cons', {})))
    
    df.to_csv("competitors_nlp_dynamic.csv", index=False)
    print("Done")

if __name__ == "__main__":
    analyze_reviews_gpt2()
    extract_unique_features()
    categorize_features()
    apply_categories_from_mapping()