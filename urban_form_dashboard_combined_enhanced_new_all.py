import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import plotly.express as px
from streamlit import session_state as ss

st.set_page_config(page_title="Transit Oriented Discoveries: Dashboard", layout="wide")
st.title("Transit Oriented Discoveries: Dashboard")


# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Final_Heighttest_with_footprints_output_typology.csv")


df = load_data()
df_copy = df.copy()

# Filter only Classic TOD, Donut, Monoculture, and Other
typology_categories = ['Classic', 'Donut', 'Monoculture', 'Other']
df = df[df['Typology'].isin(typology_categories)]

# Define app layout with tabs
tabs = st.tabs([
    "Urban Form Analysis: Geographical Comparison",
    "Typology Analysis: Median-value Comparison",
    "Typology Analysis: Transit Mode",
    "Map View"
])


# --- Tab 1 ---
with tabs[0]:
    st.title("Urban Form Relative Comparison based on Geographies: Typology Analysis")

    # Sidebar Filters
    # st.sidebar.title("Filter Options (Tab 1)")
    lines = df['line_name'].dropna().unique().tolist()
    transit_modes = df['ntd_mode'].dropna().unique().tolist()

    # selected_mode = st.sidebar.selectbox("Select Transit Mode", ["All"] + transit_modes, key="mode1")
    # selected_line = st.sidebar.selectbox("Select Lines", ["All"] + lines, key="line1")

    selected_mode = st.selectbox("Select Transit Mode", ["All"] + transit_modes, key="mode1")
    selected_line = st.selectbox("Select Lines", ["All"] + lines, key="line1")

    # Apply filters
    filtered_df = df.copy()
    if selected_line != "All":
        filtered_df = filtered_df[filtered_df['line_name'] == selected_line]
    if selected_mode != "All":
        filtered_df = filtered_df[filtered_df['ntd_mode'] == selected_mode]

    st.markdown("""
    This dashboard explores how building height, footprint, and count change with distance from transit stations (200m, 400m, 800m).
    Typologies include:
    - **Classic TOD**: Taller, denser, and fewer buildings near the station.
    - **The Donut**: Irregular patterns.
    - **Monoculture**: Uniform form across all distances.
    - **Other**: Need to be defined.
    """)

    # --- Count by Typology ---
    st.subheader("Station Count per Urban Form Typology")
    typology_summary = filtered_df['Typology'].value_counts().reset_index()
    typology_summary.columns = ['Urban Form Typology', 'Station Count']
    fig_bar = px.bar(typology_summary, x='Urban Form Typology', y='Station Count', color='Urban Form Typology',
                     text='Station Count')
    st.plotly_chart(fig_bar)

    # --- 2D Scatter Plot ---
    st.subheader("2D Scatter Plot of Station Characteristics")
    fig_scatter = px.scatter(filtered_df,
                             x='Outer_TotalBuildings',
                             y='Outer_TotalFootprint',
                             color='Typology',
                             symbol='ntd_mode',
                             hover_name='StationName')
    st.plotly_chart(fig_scatter)

    # --- 3D Scatter Plot ---
    st.subheader("3D Interactive Plot of Buildings, Footprint, and Height")
    fig_3d = px.scatter_3d(filtered_df,
                           x='Outer_TotalBuildings',
                           y='Outer_TotalFootprint',
                           z='Outer_AvgHeight',
                           color='Typology',
                           symbol='ntd_mode',
                           hover_name='StationName')
    st.plotly_chart(fig_3d)

    # --- Table View ---
    st.subheader("Filtered Data Table")
    st.dataframe(filtered_df[['StationName', 'line_name', 'ntd_mode', 'Typology',
                              'Inner_AvgHeight', 'Middle_AvgHeight', 'Outer_AvgHeight',
                              'Inner_TotalFootprint', 'Middle_TotalFootprint', 'Outer_TotalFootprint',
                              'Inner_TotalBuildings', 'Middle_TotalBuildings', 'Outer_TotalBuildings']])

