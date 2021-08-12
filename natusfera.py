#!/usr/bin/env python3
from typing import List, Union
import requests
from bs4 import BeautifulSoup
import datetime

API_URL = "https://natusfera.gbif.es"

def get_project_from_id(id:int) -> dict:
    url = f"{API_URL}/projects/{id}.json"
    page = requests.get(url, verify=False)
    
    return page.json()

def convert_to_datetime(observations: Union[dict, list]) -> list:
    campos = ["created_at", "observed_on", "updated_at"]
    
    if type(observations) is dict:
        for campo in campos:
            try:
                if type(observations[campo]) != datetime.datetime:
                    observations[campo] = datetime.datetime.fromisoformat(observations[campo])
            except KeyError:
                pass
    elif type(observations) is list:
        for observation in observations:
            for campo in campos:
                try:
                    if type(observation[campo]) != datetime.datetime:
                        observation[campo] = datetime.datetime.fromisoformat(observation[campo])
                except KeyError:
                    pass
    return observations


def get_obs_from_query(query:str) -> list:
    observations = []
    n = 1
    url = f'{API_URL}/observations.json?q="{query}"&per_page=200&page={n}'
    page = requests.get(url)
    if len(requests.get(f'{API_URL}/observations.json?q="{query}"&per_page=200&page=100').json()) < 200:
        while len(page.json()) == 200:
            observations.extend(page.json())
            n += 1
            url = f'{API_URL}/observations.json?q="{query}"&per_page=200&page={n}'
            page = requests.get(url)
        
        observations.extend(page.json())
    else:
        raise ValueError("Number of results out of range. Need to add more filters")
            
    #__import__("pdb").set_trace()
    
    observations = convert_to_datetime(observations)

    return observations

def get_obs_from_id(id:int) -> dict:
    """Get information on a specific observation given an id"""

    url = f'{API_URL}/observations/{id}.json'
    page = requests.get(url)
    
    observation = convert_to_datetime(page.json())

    return observation

def get_obs_from_user(user:str) -> list:
    """Download observations for a user"""
    observations = []
    n = 1
    url = f'{API_URL}/observations/{user}.json?per_page=200&page={n}'
    page = requests.get(url)
        
    while len(page.json()) == 200:
        observations.extend(page.json())
        n += 1
        url = f'{API_URL}/observations/{user}.json?per_page=200&page={n}'
        page = requests.get(url)
        
    observations.extend(page.json())

    observations = convert_to_datetime(observations)

    #__import__("pdb").set_trace()

    return observations

def get_obs_from_project(id:int) -> list:
    """Download observations or info from a project"""
    observations = []
    n = 1
    url = f"{API_URL}/observations/project/{id}.json?per_page=200&page={n}"
    page = requests.get(url)

    while len(page.json()) == 200:
        observations.extend(page.json())
        n += 1
        url = f"{API_URL}/observations/project/{id}.json?per_page=200&page={n}"
        page = requests.get(url)
    
    observations.extend(page.json())

    observations = convert_to_datetime(observations)

    return observations

def get_project_from_name(name:str) -> dict:
    """Download information of projects from name"""  
    
    url = f"{API_URL}/projects/search.json?q={name}"
    page = requests.get(url, verify=False)
    
    resultado = convert_to_datetime(page.json())

    return resultado

def get_obs_from_taxon(taxon:str) -> list:
    taxon_names = [
        "Chromista",
        "Protozoa",
        "Animalia",
        "Mollusca",
        "Arachnida",
        "Insecta",
        "Aves",
        "Mammalia",
        "Amphibia",
        "Reptilia",
        "Actinopterygii",
        "Fungi",
        "Plantae",
        "unknown"
    ]

    if taxon in taxon_names:
        observations = []
        n = 1
        url = f"{API_URL}/observations.json?iconic_taxa={taxon}&per_page=200&page={n}"
        page = requests.get(url, verify=False)

        while len(page.json()) == 200:
            observations.extend(page.json())
            n += 1
            url = f"{API_URL}/observations.json?iconic_taxa={taxon}&per_page=200&page={n}"
            page = requests.get(url, verify=False)

        observations.extend(page.json())
        
        observations = convert_to_datetime(observations)
        
        return observations

    else:
        print("No es una taxonomía válida")

def get_ids_from_place(place:str) -> list:
    place_ids = []
    url = f"{API_URL}/places.json?q={place}"
    page = requests.get(url, verify=False)

    for dct in page.json():
        place_id = dct['id']
        place_ids.append(place_id)
    return place_ids

def get_obs_from_place_name(place:str) -> list:
    
    place_ids = get_ids_from_place(place)
    
    #__import__("pdb").set_trace()
    
    observations = []
    for place_id in place_ids:
        n = 1
        url = f"{API_URL}/observations.json?place_id={place_id}&per_page=200&page={n}"
        page = requests.get(url, verify=False)
        if len(page.json()) > 0:
            while len(page.json()) == 200:
                observations.extend(page.json())
                n += 1
                url = f"{API_URL}/observations.json?place_id={place_id}&per_page=200&page={n}"
                page = requests.get(url, verify=False)

            observations.extend(page.json())

    observations = convert_to_datetime(observations)

    for observation in observations:
        observation['place_id'] = place_id
        
    return observations
    
def get_obs_from_place_id(place_id:int) -> list:
    
    n = 1
    observations = []
    
    url = f"{API_URL}/observations.json?place_id={place_id}&per_page=200&page={n}"
    page = requests.get(url, verify=False)
    if len(page.json()) > 0:
        while len(page.json()) == 200:
            observations.extend(page.json())
            n += 1
            url = f"{API_URL}/observations.json?place_id={place_id}&per_page=200&page={n}"
            page = requests.get(url, verify=False)

        observations.extend(page.json())
        observations = convert_to_datetime(observations)    

    else:
        print("No existen observaciones para este id de lugar")
    
    return observations

#get_inat_obs_project(): Download observations or info from a project
