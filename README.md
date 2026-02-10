### Functional-and-Data-Driven-GDP-Analysis

A fully functional, data-driven GDP analysis system built using functional programming principles, with a strong emphasis on modularity, composability, and configuration-driven analysis. The project is implemented in Python, leveraging multiple data and analysis libraries, and includes clear visualizations produced using Matplotlib to make economic trends easier to reason about.

Created by Muhammad Moosa and Syed Abdullah — two dinguses with a questionable sense of humor but a solid knack for computers and data.

# Moosa
<img width="1523" height="858" alt="image" src="https://github.com/user-attachments/assets/cee40e87-1fa6-4fe5-8e30-d0cd0de73dc3" />

# Abdullah
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/d917c426-84b9-40ab-ac21-5b94b26934e4" />


🛠 Working of the Program

This project is a configuration-driven GDP analysis system that processes historical GDP data and visualizes insights using multiple graph types. The program follows a clear pipeline-based workflow:

1. Data Loading

The dataset (gdp_with_continent_filled.csv) is loaded once using the loader.py module.

The loader reads the CSV file and converts each row into a structured dictionary.

This ensures all other modules work with clean, consistent data.

CSV File → loader.py → List of dictionaries

2. Configuration / Input Handling

The program supports two ways of controlling behavior:

a) Configuration File (config.json)

The config.json file defines one or more analyses.

Each analysis specifies:

Type of analysis (region-based or country trend)

Constraints (region, country, year, year range)

Operation (average, sum, min, max)

Graph type (bar, pie, line)

The main controller reads this file, validates it, and executes analyses sequentially.

b) Graphical User Interface (GUI)

The GUI provides an interactive way to input the same parameters.

User inputs are internally converted into config-like dictionaries, ensuring the same processing logic is reused.

This avoids code duplication and keeps the design modular.

3. Data Processing

All business logic is handled inside processor.py.

Depending on the analysis type:

Region Analysis

Filters data by region and year

Applies the selected statistical operation

Country Trend Analysis

Filters data by country and year range

Computes trend values and summary statistics

The processor returns a structured result containing:

Computed values

Labels for plotting

Metadata such as titles and statistics

This separation ensures:

No visualization logic inside data processing

No file or UI logic inside processing functions

4. Visualization & Dashboard

Visualization is handled by visualizer.py using Matplotlib.

Supported graph types:

Bar Chart – Region-wise comparisons

Pie Chart – Proportional contribution visualization

Line Chart – GDP trends over time

Each graph:

Is dynamically selected based on configuration

Includes titles, labels, grids, and styling

Gracefully handles empty or missing data

5. Error Handling & Validation

The program includes robust error handling:

Invalid or missing configuration fields are detected early

Year inputs are validated (allowed range: 1960–2024)

Start year cannot exceed end year

Invalid regions, countries, or operations trigger meaningful error messages

GUI errors are displayed using dialog boxes instead of crashing the program

🧱 Project Structure & Design

The project follows a modular and layered architecture:

├── main.py              # Entry point (config-driven execution)
├── gui_main.py          # GUI-based execution
├── loader.py            # Data loading layer
├── processor.py         # Data processing & business logic
├── visualizer.py        # Visualization & dashboard logic
├── config.json          # Configuration file
├── gdp_with_continent_filled.csv

Design Principles Used

Separation of Concerns: Each module has a single responsibility

Reusability: Same processing and visualization logic is reused by both CLI and GUI

Extensibility: New analyses or graph types can be added without modifying existing code

Configuration-Driven Behavior: Program behavior can be changed without altering source code

📌 Summary

This project demonstrates:

Configuration-driven software design

Functional-style data processing

Clean modular architecture

Multiple visualization techniques

Strong error handling and validation

The GUI acts as an optional interface layer, while the core logic remains independent, making the system flexible and easy to extend.
