from src.ingest_clean import load_data, clean_data

df = load_data('..')
df = clean_data(df)

df.to_csv('data/cleaned/cleaned_CD.json')