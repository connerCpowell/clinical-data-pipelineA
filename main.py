from src.ingest_clean import load_fhir_json_seperated
from src.ingest_clean import clean_data
from src.ingest_clean import trim_event_columns

df_p, df_e = load_fhir_json_seperated('./data/raw/20k/Aleta47_Lala778_Kovacek682_d7183866-d578-f362-a968-14acc858ee80.json')
print('pateint', df_p.head())
print('events', df_e.head())


df_p_clean = clean_data(df_p)
df_e_clean = clean_data(df_e)
df_e_chop = trim_event_columns(df_e_clean)

df_p_clean.to_csv('data/clean/cleaned_p.csv')
df_e_chop.to_csv('data/clean/cleaned_e.csv', index=False)
print("clean csv written")