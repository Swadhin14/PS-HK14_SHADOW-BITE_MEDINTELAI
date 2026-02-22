import re
from typing import List, Dict


def extract_medical_data(text: str) -> List[Dict]:
    """
    Extract structured lab test data from tabular medical report text.
    """

    results = []

    # Pattern for lines like:
    # Hemoglobin 12.5 g/dL 13.0 - 17.0 Low
    pattern = re.compile(
        r"([A-Za-z\s]+?)\s+([\d.]+)\s+([^\s]+)\s+([<>\d.\s\-–]+)\s+(Low|High|Normal|Slightly High|Slightly Low)",
        re.MULTILINE
    )

    matches = pattern.findall(text)

    for match in matches:
        test_name = match[0].strip()
        value = float(match[1])
        unit = match[2]
        normal_range = match[3].strip()
        status = match[4]

        results.append({
            "test_name": test_name,
            "value": value,
            "unit": unit,
            "normal_range": normal_range,
            "status": status
        })

    return results