import pandas as pd

PII_COLUMNS = [
    'name',
    'first_name',
    'last_name',
    'full_name',
    'ssn',
    'social_security_number',
    'email',
    'phone',
    'dob',
    'date_of_birth',
    'address',
    'street',
    'zip',
    'zip_code',
    'city',
    'state',
    'mrn',  # medical record number
]

def load_data(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.xlsx'):
        return pd.read_excel(path)
    elif path.endswith('.json'):
        return pd.read_json(path)
    else:
        raise ValueError("Unexpected format -- brrrr")
    

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    pii_removal = [col for col in df.columns if col.strip().lower().replace(' ', '_') in PII_COLUMNS]
    df = df.drop(columns=pii_removal, errors='ignore')

    return df