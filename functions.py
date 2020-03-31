import requests

def get_episodes(text):
    episodes = []
    results = requests.get("https://rickandmortyapi.com/api/episode/?name="+text).json()
    if("error" not in results.keys()):
        pages = int(results["info"]["pages"])
        print(pages)
        episodes_query = "https://rickandmortyapi.com/api/episode/?name="+text+"&page="
        print(episodes_query)
        for i in range(pages):
            print(i)
            query = episodes_query + str(i+1)
            print(query)
            episodes_result = requests.get(query).json()["results"]
            episodes += episodes_result
    return episodes

def get_characters(text):
    characters = []
    results = requests.get("https://rickandmortyapi.com/api/character/?name="+text).json()
    if("error" not in results.keys()):
        pages = int(results["info"]["pages"])
        characters_query = "https://rickandmortyapi.com/api/character/?name="+text+"&page="
        for i in range(pages):
            query = characters_query + str(i+1)
            characters_results = requests.get(query).json()["results"]
            characters += characters_results
    return characters

def get_locations(text):
    locations = []
    results = requests.get("https://rickandmortyapi.com/api/location/?name="+text).json()
    if("error" not in results.keys()):
        pages = int(results["info"]["pages"])
        locations_query = "https://rickandmortyapi.com/api/location/?name="+text+"&page="
        for i in range(pages):
            query = locations_query + str(i+1)
            locations_results = requests.get(query).json()["results"]
            locations += locations_results
    return locations
