from flask import Flask, render_template, request
import requests
from functions import get_episodes, get_characters, get_locations

app = Flask(__name__)

@app.route("/")
def episodes():
    # busco los episodios en la página (hay solo 2 páginas en total)
    query1 = f"https://integracion-rick-morty-api.herokuapp.com/api/episode/?page=1"
    query2 = f"https://integracion-rick-morty-api.herokuapp.com/api/episode/?page=2"
    data1 = requests.get(query1)
    data2 = requests.get(query2)
    results = data1.json()["results"]
    results += requests.get(query2).json()["results"]
    return render_template('episodes.html', episodes = results)

@app.route("/search", methods = ['POST'])
def search():
    print("searching")
    text = request.form["text"]

    # busco los episodios que hagan match
    episodes = get_episodes(text)
    characters = get_characters(text)
    locations = get_locations(text)

    return render_template('search.html', text = text, episodes = episodes, characters = characters, locations = locations)

@app.route("/episode/<int:id>")
def episode(id):
    # busco el episodio
    episode_query = f"https://integracion-rick-morty-api.herokuapp.com/api/episode/{id}".format(id=id)
    data = requests.get(episode_query)
    episode = data.json()

    # obtengo los ids de los que actúan en el episodio
    characters_ids = ""
    for character in episode["characters"]:
        characters_ids += character.split("/")[-1] + ","

    # busco los personajes
    character_query = f"https://integracion-rick-morty-api.herokuapp.com/api/character/{characters_ids}".format(characters_ids=characters_ids[:-1])
    data = requests.get(character_query)
    characters = data.json()

    return render_template('episode.html', episode = episode, characters = characters)

@app.route("/character/<int:id>")
def character(id):

    # busco el personaje
    character_query = f"https://integracion-rick-morty-api.herokuapp.com/api/character/{id}".format(id = id)
    data_character = requests.get(character_query)
    character = data_character.json()

    # busco los episodios donde actúa
    episodes_ids = ""
    for episode in character["episode"]:
        episodes_ids += episode.split("/")[-1] + ","

    episodes_query = f"https://integracion-rick-morty-api.herokuapp.com/api/episode/{episodes_ids}".format(episodes_ids = episodes_ids[:-1])
    data = requests.get(episodes_query)
    episodes = data.json()

    # si tiene location la busco si no retorno unknown
    if(character["location"]["name"] != "unknown"):
        location_id = character["location"]["url"].split("/")[-1]
        location_query = f"https://integracion-rick-morty-api.herokuapp.com/api/location/{location_id}".format(locations_ids = location_id)
        data = requests.get(location_query)
        location = data.json()
    else:
        location = "unknown"

    return render_template('character.html', character = character, episodes = episodes, location = location)

@app.route("/location/<int:id>")
def location(id):
    # busco la locación
    location_query = f"https://integracion-rick-morty-api.herokuapp.com/api/location/{id}".format(id = id)
    location_data = requests.get(location_query)
    location = location_data.json()

    # busco los ids de sus residentes
    residents_ids = ""
    for resident in location["residents"]:
        residents_ids += resident.split("/")[-1] + ","

    # busco a los residentes
    residents_query = f"https://integracion-rick-morty-api.herokuapp.com/api/character/{residents_ids}".format(residents_ids=residents_ids[:-1])
    data = requests.get(residents_query)
    residents = data.json()

    return render_template('location.html', location = location, residents = residents)
