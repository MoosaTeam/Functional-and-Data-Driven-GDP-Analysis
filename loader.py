import csv
from typing import List, Dict, Any

def isYearColumn(header: str) -> bool:

    return header.isdigit() and len(header) == 4

def parseGDP(value: str) -> float:

    try:
        return float(value)
    except ValueError:
        return 0.0

def cleanRow(row: Dict[str, str]) -> Dict[str, Any]:

    gdpData = {
            int(k): parseGDP(v)
            for k, v in row.items()
            if isYearColumn(k) and v.strip() != ""
            }

    return {
            "country": row.get("Country Name", "Unknown"),
            "code": row.get("Country Code", "N/A"),
            "region": row.get("Continent", "Unknown"),
            "gdp": gdpData
            }

def loadData(filename: str) -> List[Dict[str, Any]]:
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            cleanedData = list(map(cleanRow, reader))
            return cleanedData
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

if __name__ == "__main__":

    fileName = "gdp_with_continent_filled.csv"

    data = loadData(fileName)

    if data:
        print(f"Successfully loaded {len(data)} records.")
        print("-" * 30)
        print("Sample Record (First Entry):")
        print(data[0])
        print("-" * 30)

        pakistan = next((d for d in data if d["country"] == "Pakistan"), None)
        if pakistan:
            print(f"Pakistan Region: {pakistan['region']}")
            print(f"Pakistan 2020 GDP: {pakistan['gdp'].get(2020, 'N/A')}")
