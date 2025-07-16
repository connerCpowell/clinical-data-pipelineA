import pandas as pd
from sqlalchemy import create_engine


engine = create_enqine('sqlite:///clinical.db')

df_patient = pd.read_csv('data/clean/patients.csv')
df_patient.to_sql('patients', con=engine, if_exist='replace', index=False)

df_events = pd.read_csv('data/clean/conditions.csv')
df_events.to_sql('events', con=engine, if_exist='replace', index=False)
