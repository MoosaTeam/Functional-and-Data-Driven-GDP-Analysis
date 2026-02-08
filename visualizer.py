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
        plt.bar(labels, values, color='skyblue', edgecolor='black')
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("GDP (USD)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

    elif graphType == "pie":
        # --- Logic to Group Small Slices (< 5%) ---
        total_gdp = sum(values)
        threshold = 0.05 * total_gdp  # 5% Threshold

        # 1. Keep slices larger than 5% (Functional: List Comprehension)
        main_labels = [l for l, v in zip(labels, values) if v >= threshold]
        main_values = [v for v in values if v >= threshold]

        # 2. Sum up the small slices
        others_value = sum(v for v in values if v < threshold)

        # 3. Add "Others" if necessary
        if others_value > 0:
            main_labels.append("Others")
            main_values.append(others_value)

        # 4. Plot
        plt.pie(main_values, labels=main_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Ensures pie is drawn as a circle

    elif graphType == "line":
        plt.plot(labels, values, marker='o', linestyle='-', color='green')
        plt.xlabel("Year")
        plt.ylabel("GDP (USD)")
        plt.grid(True)

    else:
        print(f"Unknown graph type: {graphType}")
        return

    plt.title(title)
    plt.tight_layout()
    plt.show()
