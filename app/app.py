import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np

def main():
    st.title("Folium Maps with Streamlit")

    # Load sample data
    try:
        data_life = pd.read_csv('map_data_life_exp.csv')
        data_pop = pd.read_csv('map_data_population.csv')
    except FileNotFoundError:
        st.error("Data files not found. Please ensure 'map_data_life_exp.csv' and 'map_data_population.csv' are in the same directory.")
        return
    
    # Sidebar for map selection
    selected_map = st.sidebar.selectbox("Select Map", ["Life Expectancy", "Population"])

    # Display the selected map
    if selected_map == "Life Expectancy":
        display_life_expectancy(data_life)
    else:
        display_population(data_pop)

def display_life_expectancy(data_life):
    political_countries_url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    m1 = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    # Create quantiles for life expectancy
    quantiles = [0] + np.arange(0.05, 1.05, 0.05).tolist()
    bin_edges = data_life["Life Expectancy (both sexes)"].quantile(quantiles).tolist()

    tooltip_style = "background: #FFFFFF; color: #333333; font-weight: bold; padding: 5px;"

    folium.Choropleth(
        geo_data=political_countries_url,
        data=data_life,
        columns=("Country", "Life Expectancy (both sexes)"),
        key_on="feature.properties.name",
        bins=bin_edges,
        fill_color="YlGnBu",
        fill_opacity=0.8,
        line_opacity=0.8,
        nan_fill_color="white",
        legend_name="Life Expectancy (2023)",
        highlight=True,
        tooltip=folium.GeoJsonTooltip(fields=["Country", "Life Expectancy (both sexes)"],
                                       aliases=["Country", "Life Expectancy"],
                                       localize=True,
                                       style=tooltip_style)
    ).add_to(m1)

    st.subheader("Life Expectancy Map")
    folium_static(m1)

def display_population(data_pop):
    political_countries_url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    m2 = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    # Create quantiles for population
    quantiles = [0] + np.arange(0.05, 1.05, 0.05).tolist()
    bin_edges = data_pop["Population  (2023)"].quantile(quantiles).tolist()

    folium.Choropleth(
        geo_data=political_countries_url,
        data=data_pop,
        columns=("Country (or dependency)", "Population  (2023)"),
        key_on="feature.properties.name",
        bins=bin_edges,
        fill_color="viridis",
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="white",
        legend_name="World Population (2023)",
    ).add_to(m2)

    st.subheader("Population Map")
    folium_static(m2)

if __name__ == "__main__":
    main()
