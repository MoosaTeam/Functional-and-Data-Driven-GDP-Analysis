import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import loader
import processor
import visualizer

# Load data once
DATA = loader.loadData("gdp_with_continent_filled.csv")

# Allowed year range
MIN_YEAR = 1960
MAX_YEAR = 2024

# --- Helper: Validation Logic ---
def validateConfig(config):
    """
    Validates the structure of the uploaded JSON configuration.
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

# --- GUI ---
class GDPDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP Analysis Dashboard")
        self.root.geometry("500x550")
        self.root.resizable(True, True)

        # --- Section 1: JSON Import ---
        import_frame = ttk.LabelFrame(root, text="Batch Processing (JSON)")
        import_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(import_frame, text="Load a config.json file to run multiple analyses:").pack(pady=5)
        ttk.Button(import_frame, text="Import Config File", command=self.import_json_config).pack(pady=10)

        # --- Section 2: Manual Interactive Mode ---
        manual_frame = ttk.LabelFrame(root, text="Manual Analysis")
        manual_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(manual_frame, text="Select Analysis Type:").pack(pady=5)
        self.analysis_type = ttk.Combobox(manual_frame, values=["Region", "Country Trend"], state="readonly")
        self.analysis_type.pack()
        self.analysis_type.current(0)
        self.analysis_type.bind("<<ComboboxSelected>>", self.toggle_fields)

        # Region / Country
        self.region_label = ttk.Label(manual_frame, text="Region:")
        self.region_label.pack()
        regions = sorted(set(d['region'] for d in DATA))
        self.region_combo = ttk.Combobox(manual_frame, values=regions, state="readonly")
        self.region_combo.pack()
        self.region_combo.current(0)

        self.country_label = ttk.Label(manual_frame, text="Country:")
        self.country_entry = ttk.Entry(manual_frame)

        # Year(s)
        ttk.Label(manual_frame, text=f"Year (Region) or Start Year (Trend) [{MIN_YEAR}-{MAX_YEAR}]:").pack(pady=5)
        self.year_entry = ttk.Entry(manual_frame)
        self.year_entry.pack()

        ttk.Label(manual_frame, text=f"End Year (Trend only) [{MIN_YEAR}-{MAX_YEAR}]:").pack(pady=5)
        self.end_year_entry = ttk.Entry(manual_frame)
        self.end_year_entry.pack()

        # Operation
        ttk.Label(manual_frame, text="Operation (average, sum, max, min):").pack(pady=5)
        self.operation_entry = ttk.Entry(manual_frame)
        self.operation_entry.pack()
        self.operation_entry.insert(0, "average")

        # Graph Type
        ttk.Label(manual_frame, text="Graph Type (bar, pie, line):").pack(pady=5)
        self.graph_combo = ttk.Combobox(manual_frame, values=["bar", "pie", "line"], state="readonly")
        self.graph_combo.pack()
        self.graph_combo.current(0)

        # Button
        ttk.Button(manual_frame, text="Generate Graph", command=self.generate_graph).pack(pady=15)

        self.toggle_fields()  # initialize

    def toggle_fields(self, event=None):
        """Show/hide region or country fields based on analysis type."""
        if self.analysis_type.get() == "Region":
            self.region_label.pack()
            self.region_combo.pack()
            self.country_label.pack_forget()
            self.country_entry.pack_forget()
        else:
            self.region_label.pack_forget()
            self.region_combo.pack_forget()
            self.country_label.pack()
            self.country_entry.pack()

    def import_json_config(self):
        """Handler for the Import JSON button."""
        filename = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )

        if not filename:
            return

        try:
            with open(filename, "r") as f:
                config = json.load(f)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read JSON file:\n{e}")
            return

        if not validateConfig(config):
            messagebox.showerror("Config Error", "Invalid configuration file structure. Check console for details.")
            return

        print(f"\n--- Batch Processing: {filename} ---")

        for i, analysis in enumerate(config["analyses"]):
            print(f"\n--- Analysis #{i+1}: {analysis['type'].upper()} ---")
            
            if analysis["type"] == "region":
                result = processor.processAnalysis(DATA, analysis)
                result["graph"] = analysis.get("graph", "bar")
                
                print(f"Region: {analysis['region']}")
                print(f"Operation: {analysis['operation'].capitalize()}")
                print(f"Result: ${result['resultValue']:,.2f}")
                
                visualizer.plotDashboard(result)

            elif analysis["type"] == "country_trend":
                result = processor.processCountryTrend(
                    DATA, 
                    analysis["country"], 
                    analysis["start_year"], 
                    analysis["end_year"]
                )
                
                if result:
                    stats = result.get("stats", {})
                    print(f"Country: {analysis['country']}")
                    print(f"Average GDP ({analysis['start_year']}-{analysis['end_year']}): ${stats.get('average', 0):,.2f}")
                    
                    visualizer.plotDashboard(result)
                else:
                    print(f"Error: Country '{analysis['country']}' not found.")
        
        messagebox.showinfo("Success", "Batch processing complete. Check console for stats.")

    def generate_graph(self):
        """Generate graph from manual inputs."""
        try:
            graph_type = self.graph_combo.get()
            if graph_type not in ["bar", "pie", "line"]:
                messagebox.showerror("Invalid Graph Type", "Graph type must be 'bar', 'pie', or 'line'.")
                return

            analysis_type = self.analysis_type.get()
            print(f"\n--- Manual Analysis: {analysis_type.upper()} ---")

            # --- Region Analysis ---
            if analysis_type == "Region":
                region = self.region_combo.get()
                year_text = self.year_entry.get().strip()
                operation = self.operation_entry.get().strip().lower()

                if not year_text.isdigit():
                    messagebox.showerror("Invalid Year", "Year must be a number.")
                    return
                year = int(year_text)
                if year < MIN_YEAR or year > MAX_YEAR:
                    messagebox.showerror("Invalid Year", f"Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                    return

                if operation not in ["average", "sum", "max", "min"]:
                    messagebox.showerror("Invalid Operation", "Operation must be average, sum, max, or min.")
                    return

                config = {"region": region, "year": year, "operation": operation}
                result = processor.processAnalysis(DATA, config)
                result["graph"] = graph_type
                
                # FIX: Added Print Statements
                print(f"Region: {region}")
                print(f"Operation: {operation.capitalize()}")
                print(f"Result: ${result['resultValue']:,.2f}")
                
                visualizer.plotDashboard(result)

            # --- Country Trend Analysis ---
            else:
                country = self.country_entry.get().strip()
                start_text = self.year_entry.get().strip()
                end_text = self.end_year_entry.get().strip()

                if not start_text.isdigit():
                    messagebox.showerror("Invalid Start Year", "Start Year must be a number.")
                    return
                start_year = int(start_text)
                if start_year < MIN_YEAR or start_year > MAX_YEAR:
                    messagebox.showerror("Invalid Start Year", f"Start Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                    return

                if end_text:
                    if not end_text.isdigit():
                        messagebox.showerror("Invalid End Year", "End Year must be a number.")
                        return
                    end_year = int(end_text)
                    if end_year < MIN_YEAR or end_year > MAX_YEAR:
                        messagebox.showerror("Invalid End Year", f"End Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                        return
                else:
                    end_year = start_year

                if start_year > end_year:
                    messagebox.showerror("Invalid Year Range", "Start Year cannot be after End Year.")
                    return

                countries = [d['country'] for d in DATA]
                found_country = next((c for c in countries if c.lower() == country.lower()), None)
                
                if not found_country:
                    messagebox.showerror("Invalid Country", f"Country '{country}' not found.")
                    return

                result = processor.processCountryTrend(DATA, found_country, start_year, end_year)
                if result:
                    result["graph"] = graph_type
                    
                    # FIX: Added Print Statements
                    stats = result.get("stats", {})
                    print(f"Country: {found_country}")
                    print(f"Average GDP ({start_year}-{end_year}): ${stats.get('average', 0):,.2f}")
                    
                    visualizer.plotDashboard(result)
                else:
                    messagebox.showerror("Error", f"No data available for '{country}' in the selected years.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GDPDashboardGUI(root)
    root.mainloop()
