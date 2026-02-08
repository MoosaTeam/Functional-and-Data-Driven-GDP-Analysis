import statistics

def filterByRegion(data, regionName):
    return list(filter(lambda country: country['region'] == regionName, data))

def getYearValues(data, year):
    return [country['gdp'][year] for country in data if year in country['gdp']]

def calculateStats(values, operationName):
    if not values:
        return 0.0

    operations = {
            "average": statistics.mean,
            "sum": sum,
            "max": max,
            "min": min
            }

    func = operations.get(operationName.lower())

    if func:
        return func(values)
    else:
        print(f"Warning: Operation '{operationName}' not recognized.")
        return 0.0

def processAnalysis(data, config):
    targetRegion = config['region']
    targetYear = config['year']
    operation = config['operation']

    regionData = filterByRegion(data, targetRegion)
    gdpValues = getYearValues(regionData, targetYear)
    countryNames = [countryName['country'] for countryName in regionData if targetYear in countryName['gdp']]
    
    resultStat = calculateStats(gdpValues, operation)

    return {
            "title": f"{operation.capitalize()} GDP of {targetRegion} in {targetYear}",
            "resultValue": resultStat,
            "plotData": {
                "labels": countryNames,
                "values": gdpValues
                },
            "year": targetYear,
            "region": targetRegion
    }


def processCountryTrend(data, countryName, startYear, endYear):
    for c in data:
        if c['country'].lower() == countryName.lower():
            years = []
            values = []
            for year in range(startYear, endYear + 1):
                if year in c['gdp']:
                    years.append(year)
                    values.append(c['gdp'][year])

            return {
                "title": f"GDP Trend of {countryName} ({startYear}-{endYear})",
                "plotData": {
                    "labels": years,
                    "values": values
                },
                "graph": "line"
            }
    return None
