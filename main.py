import json
import loader
import processor
import visualizer

def validateConfig(config):
    """
    Requirement: Validate configuration fields.
    Returns True if valid, False otherwise.
    """
    if "analyses" not in config:
        print("Error: Config missing 'analyses' list.")
        return False
    
    for i, item in enumerate(config["analyses"]):
        if "type" not in item:
            print(f"Error: Analysis item #{i+1} missing 'type'.")
            return False
        
        # Check specific fields based on type
        if item["type"] == "region":
            if not all(k in item for k in ("region", "year", "operation")):
                print(f"Error: Region analysis #{i+1} missing required fields.")
                return False
        elif item["type"] == "country_trend":
            if not all(k in item for k in ("country", "start_year", "end_year")):
                print(f"Error: Country analysis #{i+1} missing required fields.")
                return False
                
    return True

def main():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON.")
        return

    # Step 1: Validate Config
    if not validateConfig(config):
        return

    # Step 2: Load Data
    data = loader.loadData("gdp_with_continent_filled.csv")
    if not data:
        print("No data loaded.")
        return

    print(f"Successfully loaded {len(data)} records.\n")

    # Step 3: Run Analyses
    for analysis in config["analyses"]:
        print(f"--- Running Analysis: {analysis['type'].upper()} ---")
        
        if analysis["type"] == "region":
            result = processor.processAnalysis(data, analysis)
            result["graph"] = analysis.get("graph", "bar")
            
            print(f"Region: {analysis['region']}")
            print(f"Operation: {analysis['operation'].capitalize()}")
            print(f"Result: ${result['resultValue']:,.2f}")
            
            visualizer.plotDashboard(result)

        elif analysis["type"] == "country_trend":
            result = processor.processCountryTrend(
                data, 
                analysis["country"], 
                analysis["start_year"], 
                analysis["end_year"]
            )
            
            if result:
                # GAP FIXED: Printing the stats we calculated
                stats = result.get("stats", {})
                print(f"Country: {analysis['country']}")
                print(f"Average GDP ({analysis['start_year']}-{analysis['end_year']}): ${stats.get('average', 0):,.2f}")
                
                visualizer.plotDashboard(result)
            else:
                print(f"Error: Country '{analysis['country']}' not found.")
        
        print("\n")

if __name__ == "__main__":
    main()
