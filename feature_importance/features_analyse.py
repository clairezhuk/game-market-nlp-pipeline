import pandas as pd
from collections import Counter
from scipy.stats import ttest_ind
from mlxtend.frequent_patterns import apriori, association_rules

def analyze_feature_importance():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    total_games = len(df)
    
    pros_counter = Counter()
    cons_counter = Counter()
    
    for _, row in df.iterrows():
        pros = str(row['Categorized_Pros']).split(',')
        cons = str(row['Categorized_Cons']).split(',')
        
        for p in pros:
            clean_p = p.strip()
            if clean_p and clean_p != 'nan':
                pros_counter[clean_p] += 1
                
        for c in cons:
            clean_c = c.strip()
            if clean_c and clean_c != 'nan':
                cons_counter[clean_c] += 1
                
    print("PROS FREQUENCY:")
    for feature, count in pros_counter.most_common():
        pct = (count / total_games) * 100
        print(f"{feature}: {count} ({pct:.1f}%)")
        
    print("\nCONS FREQUENCY:")
    for feature, count in cons_counter.most_common():
        pct = (count / total_games) * 100
        print(f"{feature}: {count} ({pct:.1f}%)")
        
    print(f"\nTotal games in dataset: {total_games}")


def run_advanced_analysis():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    
    features = set()
    for _, row in df.iterrows():
        pros = [p.strip() for p in str(row['Categorized_Pros']).split(',') if p.strip() and p.strip() != 'nan']
        cons = [c.strip() for c in str(row['Categorized_Cons']).split(',') if c.strip() and c.strip() != 'nan']
        features.update(pros + cons)
        
    for f in features:
        df[f] = df.apply(lambda r: 1 if f in str(r['Categorized_Pros']) or f in str(r['Categorized_Cons']) else 0, axis=1)
        
    print("IMPACT ON RATING (T-test):")
    print(f"{'Feature':<25} | {'Diff':<6} | {'P-Value':<8} | {'Significance'}")
    print("-" * 60)
    
    for f in features:
        with_f = df[df[f] == 1]['Rating'].dropna()
        without_f = df[df[f] == 0]['Rating'].dropna()
        
        if len(with_f) >= 3 and len(without_f) >= 3:
            stat, p = ttest_ind(with_f, without_f, equal_var=False)
            diff = with_f.mean() - without_f.mean()
            sig = "Significant" if p < 0.05 else "Noise"
            print(f"{f:<25} | {diff:>+6.2f} | {p:>8.3f} | {sig}")

    print("\nFREQUENT COMBINATIONS (Market Basket Analysis):")
    basket = df[list(features)].astype(bool)
    
    frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)
    
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
        rules = rules.sort_values(['lift', 'confidence'], ascending=[False, False]).head(15)
        
        print(f"{'Rule (A -> B)':<50} | {'Conf':<5} | {'Lift':<5}")
        print("-" * 65)
        for _, r in rules.iterrows():
            ant = ", ".join(list(r['antecedents']))
            con = ", ".join(list(r['consequents']))
            rule_str = f"{ant} -> {con}"
            print(f"{rule_str:<50} | {r['confidence']:>5.2f} | {r['lift']:>5.2f}")
    else:
        print("No frequent combinations found with current support threshold.")



def run_grouped_analysis():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    
    final_features = [
        'estetics', 'useful controls', 'fun gameplay', 'customization options',
        'ugly', 'lacks content', 'repetitive', 'boring', 'bags', 
        'hard mechanics', 'monetization'
    ]
    
    for f in final_features:
        df[f] = 0
        
    for index, row in df.iterrows():
        pros = str(row['Categorized_Pros']).lower()
        cons = str(row['Categorized_Cons']).lower()
        
        if 'good graphics' in pros or 'good music' in pros:
            df.at[index, 'estetics'] = 1
        if 'smooth controls' in pros or 'easy to learn' in pros:
            df.at[index, 'useful controls'] = 1
        if 'fun gameplay' in pros:
            df.at[index, 'fun gameplay'] = 1
        if 'customization options' in pros:
            df.at[index, 'customization options'] = 1
            
        if 'bad graphics' in cons or 'bad audio' in cons:
            df.at[index, 'ugly'] = 1
        if 'lacks content' in cons:
            df.at[index, 'lacks content'] = 1
        if 'repetitive' in cons:
            df.at[index, 'repetitive'] = 1
        if 'boring' in cons:
            df.at[index, 'boring'] = 1
        if 'bugs and glitches' in cons or 'connection issues' in cons:
            df.at[index, 'bags'] = 1
        if 'bad controls' in cons or 'too hard' in cons:
            df.at[index, 'hard mechanics'] = 1
        if 'too many ads' in cons or 'pay to win' in cons:
            df.at[index, 'monetization'] = 1

    print("IMPACT ON RATING (T-test):")
    print(f"{'Feature':<25} | {'Diff':<6} | {'P-Value':<8} | {'Significance'}")
    print("-" * 60)
    
    for f in final_features:
        with_f = df[df[f] == 1]['Rating'].dropna()
        without_f = df[df[f] == 0]['Rating'].dropna()
        
        if len(with_f) >= 3 and len(without_f) >= 3:
            stat, p = ttest_ind(with_f, without_f, equal_var=False)
            diff = with_f.mean() - without_f.mean()
            sig = "Significant" if p < 0.05 else "Noise"
            print(f"{f:<25} | {diff:>+6.2f} | {p:>8.3f} | {sig}")

    print("\nFREQUENT COMBINATIONS (Market Basket Analysis):")
    basket = df[final_features].astype(bool)
    
    frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)
    
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
        rules = rules.sort_values(['lift', 'confidence'], ascending=[False, False]).head(15)
        
        print(f"{'Rule (A -> B)':<50} | {'Conf':<5} | {'Lift':<5}")
        print("-" * 65)
        for _, r in rules.iterrows():
            ant = ", ".join(list(r['antecedents']))
            con = ", ".join(list(r['consequents']))
            rule_str = f"{ant} -> {con}"
            print(f"{rule_str:<50} | {r['confidence']:>5.2f} | {r['lift']:>5.2f}")
    else:
        print("No frequent combinations found.")


