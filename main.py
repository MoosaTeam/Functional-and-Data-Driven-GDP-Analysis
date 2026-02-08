import json
import loader
import processor
import visualizer

def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    data = loader.loadData("gdp_with_continent_filled.csv")

    if not data:
        print("No data loaded.")
        return

    for analysis in config["analyses"]:
        if analysis["type"] == "region":
            result = processor.processAnalysis(data, analysis)
            result["graph"] = analysis["graph"]
            visualizer.plotDashboard(result)

        elif analysis["type"] == "country_trend":
            result = processor.processCountryTrend(
                data,
                analysis["country"],
                analysis["start_year"],
                analysis["end_year"]
            )
            if result:
                visualizer.plotDashboard(result)

if __name__ == "__main__":
    main()
