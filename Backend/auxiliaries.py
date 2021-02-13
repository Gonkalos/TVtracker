from flask import Flask, request
import requests
import json
import Utils.configs as configs

# Note: in case of errors the OMDb API returns [200] {"Response":"False","Error":"Something went wrong."}

class OMDbException(Exception):
    pass

# Check Bearer Token Authentication existence
def checkAuth(headers):
    if 'Authorization' in headers:
        auth = str(headers['Authorization']).split()
        if auth[0] == 'Bearer': return True, auth[1]
        else: return False, 'Missing Bearer Token Authorization'
    else: return False, 'Missing Bearer Token Authorization'

# Search for a series by matching titles
def searchSeries(search):
    # Send request to OMDb API
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 's': search, 'type': 'series'})
    # Validate status code
    if response.status_code == 200:
        jsonResponse = response.json()
        # Check OMDb API errors
        if 'Error' not in jsonResponse: 
            return jsonResponse
        else: raise OMDbException('OMDb API Error')
    else: raise OMDbException('OMDb API Status Code ' + str(response.status_code))

# Get series by IMDb id
def getSeries(imdbID):
    # Send request to OMDb API
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series', 'plot': 'full'})
    # Validate status code
    if response.status_code == 200:
        jsonResponse = response.json()
        # Check OMDb API errors
        if 'Error' not in jsonResponse: 
            return jsonResponse
        else: raise OMDbException('OMDb API Error')
    else: raise OMDbException('OMDb API Status Code ' + str(response.status_code))

# Get the number of episodes of a season from a series
def getSeasonEpisodes(title, season):
    # Send request to OMDb API
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 't': title, 'Season': season})
    # Validate status code
    if response.status_code == 200:
        jsonResponse = response.json()
        # Check OMDb API errors
        if 'Error' not in jsonResponse: 
            return len(jsonResponse['Episodes'])
        else: raise OMDbException('OMDb API Error')
    else: raise OMDbException('OMDb API Status Code ' + str(response.status_code))

# Get the number of episodes for all seasons of a series
def getTotalEpisodes(imdbID):
    # Get series
    jsonResponse = getSeries(imdbID)
    title = jsonResponse['Title']
    totalSeasons = int(jsonResponse['totalSeasons'])
    # Get number of episodes
    episodes = {}
    for season in range(1, totalSeasons + 1):
        episodes[season] = getSeasonEpisodes(title, season)
    return episodes

# Check if series exists
def checkSeries(imdbID):
    # Send request to OMDb API
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
    # Validate status code
    if response.status_code == 200:
        jsonResponse = response.json()
        # Check OMDb API errors
        if 'Error' in jsonResponse: raise OMDbException('OMDb API Error')
    else: raise OMDbException('OMDb API Status Code ' + str(response.status_code))