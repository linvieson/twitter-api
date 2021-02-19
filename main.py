'''
This module is a web-app that creates a map with locations of twitter
followers of a user marked on the map.
'''

import requests
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from flask import Flask, render_template, request

app = Flask(__name__)

def get_followers(username: str, bearer_token: str) -> dict:
    """
    Send a get request on a server, get user's followers' locations.
    """
    base_url = "https://api.twitter.com/"
    search_url = f'{base_url}1.1/friends/list.json'
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    params = {
        'screen_name': username,
        'count':  20
    }
    response = requests.get(search_url, headers = headers, params = params)
    return response.json()


def get_locations(data: dict) -> list:
    """
    Get users' locations from the dictionary. Return list of lists, every one
    of which contains user's nickname and location.
    >>> get_locations({'users': [{'screen_name': 'Alina', 'location':\
 'Lviv, Ukraine'}]})
    [['Alina', 'Lviv, Ukraine']]
    """
    result = []
    users = data['users']
    for user in users:
        name = user['screen_name']
        location = user['location']
        result.append([name, location])
    return result


def get_coordinates(data: str) -> list:
    '''
    Replace locations with their coordinates in latitude and longitude.
    Return coordinates as a tuple. If coordinates are not found, return (0, 0).
    >>> get_coordinates('California')
    (36.7014631, -118.755997)
    >>> get_coordinates('Lviv, Ukraine')
    (49.841952, 24.0315921)
    '''
    try:
        geolocator = Nominatim(user_agent='alina').geocode(data)
        return (geolocator.latitude, geolocator.longitude)
    except (AttributeError, GeocoderUnavailable):
        return (0, 0)


def build_map(data: list):
    '''
    Generate an html map, where the locations of the friends of the user are
    displayed as markers. Save the map to the "friends.html" file.
    '''
    map = folium.Map(location = (36.870190, -29.421995), zoom_start=3)
    fg_map = folium.FeatureGroup(name = 'Friends\' locations')

    for name, location in data:
        fg_map.add_child(folium.Marker(location = location,
                                       popup = name,
                                       icon=folium.Icon(color = 'cadetblue')))

    map.add_child(fg_map)
    map.add_child(folium.LayerControl())
    map.save('templates/friends.html')


def main(name: str, token: str):
    '''
    The main function that runs the module.
    '''
    json_data = get_followers(name, token)
    locations = get_locations(json_data)

    for index, elem in enumerate(locations):
        locations[index][1] = get_coordinates(elem[1])

    locations = [loc for loc in locations if (0, 0) not in loc]
    build_map(locations)


@app.route('/')
def index():
    '''
    Generates first web page of the web application.
    '''
    return render_template('index.html')


@app.route('/register', methods = ['POST'])
def register():
    '''
    Takes input from the user and navigates him or her to the next web pages,
    accordingly to the entered data. If both name and token are valid, a map
    is generated, else the web page with the message of failure is generated.
    '''
    name = request.form.get('name')
    token = request.form.get('token')
    if not name or not token:
        return render_template('failure.html')
    main(request.form.get('name'), request.form.get('token'))
    return render_template('friends.html')


if __name__ == '__main__':
    app.run(debug = False)
