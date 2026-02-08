import json
import loader
import processor
import visualizer

def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    data = loader.loadData("gdp_with_continent_filled.csv")

    regions = sorted(set(d['region'] for d in data))
    print("Available regions:", regions)


    if not data:
        print("No data loaded.")
        return

    analysisResult = processor.processAnalysis(data, config)

    if config.get("output") == "dashboard":
        visualizer.plotDashboard(analysisResult)
    else:
        print(analysisResult)

if __name__ == "__main__":
    main()
