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

    event_types = [
        'Encounter', 'Condition', 'Claim', 'DiagnosticReport', 'Observation',
        'Procedure', 'ExplanationOfBenefit', 'DocumentReference',
        'SupplyDelivery', 'MedicationRequest', 'Medication',
        'MedicationAdministration', 'Immunization', 'Device',
        'CareTeam', 'CarePlan', 'ImagingStudy'
    ]

    for entry in data.get('entry', []):
        res = entry.get('resource', {})
        if res.get('resourceType') == 'Patient':
            p_data.append(flatten_file(res))
        elif res.get('resourceType') in event_types:
            flat = flatten_file(res)
            other_records.append(flat)

    df_patient = pd.DataFrame(p_data)
    df_events = pd.DataFrame(other_records)


    return df_patient, df_events


def trim_event_columns(df: pd.DataFrame) -> pd.DataFrame:
    shared_cols = [
        'subject_reference',
        'resourceType',
        'id',
        'status',
        'issued',
        'period_start',
        'period_end',
        'outcome',
        'code_text',
    ]

    # Patient-like info (if merged)
    patient_cols = [
        'gender',
        'birthDate',
        'maritalStatus_text',
        'communication_language_text',
    ]

    # Diagnostic / billing
    diag_cols = [
        'diagnosis_0_type_0_coding_0_code',
        'total_value',
    ]

    # Medication / procedures
    med_cols = [
        'suppliedItem_itemCodeableConcept_text',
        'manufactureDate',
        'participant_0_role_0_text',
    ]

    # Encounter/location data
    encounter_cols = [
        'type_0_text',
        'location_0_location_display',
    ]
    columns_to_keep = shared_cols + patient_cols + diag_cols + med_cols + encounter_cols
    return df[[col for col in columns_to_keep if col in df.columns]]    
    

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    pii_removal = [col for col in df.columns if col.strip().lower().replace(' ', '_') in PII_COLUMNS]
    df = df.drop(columns=pii_removal, errors='ignore')

    return df