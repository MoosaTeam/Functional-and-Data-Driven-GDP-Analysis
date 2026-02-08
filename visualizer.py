import matplotlib.pyplot as plt

def plotDashboard(result):
    graphType = result.get("graph", "bar")
    labels = result["plotData"]["labels"]
    values = result["plotData"]["values"]
    title = result["title"]

    if not labels or not values:
        print("No data available for visualization.")
        return

    plt.figure(figsize=(10, 6))

    if graphType == "bar":
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("GDP")

    elif graphType == "pie":
        plt.pie(values, labels=labels, autopct='%1.1f%%')
    
    elif graphType == "line":
        plt.plot(labels, values, marker='o')
        plt.xlabel("Year")
        plt.ylabel("GDP")

    else:
        print(f"Unknown graph type: {graphType}")
        return

    plt.title(title)
    plt.tight_layout()
    plt.show()
