import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

def get_country_latitude_longitude(country_name):
    """
    Get the latitude and longitude of a given country using its name.
    
    Args:
        country_name (str): The name of the country.
        
    Returns:
        latitude (float): Latitude of the country.
        longitude (float): Longitude of the country.
    """
    geolocator = Nominatim(user_agent="my_geocoder")

    try:
        location = geolocator.geocode(country_name, exactly_one=True)
        if location:
            return location.latitude, location.longitude
        else:
            return np.NaN, np.NaN
    except Exception as e:
        print("Error:", e)
        return np.NaN, np.NaN

def main():
    # Load life expectancy data from the website
    life_expectancy_url = 'https://www.worldometers.info/demographics/life-expectancy/'
    table_life = pd.read_html(life_expectancy_url)

    # Load population data from the website
    population_url = 'https://www.worldometers.info/world-population/population-by-country/'
    table_pop = pd.read_html(population_url)

    # Add latitude and longitude columns using geocoding
    table_life[0]['Latitude'], table_life[0]['Longitude'] = zip(*table_life[0]['Country'].apply(get_country_latitude_longitude))
    table_pop[0]['Latitude'], table_pop[0]['Longitude'] = zip(*table_pop[0]['Country (or dependency)'].apply(get_country_latitude_longitude))

    # Save data to CSV files
    table_life[0].to_csv('data/map_data_life_exp.csv', index=False)
    table_pop[0].to_csv('data/map_data_population.csv', index=False)

if __name__ == "__main__":
    main()