# --- Tab 2 ---
with tabs[1]:
    st.title("Urban Form Within 800m of Transit Stations")
    st.markdown("""
    This tab analyzes urban typologies near stations using building count, footprint, and height.
    Dividing stations into eight (8) distinct urban form categories:
    - **Category 1 – Underbuilt**: Lower buildings, lower footprint, lower height. These station areas are underutilized, typically with few small, low-rise structures. This may reflect zoning constraints, disinvestment, or undeveloped land.
    - **Category 2 – Vertical Outliers**: Lower number of buildings, lower footprint, higher height. Stations are mostly single-use vertical developments like hospitals, universities, or legacy towers surrounded by open space or parking.
    - **Category 3 – Spread-Low Density**: Lower number of buildings, higher footprint, lower height. Often associated with big-box retail, surface parking, or single-story industrial uses. The land is used inefficiently in a high-value location.
    - **Category 4 – Vertical Campuses**: Lower number of buildings, higher footprint, higher height. This form suggests institutional or corporate campuses with tall, bulky buildings and limited surrounding density.
    - **Category 5 – Compact Low-Rise**: Higher number of buildings, lower footprint, lower height. Dense clusters of small-scale, fine-grain structures, often historic or neighborhood-serving.
    - **Category 6 – Compact Vertical**: Higher number of buildings, lower footprint, higher height. A pattern consistent with high-rise TOD or Asian-style TOD nodes — efficient land use with walkable density.
    - **Category 7 – Sprawling Mid-Density**: Higher number of buildings, higher footprint, lower height. Horizontal spread of 1–3 story structures — light industrial, aging commercial, or suburban TOD with limited vertical investment.
    - **Category 8 – Urban Core**: Higher number of buildings, higher footprint, higher height. These are fully built-out urban cores — dense, tall, and walkable, often with high land values and demand.
    """)

    df1 = df_copy[['Outer_TotalBuildings', 'Outer_TotalFootprint', 'Outer_AvgHeight']].dropna()
    median_buildings = df1['Outer_TotalBuildings'].median()
    median_footprint = df1['Outer_TotalFootprint'].median()
    median_height = df1['Outer_AvgHeight'].median()

    def categorize(row):
        b = row['Outer_TotalBuildings'] > median_buildings
        f = row['Outer_TotalFootprint'] > median_footprint
        h = row['Outer_AvgHeight'] > median_height
        return f"{'Higher' if b else 'Lower'} Building Count, {'Higher' if f else 'Lower'} Footprint, {'Higher' if h else 'Lower'} Height"

    df1['Category'] = df1.apply(categorize, axis=1)

    mapping_dict = {
        'Lower Building Count, Lower Footprint, Lower Height': 'Category 1 – Underbuilt',
        'Lower Building Count, Lower Footprint, Higher Height': 'Category 2 – Vertical Outliers',
        'Lower Building Count, Higher Footprint, Lower Height': 'Category 3 – Spread-Low Density',
        'Lower Building Count, Higher Footprint, Higher Height': 'Category 4 – Vertical Campuses',
        'Higher Building Count, Lower Footprint, Lower Height': 'Category 5 – Compact Low-Rise',
        'Higher Building Count, Lower Footprint, Higher Height': 'Category 6 – Compact Vertical',
        'Higher Building Count, Higher Footprint, Lower Height': 'Category 7 – Sprawling Mid-Density',
        'Higher Building Count, Higher Footprint, Higher Height': 'Category 8 – Urban Core'
    }

    df1['Category'] = df1['Category'].map(mapping_dict)

    colors = sns.color_palette("Set2", df1['Category'].nunique())
    category_colors = dict(zip(df1['Category'].unique(), colors))

    ### Urban Form Typology with Median References: Station Count per Urban Form Typology Analysis
    st.subheader("Urban Form Typology with Median References: Station Count per Typology")
    summary = df1['Category'].value_counts().reset_index()
    summary.columns = ['Urban Form Around Transit Stations Typology', 'Station Count']
    st.dataframe(summary)
    summary.to_csv('Urban Form Typology with Median References-Station Count per Typology.csv', index=False)
    # Download CSV option
    csv = summary.reset_index().to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "Urban Form Typology with Median References-Station Count per Typology.csv", "text/csv")

    ### Urban Form Typology with Median References: Pairwise 2D Quadrant Plots
    st.subheader("Urban Form Typology with Median References: 2D Quadrant Plots")
    scatter_options = ["Buildings vs Height", "Buildings vs Footprint", "Footprint vs Height"]
    selected_scatter = st.selectbox("Select 2D plot", scatter_options)

    fig, ax = plt.subplots(figsize=(10, 6))
    if selected_scatter == "Buildings vs Height":
        sns.scatterplot(data=df1, x='Outer_TotalBuildings', y='Outer_AvgHeight', hue='Category',
                        palette=category_colors, ax=ax)
        ax.axvline(median_buildings, color='gray', linestyle='--')
        ax.axhline(median_height, color='gray', linestyle='--')
        ax.set_title('Building Count vs Building Avg Height')
        ax.set_xlabel('Total Buildings')
        ax.set_ylabel('Average Height')
    elif selected_scatter == "Buildings vs Footprint":
        sns.scatterplot(data=df1, x='Outer_TotalBuildings', y='Outer_TotalFootprint', hue='Category',
                        palette=category_colors, ax=ax)
        ax.axvline(median_buildings, color='gray', linestyle='--')
        ax.axhline(median_footprint, color='gray', linestyle='--')
        ax.set_title('Building Count vs Building Footprint')
        ax.set_xlabel('Total Buildings')
        ax.set_ylabel('Total Footprint')
    elif selected_scatter == "Footprint vs Height":
        sns.scatterplot(data=df1, x='Outer_TotalFootprint', y='Outer_AvgHeight', hue='Category',
                        palette=category_colors, ax=ax)
        ax.axvline(median_footprint, color='gray', linestyle='--')
        ax.axhline(median_height, color='gray', linestyle='--')
        ax.set_title('Building Footprint vs Building Height')
        ax.set_xlabel('Total Footprint')
        ax.set_ylabel('Average Height')
    st.pyplot(fig)

    st.subheader("Urban Form Typology: 3D View")
    df1['CategoryCode'] = df1['Category'].astype('category').cat.codes.astype(int)
    scatter3d = go.Scatter3d(
        x=df1['Outer_TotalBuildings'],
        y=df1['Outer_TotalFootprint'],
        z=df1['Outer_AvgHeight'],
        mode='markers',
        marker=dict(
            size=5,
            color=df1['CategoryCode'],
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title='Category Code')
        ),
        text=df1.get('StationName', None),
        hovertemplate="<b>%{text}</b><br>Buildings: %{x}<br>Footprint: %{y}<br>Height: %{z}<extra></extra>"
    )

    fig3d = go.Figure(data=[scatter3d])
    fig3d.update_layout(
        scene=dict(
            xaxis_title='Total Buildings',
            yaxis_title='Total Footprint',
            zaxis_title='Average Height'
        ),
        # title='3D Urban Form Typology',
        height=700
    )
    st.plotly_chart(fig3d, use_container_width=True)



