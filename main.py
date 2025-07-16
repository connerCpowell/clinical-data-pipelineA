from src.ingest_clean import load_fhir_json_seperated
from src.ingest_clean import clean_data
from src.ingest_clean import trim_columns

df_p, df_events = load_fhir_json_seperated('./data/raw/20k/Aleta47_Lala778_Kovacek682_d7183866-d578-f362-a968-14acc858ee80.json')
df_clean = clean_data(df_p)
df_chop = trim_columns(df_clean)

df_chop.to_csv('data/clean/cleaned_CD.csv', index=False)
print("clean csv written")