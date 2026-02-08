import tkinter as tk
from tkinter import ttk, messagebox
import loader
import processor
import visualizer

# Load data once
DATA = loader.loadData("gdp_with_continent_filled.csv")

# Allowed year range
MIN_YEAR = 1960
MAX_YEAR = 2024

# --- GUI ---
class GDPDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GDP Analysis Dashboard")
        self.root.geometry("500x450")
        self.root.resizable(True, True)

        # --- Widgets ---
        ttk.Label(root, text="Select Analysis Type:").pack(pady=5)
        self.analysis_type = ttk.Combobox(root, values=["Region", "Country Trend"], state="readonly")
        self.analysis_type.pack()
        self.analysis_type.current(0)
        self.analysis_type.bind("<<ComboboxSelected>>", self.toggle_fields)

        # Region / Country
        self.region_label = ttk.Label(root, text="Region:")
        self.region_label.pack()
        regions = sorted(set(d['region'] for d in DATA))
        self.region_combo = ttk.Combobox(root, values=regions, state="readonly")
        self.region_combo.pack()
        self.region_combo.current(0)

        self.country_label = ttk.Label(root, text="Country:")
        self.country_entry = ttk.Entry(root)

        # Year(s)
        ttk.Label(root, text=f"Year (for Region) or Start Year (for Country Trend) [{MIN_YEAR}-{MAX_YEAR}]:").pack(pady=5)
        self.year_entry = ttk.Entry(root)
        self.year_entry.pack()

        ttk.Label(root, text=f"End Year (for Country Trend, optional) [{MIN_YEAR}-{MAX_YEAR}]:").pack(pady=5)
        self.end_year_entry = ttk.Entry(root)
        self.end_year_entry.pack()

        # Operation
        ttk.Label(root, text="Operation (average, sum, max, min):").pack(pady=5)
        self.operation_entry = ttk.Entry(root)
        self.operation_entry.pack()
        self.operation_entry.insert(0, "average")

        # Graph Type
        ttk.Label(root, text="Graph Type (bar, pie, line):").pack(pady=5)
        self.graph_combo = ttk.Combobox(root, values=["bar", "pie", "line"], state="readonly")
        self.graph_combo.pack()
        self.graph_combo.current(0)

        # Button
        ttk.Button(root, text="Generate Graph", command=self.generate_graph).pack(pady=15)

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

    def generate_graph(self):
        """Generate graph with input validation."""
        try:
            graph_type = self.graph_combo.get()
            if graph_type not in ["bar", "pie", "line"]:
                messagebox.showerror("Invalid Graph Type", "Graph type must be 'bar', 'pie', or 'line'.")
                return

            analysis_type = self.analysis_type.get()

            # --- Region Analysis ---
            if analysis_type == "Region":
                region = self.region_combo.get()
                year_text = self.year_entry.get().strip()
                operation = self.operation_entry.get().strip().lower()

                # Validate year
                if not year_text.isdigit():
                    messagebox.showerror("Invalid Year", "Year must be a number.")
                    return
                year = int(year_text)
                if year < MIN_YEAR or year > MAX_YEAR:
                    messagebox.showerror("Invalid Year", f"Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                    return

                # Validate operation
                if operation not in ["average", "sum", "max", "min"]:
                    messagebox.showerror("Invalid Operation", "Operation must be average, sum, max, or min.")
                    return

                config = {"region": region, "year": year, "operation": operation}
                result = processor.processAnalysis(DATA, config)
                result["graph"] = graph_type
                visualizer.plotDashboard(result)

            # --- Country Trend Analysis ---
            else:
                country = self.country_entry.get().strip()
                start_text = self.year_entry.get().strip()
                end_text = self.end_year_entry.get().strip()

                # Validate start year
                if not start_text.isdigit():
                    messagebox.showerror("Invalid Start Year", "Start Year must be a number.")
                    return
                start_year = int(start_text)
                if start_year < MIN_YEAR or start_year > MAX_YEAR:
                    messagebox.showerror("Invalid Start Year", f"Start Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                    return

                # Validate end year (optional)
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

                # Validate country exists
                countries = [d['country'] for d in DATA]
                if country not in countries:
                    messagebox.showerror("Invalid Country", f"Country '{country}' not found.")
                    return

                result = processor.processCountryTrend(DATA, country, start_year, end_year)
                if result:
                    result["graph"] = graph_type
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
