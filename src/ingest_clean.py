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
    
def load_fhir_json_seperated(path: str):
    with open(path, 'r') as f:
        data = json.load(f)

    p_data = []
    other_records = []

    for entry in data.get('entry', []):
        res = entry.get('resource', {})
        if res.get('resourceType') == 'Patient':
            p_data.append(flatten_file(res))
        elif res.get('resouceType') in ['Encounter', 'Condition', 'Claim', 'DiagnosticReport']:
            flat = flatten_file(res)
            other_records.append(flat)

    df_patient = pd.DataFrame(p_data)
    df_events = pd.DataFrame(other_records)


    return df_patient, df_events


def load_fhir_json_seperated(path: str):
    with open(path, 'r') as f:
        data = json.load(f)


def trim_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_keep = [
        'subject_reference',
        'resourceType',
        'gender',
        'birthDate',
        'maritalStatus_text',
        'communication_language_text',
        'type_0_text',
        'period_start',
        'period_end',
        'location_0_location_display',
        'code_text',
        'total_value',
        'diagnosis_0_type_0_coding_0_code',
        'issued',
        'outcome',
        'participant_0_role_0_text',
        'suppliedItem_itemCodeableConcept_text',
        'manufactureDate'
    ]
    # Only keep what's present in the DataFrame
    return df[[col for col in columns_to_keep if col in df.columns]]    

def row_smush(df: pd.DataFrame) -> pd.DataFrame:
    df['subject_reference'] = df['subject_reference'].ffill()
    df['gender'] = df['gender'].ffill()

    grouped = df.groupby('subject_reference')
    

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    pii_removal = [col for col in df.columns if col.strip().lower().replace(' ', '_') in PII_COLUMNS]
    df = df.drop(columns=pii_removal, errors='ignore')

    return df