import csv
import os
from typing import List, Dict


def get_csv_data(filename: str) -> List[Dict]:
    """
    Reads a CSV file from the 'test_data' directory.

    Returns:
        List[Dict]: A list of dictionaries representing the rows,
                    e.g., [{'sku': 'A01', 'quantity': '1'}, ...]
    """
    # Dynamically retrieve the project root directory path
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "test_data", filename)

    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"❌ Error: Test data file not found: {file_path}")
        return []
