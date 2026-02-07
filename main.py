import csv

def read_csv(filename):
    
    # Reads a CSV file and converts rows into structured country records.
    # Returns a list of country dictionaries.
    
    countries = []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)

            year_columns = headers[4:-1]      # 1960–2024
            continent_index = len(headers) - 1

            for row in reader:
                gdp_data = {}

                for i, year in enumerate(year_columns):
                    value = row[4 + i]
                    if value.strip() != "":
                        gdp_data[int(year)] = float(value)

                country = {
                    "name": row[0],
                    "code": row[1],
                    "continent": row[continent_index],
                    "gdp": gdp_data
                }

                countries.append(country)

        return headers, countries

    except FileNotFoundError:
        print("Error: File not found.")
        return [], []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return [], []

def display_sample(headers, countries, sample_size=1):
   
    # Displays column names and sample country data.
    
    print(f"\nTotal number of countries: {len(countries)}\n")
    print("Field names:", ", ".join(headers), "\n")

    print(f"Showing first {sample_size} country record(s):\n")

    for country in countries[:sample_size]:
        print(f"Country: {country['name']}")
        print(f"Code: {country['code']}")
        print(f"Continent: {country['continent']}")
        print(f"GDP data available for {len(country['gdp'])} years\n")

def get_country_gdp(countries, country_name, year):
   
    # Returns GDP of a specific country for a given year.
    
    for country in countries:
        if country["name"].lower() == country_name.lower():
            return country["gdp"].get(year, "No data available")
    return "Country not found"

def main():
    filename = "gdp_with_continent_filled.csv"
    headers, countries = read_csv(filename)

    if headers and countries:
        display_sample(headers, countries, 2)

        # just a sample you retard
        gdp_2020 = get_country_gdp(countries, "Pakistan", 2020)
        print("Pakistan GDP in 2020:", gdp_2020)

if __name__ == "__main__":
    main()
