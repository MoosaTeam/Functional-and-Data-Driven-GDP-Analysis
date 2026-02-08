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

if __name__ == "__main__":
    import loader

    testConfig = {
            "region": "Asia",
            "year": 1962,
            "operation": "average"
            }

    print("Loading data for test...")
    rawData = loader.loadData("gdp_with_continent_filled.csv")

    if rawData:
        print("Running processor...")
        results = processAnalysis(rawData, testConfig)

        print("\n--- Test Results ---")
        print(f"Title: {results['title']}")
        print(f"Value: {results['resultValue']:,.2f}")
        print(f"Countries included: {len(results['plotData']['labels'])}")
    else:
        print("Could not load data. Check loader.py or CSV filename.")
