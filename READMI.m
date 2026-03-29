# Data Analytics & NLP Pipeline: Game Market ROI & Competitor Insights

## Objective
A modular data pipeline built to identify the most profitable geographic markets for mobile game localization and to extract statistically significant game features from user reviews using Natural Language Processing. 

## Tech Stack
* Data Processing: Python, Pandas, NumPy
* NLP & LLMs: HuggingFace (Flan-T5, GPT-2), Prompt Engineering
* Statistical Analysis: SciPy (Student`s t-test), Market Basket Analysis
* Visualization: Matplotlib, Geographic Mapping
* Data Extraction: Web Scraping, Google Play API

## Pipeline Architecture

### Part 1: Market ROI & Localization Analysis
* demographic.py
* amound_players.py
* android.py
* icp.py
* localization_analise.py

### Part 2: NLP Review Analysis & Feature Importance
* reviuws_parser.py
* analise_nlp.py
* features_analyse.py

## Key Features
* Calculates comparative ROI and organic growth potential across different regions.
* Automates the extraction of missing dataset metrics using LLM prompt engineering.
* Categorizes unstructured user reviews into structured feature tags using open-source models.
* Evaluates the statistical significance of specific game features on overall app ratings.
* Recommends optimal competitor games for manual breakdown based on weighted positive and negative criteria.

## Execution
python demographic.py
python amound_players.py
python android.py
python icp.py
python localization_analise.py
python reviuws_parser.py
python analise_nlp.py
python features_analyse.py