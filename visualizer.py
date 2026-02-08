import matplotlib.pyplot as plt

# --- Style Configuration ---
plt.style.use('dark_background')
COLORS = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5']

def shorten_label(label, max_len=50):
    """
    Helper: Cuts off long names so they don't clutter the graph.
    Checks if label is a string first to avoid breaking Line Charts.
    """
    if isinstance(label, str) and len(label) > max_len:
        return label[:max_len] + "..."
    return label

def plotDashboard(result):
    graphType = result.get("graph", "bar")
    
    # Get Data
    raw_labels = result["plotData"]["labels"]
    values = result["plotData"]["values"]
    title = result["title"]

    if not raw_labels or not values:
        print("No data available.")
        return

    # Shorten labels (safe for strings only)
    labels = [shorten_label(l) for l in raw_labels]

    # Create Figure
    fig = plt.figure(figsize=(12, 7), facecolor='#1e1e1e')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#1e1e1e')

    # --- BAR CHART ---
    if graphType == "bar":
        ax.bar(labels, values, color=COLORS[:len(labels)], edgecolor='white', alpha=0.8)
        
        ax.set_ylabel("GDP (USD)", color='white', fontsize=12)
        
        if len(labels) > 10:
            font_size = 8
            rotation = 90
        else:
            font_size = 10
            rotation = 45
        
        ax.tick_params(axis='x', rotation=rotation, colors='white', labelsize=font_size)
        ax.tick_params(axis='y', colors='white')
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='gray', zorder=0)

    # --- PIE CHART ---
    elif graphType == "pie":
        total = sum(values)
        threshold = 0.01 * total # 1% Threshold
        
        main_labels = [l for l, v in zip(labels, values) if v >= threshold]
        main_values = [v for v in values if v >= threshold]
        
        others = sum([v for v in values if v < threshold])
        if others > 0:
            main_labels.append("Others")
            main_values.append(others)

        # PLOT PIE
        wedges, texts, autotexts = ax.pie(
            main_values, 
            labels=main_labels, 
            autopct='%1.1f%%', 
            startangle=140,
            colors=COLORS,
            radius=1.2, 
            center=(0, 0), 
            textprops={'color':"white"}
        )
        plt.setp(autotexts, size=10, weight="bold", color="black")

    # --- LINE CHART ---
    elif graphType == "line":
        ax.plot(labels, values, color='#00ffcc', linewidth=2, marker='o', 
                markersize=8, markerfacecolor='#ffffff', markeredgecolor='#00ffcc')
        
        ax.fill_between(labels, values, color='#00ffcc', alpha=0.1)
        
        ax.set_xlabel("Year", color='white', fontsize=12)
        ax.set_ylabel("GDP (USD)", color='white', fontsize=12)
        
        # Vertical X-Axis Labels
        ax.tick_params(axis='x', rotation=90, colors='white')
        ax.tick_params(axis='y', colors='white')
        
        ax.grid(True, linestyle=':', alpha=0.4, color='gray')

    else:
        print(f"Unknown graph type: {graphType}")
        return

    # --- STATS BOX LOGIC ---
    # Construct the string to display
    stat_text = ""
    if "resultValue" in result:
        # This comes from Region Analysis (Single Stat)
        val = result["resultValue"]
        stat_text = f"Calculated Result:\n${val:,.2f}"
    elif "stats" in result:
        # This comes from Country Trend (Dictionary of stats)
        avg = result["stats"].get("average", 0)
        tot = result["stats"].get("total", 0)
        stat_text = f"Period Average:\n${avg:,.2f}\n\nTotal Volume:\n${tot:,.2f}"

    # Draw the Text Box in Top Right Corner (if we have text)
    if stat_text:
        ax.text(0.98, 0.98, stat_text, transform=ax.transAxes,
                fontsize=11, color='#00ffcc', fontweight='bold',
                ha='right', va='top', 
                bbox=dict(boxstyle="round,pad=0.5", fc="#333333", ec="white", alpha=0.9))

    # --- Layout Polish ---
    ax.set_title(title, color='white', fontsize=16, fontweight='bold', pad=20)
    
    # Remove borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    # Adjust bottom margin
    plt.subplots_adjust(bottom=0.25)
    plt.show()
