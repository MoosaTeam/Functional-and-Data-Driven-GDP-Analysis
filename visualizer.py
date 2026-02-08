import matplotlib.pyplot as plt

def plotDashboard(analysisResult):
    """
    Creates a GDP visualization dashboard using matplotlib.
    """

    title = analysisResult["title"]
    values = analysisResult["plotData"]["values"]
    labels = analysisResult["plotData"]["labels"]
    year = analysisResult["year"]
    region = analysisResult["region"]
    resultValue = analysisResult["resultValue"]

    if not values or not labels:
        print("No data available for visualization.")
        return

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    
    plt.title(f"{title}\nResult: {resultValue:,.2f}")
    plt.xlabel("Countries")
    plt.ylabel("GDP")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()