import os
import json
import pandas as pd
from google_play_scraper import search, app, reviews, Sort

def scrape_mechanical_competitors():
    keywords = [
        "hyper casual obstacle", 
        "swipe to dodge", 
        "endless runner casual", 
        "arcade dodging game", 
        "reflex swipe"
    ]
    
    os.makedirs("reviews_v2", exist_ok=True)
    app_ids = set()
    
    for kw in keywords:
        try:
            results = search(kw, lang="en", country="us")
            for r in results:
                app_ids.add(r["appId"])
        except Exception:
            continue
            
    games_data = []
    
    for app_id in list(app_ids):
        try:
            details = app(app_id, lang="en", country="us")
        except Exception:
            continue
            
        genre = details.get("genre", "")
        if not details.get("free") or not details.get("adSupported") or "Puzzle" in genre:
            continue
            
        game_reviews = {}
        skip_game = False
        
        for score in range(1, 6):
            try:
                revs, _ = reviews(
                    app_id, lang="en", country="us", sort=Sort.MOST_RELEVANT, count=100, filter_score_with=score
                )
            except Exception:
                revs = []
                
            valid = [r for r in revs if r.get("content") and len(r.get("content")) >= 30][:20]
            
            if not valid:
                skip_game = True
                break
                
            game_reviews[f"star_{score}"] = [{"text": r["content"], "thumbsUp": r["thumbsUpCount"]} for r in valid]
            
        if skip_game:
            continue
            
        with open(f"reviews_v2/{app_id}.json", "w", encoding="utf-8") as f:
            json.dump(game_reviews, f, indent=4, ensure_ascii=False)
            
        hist = details.get("histogram", [0, 0, 0, 0, 0])
        
        games_data.append({
            "App_ID": app_id,
            "Title": details.get("title"),
            "Installs": details.get("maxInstalls"),
            "Rating": details.get("score"),
            "1_star": hist[0],
            "2_star": hist[1],
            "3_star": hist[2],
            "4_star": hist[3],
            "5_star": hist[4],
            "Description": details.get("description")
        })
        
    if games_data:
        df = pd.DataFrame(games_data)
        df.to_csv("competitors_usa_v2.csv", index=False, encoding="utf-8")
        print(f"Saved {len(games_data)} games.")

if __name__ == "__main__":
    scrape_mechanical_competitors()