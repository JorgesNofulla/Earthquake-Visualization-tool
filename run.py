import folium
from folium import LayerControl
from folium.plugins import HeatMap
import utilities

# URL for earthquake data
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.csv"

# Load earthquake data
data = utilities.load_earthquake_data(url)

# Create a base map
map = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)

# Add tile layers

folium.TileLayer('CartoDB positron', name='CartoDB Map').add_to(map)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri World Imagery',
    overlay=False,
    control=True
).add_to(map)

folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attr='CartoDB',
    name='CartoDB Dark Matter',
    overlay=False,
    control=True
).add_to(map)

# Add HeatMap layer
heatmap_data = data[['latitude', 'longitude', 'mag']].values.tolist()
HeatMap(heatmap_data).add_to(map)

# Add earthquake markers
utilities.add_earthquake_markers(map, data)

# Add layer control
LayerControl().add_to(map)

# Add legend
utilities.add_custom_legend(map, data)

# Save and display the map
map.save("enhanced_earthquakes_map_with_layers_and_backgrounds.html")
