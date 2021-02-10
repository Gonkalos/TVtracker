from flask import Flask, request
import requests
import Utils.configs as configs

# Check Bearer Token Authentication existence
def checkAuth(headers):
    if 'Authorization' in headers:
        auth = str(headers['Authorization']).split()
        if auth[0] == 'Bearer': return True, auth[1]
        else: return False, 'Missing Bearer Token Authorization'
    else: return False, 'Missing Bearer Token Authorization'

# Get the number of episodes of a season from a series
def getSeasonEpisodes(title, season):
    # Send request
    # If imdbID doesn't exist, returns status code 500
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 't': title, 'Season': season})
    jsonResponse = response.json()
    totalEpisodes = len(jsonResponse['Episodes'])
    return totalEpisodes

# Get the number of episodes for all seasons of a series
def getTotalEpisodes(title, totalSeasons):
    episodes = {}
    for season in range(1, totalSeasons + 1):
        episodes[season] = getSeasonEpisodes(title, season)
    return episodes