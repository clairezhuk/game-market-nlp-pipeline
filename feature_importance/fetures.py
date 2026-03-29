import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_impact():
    df = pd.read_csv("competitors_nlp_analyzed.csv")
    
    mask_has = df['Mechanics'].fillna('').str.contains('avoid obstacles', case=False)# & \
               #df['Mechanics'].fillna('').str.contains('endless runner', case=False)
    #mask_not = ~df['Mechanics'].fillna('').str.contains('color matching', case=False) & \
     #          ~df['Mechanics'].fillna('').str.contains('timing', case=False)
               
    filtered_df = df[mask_has].copy()
    filtered_df.to_csv("filtered_competitors.csv", index=False)
    
    pros = ['relaxing', 'good graphics', 'smooth controls', 'good physics', 'offline play', 'challenging']
    cons = ['too many ads', 'bad controls', 'bugs and glitches', 'repetitive', 'pay to win', 'battery drain']
    
    print(f"Games after filtering: {len(filtered_df)}")
    print("\nImpact on Rating (Difference in Average Rating: With Feature vs Without Feature)")
    
    print("\nPROS:")
    for pro in pros:
        has_feature = df['Pros'].fillna('').str.contains(pro, case=False)
        if has_feature.sum() > 0 and (~has_feature).sum() > 0:
            avg_with = df[has_feature]['Rating'].mean()
            avg_without = df[~has_feature]['Rating'].mean()
            diff = avg_with - avg_without
            print(f"{pro:<15}: {diff:+.2f}")
        else:
            print(f"{pro:<15}: Not enough data")
            
    print("\nCONS:")
    for con in cons:
        has_feature = df['Cons'].fillna('').str.contains(con, case=False)
        if has_feature.sum() > 0 and (~has_feature).sum() > 0:
            avg_with = df[has_feature]['Rating'].mean()
            avg_without = df[~has_feature]['Rating'].mean()
            diff = avg_with - avg_without
            print(f"{con:<18}: {diff:+.2f}")
        else:
            print(f"{con:<18}: Not enough data")

def visualize_correlation():
    df = pd.read_csv("filtered_competitors.csv")
    
    pros = ['relaxing', 'good graphics', 'smooth controls', 'good physics', 'offline play', 'challenging']
    cons = ['too many ads', 'bad controls', 'bugs and glitches', 'repetitive', 'pay to win', 'battery drain']
    
    for pro in pros:
        df[f'Pro_{pro}'] = df['Pros'].fillna('').str.contains(pro, case=False).astype(int)
        
    for con in cons:
        df[f'Con_{con}'] = df['Cons'].fillna('').str.contains(con, case=False).astype(int)
        
    features = [f'Pro_{pro}' for pro in pros] + [f'Con_{con}' for con in cons]
    corr_matrix = df[features].corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, center=0)
    plt.title("Correlation Matrix: Pros vs Cons")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("pros_cons_correlation.png", dpi=300)
    plt.close()
    
    print("Done")


def generate_examples():
    df = pd.read_csv("filtered_competitors.csv")
    
    pros = ['relaxing', 'good graphics', 'smooth controls', 'good physics', 'offline play', 'challenging']
    cons = ['too many ads', 'bad controls', 'bugs and glitches', 'repetitive', 'pay to win', 'battery drain']
    
    def get_matches(text, target_list):
        if pd.isna(text): return []
        return [item for item in target_list if item.lower() in str(text).lower()]

    df['Matched_Pros'] = df['Pros'].apply(lambda x: get_matches(x, pros))
    df['Matched_Cons'] = df['Cons'].apply(lambda x: get_matches(x, cons))
    df['Pros_Count'] = df['Matched_Pros'].apply(len)
    df['Cons_Count'] = df['Matched_Cons'].apply(len)
    df['Pos_Score'] = df['Pros_Count'] - df['Cons_Count']
    
    avg_rating = df['Rating'].mean()
    
    pos_df = df[df['Rating'] > avg_rating].sort_values(by=['Pos_Score', 'Rating'], ascending=[False, False])
    neg_df = df[df['Rating'] < avg_rating].sort_values(by=['Cons_Count', 'Rating'], ascending=[False, True])
    
    def write_file(filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            for i, row in enumerate(data.itertuples(), 1):
                p_str = ", ".join(row.Matched_Pros)
                c_str = ", ".join(row.Matched_Cons)
                rating = float(row.Rating) if pd.notna(row.Rating) else 0.0
                f.write(f"{i}. {row.Title} --> {rating:.1f}, [{p_str}] | [{c_str}]\n")
                if i % 5 == 0:
                    f.write("-" * 40 + "\n")
                    
    write_file("positive_examples.txt", pos_df)
    write_file("negative_examples.txt", neg_df)
    print("Files created.")


if __name__ == "__main__":
    #analyze_impact()
    #visualize_correlation()
    generate_examples()