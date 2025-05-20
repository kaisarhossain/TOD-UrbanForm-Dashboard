# Transit Oriented Discoveries - Urban Form Dashboard

**📌 Project Summary**

 This project focuses on the exploratory data analysis and interactive visualization of urban form typologies surrounding public transit stations in the United States. The primary aim  is to provide urban planners, transit agencies, and researchers with intuitive insights into the built environment characteristics near transit stops, supporting more informed
 decisions around land use, density, and accessibility planning.
 
 The dashboard is built using Streamlit and visualizes various spatial and structural attributes within buffer zones (200m, 400m, and 800m) around transit stations. It provides
 typology-based comparisons, visual analytics, and interactive maps for urban form interpretation.

**🎯 Project Objectives**

 Analyze urban form typologies near rail and metro stations. Compare station surroundings using parameters like:
 
 - Number of buildings
 - Average building height
 - Total building footprint

 Provide geographical insights into the typologies for different agencies, transit modes, and lines. Facilitate visual, interactive exploration through web-based dashboards.

**📁 Dataset Description**

 The dataset used contains information on transit stations and surrounding built environment statistics, with the following major components:

**Column Name	Description:**

 station_id:	Unique ID for each transit station
 
 StationName:	Name of the transit station
 
 ntd_agency:	Transit agency name
 
 ntd_mode:	Mode of transportation (e.g., Rail, Metro)
 
 line_name:	Transit line identifier
 
 latitude, longitude:	Latitude and longitude coordinates of the station
 
 Typology:	Categorization of the urban form (e.g., "Category 1 - Underbuilt")
 
 Inner_TotalBuildings	Number of buildings within 200m buffer
 
 Inner_AvgHeight	Average building height within 200m
 
 Inner_TotalFootprint	Total building footprint within 200m (in square meters)
 
 Middle_TotalBuildings	Number of buildings within 400m buffer
 
 Middle_AvgHeight	Average building height within 400m
 
 Middle_TotalFootprint	Total building footprint within 400m (in square meters)
 
 Outer_TotalBuildings	Number of buildings within 800m buffer
 
 Outer_AvgHeight	Average building height within 800m
 
 Outer_TotalFootprint	Total building footprint within 800m (in square meters)

**🛠️ Technologies Used**

 - Language: Python
 - Framework: Streamlit
 - Visualization: matplotlib, seaborn, plotly, folium, streamlit-folium, plotly-express
 - Data Handling: Pandas
 - Other Tools: Jupyter Notebook, GitHub, PyCharm

**🎨 Dashboard Tabs & Features**

  **📌 Tab 1:** Typology Relative Comparison by Geography
   
   - Purpose: Show how different urban forms relate to geography and line/mode.
   - Filters: Transit Mode, Transit Line
   - Bar Chart: Number of stations in each typology
   - Scatter Plot: Total buildings vs. footprint colored by typology
   - 3D Scatter Plot: Interactive view showing typology patterns based on: Total buildings, Avg. height, Total footprint
  
  **📌 Tab 2:** Typology Interpretation
  
   Purpose: Inform users on what typologies mean spatially and functionally.
  
   Markdown and structured documentation of each typology category:
   
   - Category 1 – Underbuilt:           Lower Building Count, Lower Footprint, Lower Height
   - Category 2 – Vertical Outliers:    Lower Building Count, Lower Footprint, Higher Height
   - Category 3 – Spread-Low Density:   Lower Building Count, Higher Footprint, Lower Height
   - Category 4 – Vertical Campuses:    Lower Building Count, Higher Footprint, Higher Height
   - Category 5 – Compact Low-Rise:     Higher Building Count, Lower Footprint, Lower Height
   - Category 6 – Compact Vertical:     Higher Building Count, Lower Footprint, Higher Height
   - Category 7 – Sprawling Mid-Density:Higher Building Count, Higher Footprint, Lower Height
   - Category 8 – Urban Core:           Higher Building Count, Higher Footprint, Higher Height
  
  **📌 Tab 3: Data Table**
  
   - Interactive dataframe view of all records
   - Users can sort, filter, and inspect station-level details
   - Purpose: Give transparency and allow detailed inspection of raw data
  
  **📌 Tab 4: Map View**
  
   Planned: Folium map to display stations with color-coded typologies and metrics.

   Hover/click tooltips to explore building density metrics per station.

**🧠 Learning Outcomes**

 - Practical experience building multi-tab, interactive dashboards using Streamlit and Plotly.
 - Gained expertise in designing geo-spatial urban analytics visualizations.
 - Improved understanding of how data storytelling and UI/UX play a role in decision-support tools.
 - Successfully applied data filtering, caching, state management, and visual storytelling techniques.

**📚 References & Acknowledgements**

 Dataset source: Schneider Analytics, Public and open dataset repository (OpenStreetMap)
 
 Visual design inspired by urban typology frameworks from urban planning literatures.

**📦 Repository & Deployment**

 - Repository: [Github_link](https://github.com/kaisarhossain/TOD-UrbanForm-Dashboard)
 - Deployment: Streamlit Community Cloud
 - Access Link: [Access_link](https://tod-urbanform-dashboard.streamlit.app/?embed_options=light_theme,show_toolbar)