# --- Tab 3 ---
with tabs[2]:
    st.title("Urban Form Typology by Transit Mode")
    df2 = df_copy[['Outer_TotalBuildings', 'Outer_TotalFootprint', 'Outer_AvgHeight', 'ntd_mode']].dropna()

    # Compute national medians
    median_buildings = df2['Outer_TotalBuildings'].median()
    median_footprint = df2['Outer_TotalFootprint'].median()
    median_height = df2['Outer_AvgHeight'].median()

    # Create category labels for each octant
    def categorize(row):
        b = row['Outer_TotalBuildings'] > median_buildings
        f = row['Outer_TotalFootprint'] > median_footprint
        h = row['Outer_AvgHeight'] > median_height
        return f"{'Higher' if b else 'Lower'} Building Count, {'Higher' if f else 'Lower'} Footprint, {'Higher' if h else 'Lower'} Height"


    df2['Category'] = df2.apply(categorize, axis=1)

    # Create a dictionary to map old values to new values
    mapping_dict = {
        'Lower Building Count, Lower Footprint, Lower Height': 'Category 1 – Underbuilt',
        'Lower Building Count, Lower Footprint, Higher Height': 'Category 2 – Vertical Outliers',
        'Lower Building Count, Higher Footprint, Lower Height': 'Category 3 – Spread-Low Density',
        'Lower Building Count, Higher Footprint, Higher Height': 'Category 4 – Vertical Campuses',
        'Higher Building Count, Lower Footprint, Lower Height': 'Category 5 – Compact Low-Rise',
        'Higher Building Count, Lower Footprint, Higher Height': 'Category 6 – Compact Vertical',
        'Higher Building Count, Higher Footprint, Lower Height': 'Category 7 – Sprawling Mid-Density',
        'Higher Building Count, Higher Footprint, Higher Height': 'Category 8 – Urban Core'
    }

    # Rename the values in the 'Category' column using the mapping dictionary
    df2['Category'] = df2['Category'].map(mapping_dict)

    # 2D Scatter Plot with Dropdown for Axis Selection
    st.subheader("Urban Form by Transit Mode: 2D Scatter Plots")

    scatter_options = ["Buildings vs Height", "Buildings vs Footprint", "Footprint vs Height"]
    selected_scatter = st.selectbox("Select 2D plot", scatter_options, key="transit_mode_scatter_tab_2")

    # Define dynamic axes and medians based on selected plot
    if selected_scatter == "Buildings vs Height":
        x_col = 'Outer_TotalBuildings'
        y_col = 'Outer_AvgHeight'
        x_label = 'Number of Buildings (Outer_TotalBuildings)'
        y_label = 'Building Average Height (Outer_AvgHeight)'
        x_median = median_buildings
        y_median = median_height
    elif selected_scatter == "Buildings vs Footprint":
        x_col = 'Outer_TotalBuildings'
        y_col = 'Outer_TotalFootprint'
        x_label = 'Number of Buildings (Outer_TotalBuildings)'
        y_label = 'Building Square Footage (Outer_TotalFootprint)'
        x_median = median_buildings
        y_median = median_footprint
    elif selected_scatter == "Footprint vs Height":
        x_col = 'Outer_TotalFootprint'
        y_col = 'Outer_AvgHeight'
        x_label = 'Building Square Footage (Outer_TotalFootprint)'
        y_label = 'Building Average Height (Outer_AvgHeight)'
        x_median = median_footprint
        y_median = median_height

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(
        data=df2,
        x=x_col,
        y=y_col,
        hue='ntd_mode',
        palette='Set2',
        s=100,
        alpha=0.8,
        ax=ax
    )
    ax.axvline(x_median, color='gray', linestyle='--', linewidth=1.5, label='Median (X)')
    ax.axhline(y_median, color='gray', linestyle='--', linewidth=1.5, label='Median (Y)')

    ax.set_title(f'Urban Form by Transit Mode: {x_label.split("(")[0]} vs {y_label.split("(")[0]}')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)
    ax.legend(title='Transit Mode')
    st.pyplot(fig)

    # Station Count per Category and Transit Mode
    st.subheader("Station Count per Urban Form Typology and Transit Mode")
    summary_by_mode = df2.groupby(['ntd_mode', 'Category']).size().reset_index(name='Station Count')

    pivot_summary = summary_by_mode.pivot(index='ntd_mode', columns='Category', values='Station Count').fillna(
        0).astype(int)

    # Display the pivot table
    st.dataframe(pivot_summary, use_container_width=True)

    # Download CSV option
    csv = pivot_summary.reset_index().to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "Urban_Form_Typology_Summary.csv", "text/csv")

# --- Tab 4 ---
with tabs[3]:
    st.title("Transit Stations & Urban Form Metrics")

    if {'Latitude', 'Longitude'}.issubset(df.columns):
        map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
        m = folium.Map(location=map_center, zoom_start=11, tiles='CartoDB positron')

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='blue',
                fill=True,
                fill_opacity=0.7,
                popup=(f"<b>{row.get('StationName', 'N/A')}</b><br>"
                       f"Buildings: {row.get('Outer_TotalBuildings', 'N/A')}<br>"
                       f"Footprint: {row.get('Outer_TotalFootprint', 'N/A')}<br>"
                       f"Height: {row.get('Outer_AvgHeight', 'N/A')}")
            ).add_to(m)

        st_folium(m, width=1000, height=600)
    else:
        st.warning("Latitude and Longitude columns not found in dataset. Please ensure they are included for map view.")

st.markdown("---")
st.markdown(
    "Analysis & dashboard designed by: Mohammed Golam Kaisar Hossain Bhuyan | GitHub: https://kaisarhossain.github.io/portfolio/")
