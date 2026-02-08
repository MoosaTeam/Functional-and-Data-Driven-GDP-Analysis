import statistics

# --- Helper Functions ---

def filterByRegion(data, regionName):
    return list(filter(lambda country: country['region'] == regionName, data))

def getYearValues(data, year):
    return [country['gdp'][year] for country in data if year in country['gdp']]

def calculateStats(values, operationName):
    if not values: return 0.0
    operations = {
        "average": statistics.mean,
        "sum": sum,
        "max": max,
        "min": min
    }
    func = operations.get(operationName.lower())
    return func(values) if func else 0.0

# --- Main Functions ---

def processAnalysis(data, config):
    targetRegion = config.get('region')
    targetYear = config.get('year')
    operation = config.get('operation', 'average')

    regionData = filterByRegion(data, targetRegion)
    gdpValues = getYearValues(regionData, targetYear)
    countryNames = [c['country'] for c in regionData if targetYear in c['gdp']]
    
    resultStat = calculateStats(gdpValues, operation)

    return {
        "title": f"{operation.capitalize()} GDP of {targetRegion} in {targetYear}",
        "resultValue": resultStat,
        "plotData": {"labels": countryNames, "values": gdpValues},
        "year": targetYear,
        "region": targetRegion
    }

def processCountryTrend(data, countryName, startYear, endYear):
    # Functional approach to find the country
    countryObj = next(filter(lambda c: c['country'].lower() == countryName.lower(), data), None)
    
    if not countryObj:
        return None

    # List Comprehension to extract range of years
    years = [y for y in range(startYear, endYear + 1) if y in countryObj['gdp']]
    values = [countryObj['gdp'][y] for y in years]

    # GAP FIXED: Calculate the stats for the country trend
    avg_val = statistics.mean(values) if values else 0.0
    total_val = sum(values)

    return {
        "title": f"GDP Trend of {countryName} ({startYear}-{endYear})",
        "plotData": { "labels": years, "values": values },
        "graph": "line",
        # Adding these stats to satisfy requirements
        "stats": { 
            "average": avg_val, 
            "total": total_val 
        }
    }
