import json
from collections import Counter
import argparse

def inspect_resource_types(path):
    with open(path, 'r') as f:
        data = json.load(f)

    types = [entry['resource']['resourceType'] for entry in data.get('entry', []) if 'resource' in entry]
    print(Counter(types))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path to FHIR JSON file")
    args = parser.parse_args()
    inspect_resource_types(args.filepath)
