import geopandas as gpd


world = gpd.read_file("online_countries/ne_110m_admin_0_countries.shp")

world['centroid'] = world.geometry.centroid
world['latitude'] = world.centroid.y
world['longitude'] = world.centroid.x

country_coords_df = world[['ADMIN', 'ISO_A3', 'latitude', 'longitude']]
country_coords_df.columns = ['country', 'iso3', 'latitude', 'longitude']

country_coords_df.to_csv("country_coordinates.csv", index=False)
