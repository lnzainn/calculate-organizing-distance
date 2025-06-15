import pandas as pd
import geopandas as gpd
from geopy.distance import geodesic

wca = pd.read_csv("wca_countries/WCA_export_Countries.tsv", sep="\t")

world = gpd.read_file("online_countries/ne_110m_admin_0_countries.shp")
world = world.to_crs(epsg=3857)
world['centroid'] = world.geometry.centroid
centroids = world['centroid'].to_crs(epsg=4326)
world['latitude'] = centroids.y
world['longitude'] = centroids.x
world_coords = world[['ADMIN', 'ISO_A3', 'latitude', 'longitude']].copy()
world_coords.columns = ['country_name', 'iso3', 'latitude', 'longitude']

shp_to_wca_name_map = {
    "United States of America": "USA",
    "South Korea": "Korea",
    "North Korea": "Korea",
    "Ivory Coast": "Cote d_Ivoire",
    "Czechia": "Czech Republic",
    "Republic of the Congo": "Congo",
    "Republic of Serbia": "Serbia",
}

world_coords['country_name'] = world_coords['country_name'].replace(shp_to_wca_name_map)

merged = pd.merge(wca, world_coords, left_on='name', right_on='country_name', how='left')


manual_coords = {
    "Andorra": (42.5078, 1.5211),
    "Bahrain": (26.0667, 50.5577),
    "Barbados": (13.1939, -59.5432),
    "Cote d_Ivoire": (7.5400, -5.5471),
    "Czech Republic": (49.8175, 15.4730),
    "Hong Kong": (22.3193, 114.1694),
    "Korea": (36.5, 127.8),  # Midpoint between North and South Korea
    "Liechtenstein": (47.1660, 9.5554),
    "Macau": (22.1987, 113.5439),
    "Malta": (35.8997, 14.5146),
    "Mauritius": (-20.3484, 57.5522),
    "San Marino": (43.9333, 12.4500),
    "Serbia": (44.0165, 21.0059),
    "Singapore": (1.3521, 103.8198),
    "USA": (39.8283, -98.5795),  
}

for country, (lat, lon) in manual_coords.items():
    idx = merged[merged['id'] == country].index
    if not idx.empty:
        if pd.isna(merged.loc[idx[0], 'latitude']):
            merged.loc[idx[0], 'latitude'] = lat
            merged.loc[idx[0], 'longitude'] = lon


wca_coord_dict = {
    row['id']: (row['latitude'], row['longitude'])
    for _, row in merged.iterrows()
    if not pd.isna(row['latitude']) and not pd.isna(row['longitude'])
}

df = pd.read_csv("highest_distance.csv")  


def compute_distance(row):
    home = row['home_country']         
    comp = row['competition_country']  
    if home in wca_coord_dict and comp in wca_coord_dict:
        return geodesic(wca_coord_dict[home], wca_coord_dict[comp]).kilometers
    return None

df['distance_km'] = df.apply(compute_distance, axis=1)

df = df.sort_values(by='distance_km', ascending=False)
df.to_csv("wca_organizers_by_distance.csv", index=False)
