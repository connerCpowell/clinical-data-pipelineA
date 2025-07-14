import pandas as pd
import json

PII_COLUMNS = [
    'name',
    'first_name',
    'last_name',
    'full_name',
    'ssn',
    'social_security_number',
    'email',
    'phone',
    #'dob',
    #'date_of_birth',
    #'address',
    #'street',
    #'zip',
    #'zip_code',
    #'city',
    #'state',
    #'mrn',  # medical record number
]


def flatten_file(jfile):
    flat = {}
    def _flatten(obj, prefix=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _flatten(v, f"{prefix}{k}_" if prefix else k + "_")
        elif isinstance(obj, list):
            flat[prefix.rstrip('_')] = str(obj)
        else:
            flat[prefix.strip('_')] = obj
    _flatten(jfile)
    return flat

def load_data(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.xlsx'):
        return pd.read_excel(path)
    elif path.endswith('.json'):
        return pd.read_json(path)
    else:
        raise ValueError("Unexpected format -- brrrr")
    
def load_fhir_json(path: str) -> pd.DataFrame:
    with open(path, 'r') as f:
        data = json.load(f)

    good_cols = ['Patient', 'Encounter', 'Condition', 'Claim', 'DiagnosticReport']

    flat_rec = []
    for entry in data.get('entry', []):
        res = entry.get('resource', {})
        if res.get('resourceType') in good_cols:
            flat = flatten_file(res)
            flat_rec.append(flat)

    df = pd.DataFrame(flat_rec)
    return df

            
    

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    pii_removal = [col for col in df.columns if col.strip().lower().replace(' ', '_') in PII_COLUMNS]
    df = df.drop(columns=pii_removal, errors='ignore')

    return df