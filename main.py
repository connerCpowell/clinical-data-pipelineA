from src.ingest_clean import load_data, clean_data

df = load_data('./data/raw/20k/Aleta47_Lala778_Kovacek682_d7183866-d578-f362-a968-14acc858ee80.json')
df = clean_data(df)

df.to_csv('data/clean/cleaned_CD.json')