def calculate_score(pros_str, cons_str):
    pros = [p.strip() for p in str(pros_str).split(',') if p.strip() and p.strip() != 'nan']
    cons = [c.strip() for c in str(cons_str).split(',') if c.strip() and c.strip() != 'nan']
    
    cons_score = 0
    for c in cons:
        if c == 'too hard':
            continue
        elif c == 'boring':
            cons_score += 2
        else:
            cons_score += 1
            
    return len(pros) - cons_score

def sort_for_manual_review():
    df = pd.read_csv("competitors_nlp_dynamic.csv")
    avg_rating = df['Rating'].mean()
    
    df['Score'] = df.apply(lambda row: calculate_score(row['Categorized_Pros'], row['Categorized_Cons']), axis=1)
    df['Rating_Bin'] = (df['Rating'] // 0.2) * 0.2
    
    pos_df = df[df['Rating'] >= avg_rating].sort_values(
        by=['Rating_Bin', 'Score', 'Rating'], ascending=[False, False, False]
    )
    neg_df = df[df['Rating'] < avg_rating].sort_values(
        by=['Rating_Bin', 'Score', 'Rating'], ascending=[True, True, True]
    )
    
    def write_file(filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, row in enumerate(data.itertuples(), 1):
                p_str = str(row.Categorized_Pros) if pd.notna(row.Categorized_Pros) else ""
                c_str = str(row.Categorized_Cons) if pd.notna(row.Categorized_Cons) else ""
                r = float(row.Rating) if pd.notna(row.Rating) else 0.0
                f.write(f"{i}. {row.Title} --> Rating: {r:.2f}, Score: {row.Score}\n")
                f.write(f"   Pros: [{p_str}] | Cons: [{c_str}]\n")
                if i % 5 == 0:
                    f.write("-" * 40 + "\n")
                    
    write_file("positive_reviews_sorted.txt", pos_df)
    write_file("negative_reviews_sorted.txt", neg_df)



def create_feature_lists():
    df = pd.read_csv("competitors_nlp_dynamic.csv")

    def get_games(feature_list, column):
        games = []
        for _, row in df.iterrows():
            val = str(row[column]).lower()
            if any(f in val for f in feature_list):
                p_str = str(row['Categorized_Pros']) if pd.notna(row['Categorized_Pros']) else ""
                c_str = str(row['Categorized_Cons']) if pd.notna(row['Categorized_Cons']) else ""
                r = float(row['Rating']) if pd.notna(row['Rating']) else 0.0
                games.append(f"{row['Title']} --> Rating: {r:.2f} | Pros: [{p_str}] | Cons: [{c_str}]")
        return games

    def write_group(file, title, games):
        file.write(f"=== {title} ===\n")
        for i, g in enumerate(games, 1):
            file.write(f"{i}. {g}\n")
        file.write("\n" + "-" * 50 + "\n\n")

    with open("negative_specific_features.txt", "w", encoding="utf-8") as f:
        write_group(f, "BORING", get_games(['boring'], 'Categorized_Cons'))
        write_group(f, "MONETIZATION (too many ads, pay to win)", get_games(['too many ads', 'pay to win'], 'Categorized_Cons'))
        write_group(f, "BAD CONTROLS", get_games(['bad controls'], 'Categorized_Cons'))

    with open("positive_specific_features.txt", "w", encoding="utf-8") as f:
        write_group(f, "FUN GAMEPLAY", get_games(['fun gameplay'], 'Categorized_Pros'))
        write_group(f, "USEFUL CONTROLS (smooth controls, easy to learn)", get_games(['smooth controls', 'easy to learn'], 'Categorized_Pros'))
        write_group(f, "GOOD GRAPHICS", get_games(['good graphics'], 'Categorized_Pros'))


if __name__ == "__main__":
    run_advanced_analysis()
    run_grouped_analysis()
    sort_for_manual_review()
    create_feature_lists()
