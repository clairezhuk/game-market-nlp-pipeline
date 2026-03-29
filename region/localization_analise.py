import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def generate_reports_a():
    df = pd.read_excel("Region_analysis.xlsx")
    df['Margin'] = df['Estimated eCPM'] - df['Estimated CPI']
    df = df.dropna(subset=['Margin'])
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Margin",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title="Margin (Estimated eCPM - Estimated CPI)"
    )
    
    fig.write_html("Map_Analysis2.html")
    print("Map saved to Map_Analysis2.html (open in browser to view)")


def generate_reports():
    df = pd.read_excel("Region_analysis.xlsx")
    
    # 1. Розрахунок метрик
    df['Margin'] = df['Estimated eCPM'] - df['Estimated CPI']
    df['Market_Potential'] = df['Potential Player Volume'] * df['Margin']
    
    # Очищення від пустих даних
    df = df.dropna(subset=['Margin', 'Market_Potential'])
    
    # --- МАПА ---
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Market_Potential",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title="Market Potential (Колір) та Чиста різниця eCPM - CPI (Текст)"
    )
    
    # Додавання тексту (Margin) на мапу
    fig.add_trace(
        go.Scattergeo(
            locations=df["Country"],
            locationmode="country names",
            text=df["Margin"].round(2).astype(str),
            mode="text",
            textfont=dict(size=10, color="darkred"),
            showlegend=False
        )
    )
    fig.write_html("Map_Analysis.html")
    print("Map saved to Map_Analysis.html (open in browser to view)")

    # --- ДІАГРАМА: Мови ---
    plt.figure(figsize=(12, 6))
    lang_df = df.groupby('Languages')['Margin'].mean().sort_values(ascending=False).head(20)
    lang_df.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Average Margin (eCPM - CPI) by Language (Top 20)")
    plt.ylabel("Margin")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("Languages_Margin.png", dpi=300)
    plt.close()

    # --- ДІАГРАМА: Регіони ---
    plt.figure(figsize=(12, 6))
    reg_df = df.groupby('Region')['Margin'].mean().sort_values(ascending=False).head(20)
    reg_df.plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.title("Average Margin (eCPM - CPI) by Region (Top 20)")
    plt.ylabel("Margin")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("Regions_Margin.png", dpi=300)
    plt.close()
    
    print("Bar charts saved as PNG files.")



def calculate_language_roi():
    df = pd.read_excel("Region_analysis.xlsx")
    
    ADS_PER_USER = 8
    
    df['Android Share'] = pd.to_numeric(df['Android Share'].astype(str).str.replace('%', ''), errors='coerce') / 100.0
    df['Android Share'] = df['Android Share'].fillna(0.1).clip(lower=0.01)
    
    df['eCPI'] = df['Estimated CPI'] / df['Android Share']
    df['LTV'] = (df['Estimated eCPM'] / 1000) * ADS_PER_USER
    
    df['Margin'] = df['LTV'] - df['eCPI']
    df['Language_ROI'] = df['Potential Player Volume'] * df['Margin']
    
    lang_df = df.groupby('Languages')['Language_ROI'].sum().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    lang_df.plot(kind='bar', color='coral', edgecolor='black')
    plt.title("Total ROI by Language")
    plt.ylabel("Projected ROI")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("Language_ROI.png", dpi=300)
    plt.close()
    
    df_map = df.dropna(subset=['Margin', 'Language_ROI'])
    
    fig = px.choropleth(
        df_map,
        locations="Country",
        locationmode="country names",
        color="Language_ROI",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title="Total ROI by Country (Color) & Margin LTV-eCPI (Text)"
    )
    
    fig.add_trace(
        go.Scattergeo(
            locations=df_map["Country"],
            locationmode="country names",
            text=df_map["Margin"].round(2).astype(str),
            mode="text",
            textfont=dict(size=10, color="darkred"),
            showlegend=False
        )
    )
    
    fig.write_html("ROI_Map.html")
    
    df.to_excel("Region_analysis_v2.xlsx", index=False)
    print("Done")


def calculate_organic_potential():
    df = pd.read_excel("Region_analysis.xlsx")
    
    df = df[df['Potential Player Volume'] > 0].copy()
    
    ADS_PER_USER = 8
    
    df['Android Share'] = pd.to_numeric(df['Android Share'].astype(str).str.replace('%', ''), errors='coerce') / 100.0
    df['Android Share'] = df['Android Share'].fillna(0.1).clip(lower=0.01)
    
    df['eCPI'] = df['Estimated CPI'] / df['Android Share']
    df['LTV'] = (df['Estimated eCPM'] / 1000) * ADS_PER_USER
    
    df['Paid_Margin'] = df['LTV'] - df['eCPI']
    df['Organic_Revenue_Potential'] = df['Potential Player Volume'] * df['LTV']
    
    lang_df = df.groupby('Languages')['Organic_Revenue_Potential'].sum().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    lang_df.plot(kind='bar', color='coral', edgecolor='black')
    plt.title("Organic Revenue Potential by Language ($)")
    plt.ylabel("Potential Revenue")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("Language_Organic_Potential.png", dpi=300)
    plt.close()
    
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Organic_Revenue_Potential",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title="Organic Revenue Potential by Country ($)"
    )
    fig.write_html("Organic_Revenue_Map.html")
    
    df.to_excel("Region_analysis_v2.xlsx", index=False)
    print("Done")



def calculate_adjusted_roi():
    df = pd.read_excel("Region_analysis.xlsx")
    df = df[df['Potential Player Volume'] > 0].copy()
    
    ADS_PER_USER = 15
    BASE_TIME_COST = 0.05 
    
    df['Android Share'] = pd.to_numeric(df['Android Share'].astype(str).str.replace('%', ''), errors='coerce') / 100.0
    df['Android Share'] = df['Android Share'].fillna(0.1).clip(lower=0.01)
    
    df['LTV'] = (df['Estimated eCPM'] / 1000) * ADS_PER_USER
    df['Effective_Time_Cost'] = BASE_TIME_COST / df['Android Share']
    
    df['Organic_Margin'] = df['LTV'] - df['Effective_Time_Cost']
    df['Adjusted_ROI'] = df['Potential Player Volume'] * df['Organic_Margin']
    
    lang_df = df.groupby('Languages')['Adjusted_ROI'].sum().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(10, 5))
    lang_df.plot(kind='bar', color='purple', edgecolor='black')
    plt.title("Adjusted ROI by Language")
    plt.tight_layout()
    plt.savefig("Language_Adjusted_ROI.png", dpi=300)
    plt.close()
    
    fig = px.choropleth(
        df, locations="Country", locationmode="country names",
        color="Adjusted_ROI", hover_name="Country",
        color_continuous_scale="RdYlGn", title="Adjusted ROI by Country"
    )
    fig.write_html("Adjusted_ROI_Map.html")
    
    df.to_excel("Region_analysis_v3.xlsx", index=False)

    

if __name__ == "__main__":
    #generate_reports()
    #generate_reports_a()
    #calculate_language_roi()
    #calculate_organic_potential()
    calculate_adjusted_roi()