import pandas as pd
import folium
from folium import FeatureGroup
from branca.element import Element

def load_earthquake_data(url):
    data = pd.read_csv(url)
    data['time'] = pd.to_datetime(data['time'], utc=True)
    return data

def size_producer(magnitude):
    return magnitude * 3

def color_producer(magnitude):
    if magnitude < 2.5:
        return 'green'
    elif 2.5 <= magnitude < 5.0:
        return 'orange'
    else:
        return 'red'

def add_earthquake_markers(map, data):
    low_magnitude = FeatureGroup(name='Low Magnitude (0-2.5)')
    medium_magnitude = FeatureGroup(name='Medium Magnitude (2.5-5.0)')
    high_magnitude = FeatureGroup(name='High Magnitude (5.0+)')

    for _, earthquake in data.iterrows():
        marker = folium.CircleMarker(
            location=[earthquake['latitude'], earthquake['longitude']],
            radius=size_producer(earthquake['mag']),
            color=color_producer(earthquake['mag']),
            fill=True,
            fill_color=color_producer(earthquake['mag']),
            fill_opacity=0.7,
            popup=f"Time: {earthquake['time'].to_pydatetime().strftime('%Y-%m-%d %H:%M:%S')}\nMagnitude: {earthquake['mag']}\nDepth: {earthquake['depth']} km"
        )
        if earthquake['mag'] < 2.5:
            marker.add_to(low_magnitude)
        elif 2.5 <= earthquake['mag'] < 5.0:
            marker.add_to(medium_magnitude)
        else:
            marker.add_to(high_magnitude)

    low_magnitude.add_to(map)
    medium_magnitude.add_to(map)
    high_magnitude.add_to(map)

def add_custom_legend(map, data):

    title_html = '''
        <h2 align="center" style="font-size:22px; margin-top:20px;">
        <b>Earthquake Data</b></h2>
        <h3 align="center" style="font-size:18px; margin-bottom:20px;">
        <i>From {} to {}</i></h3>
        '''.format(data['time'].min().strftime('%Y-%m-%d'), data['time'].max().strftime('%Y-%m-%d'))
    map.get_root().html.add_child(folium.Element(title_html))

    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; left: 50px; width: 180px; height: 130px; 
        background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
        ">&nbsp; <b>Earthquake Magnitude</b> <br>
        &nbsp; <i class="fa fa-circle fa-1x" style="color:green"></i>&nbsp;0-2.5<br>
        &nbsp; <i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;2.5-5.0<br>
        &nbsp; <i class="fa fa-circle fa-1x" style="color:red"></i>&nbsp;5.0+<br>
    </div>
    '''
    map.get_root().html.add_child(folium.Element(legend_html))