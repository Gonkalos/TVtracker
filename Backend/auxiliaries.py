from flask import Flask, request
import requests
import Utils.configs as configs

# Check for Bearer Token Authentication
def checkAuth(headers):
    if 'Authorization' in headers:
        auth = str(headers['Authorization']).split()
        if auth[0] == 'Bearer': return True, auth[1]
        else: return False, 'Error: Missing Bearer Token Authorization.'
    else: return False, 'Error: Missing Bearer Token Authorization.'

# Get the number of episodes of a season from a series
def getSeasonEpisodes(title, season):
    # Send request
    response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 't': title, 'Season': season})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        jsonResponse = response.json()
        totalEpisodes = len(jsonResponse['Episodes'])
        return True, totalEpisodes
    else: return False, 'Error: OMDb response status ' + str(status)

# Get the number of episodes of all seasons from a series
def getTotalEpisodes(title, totalSeasons):
    episodes = {}
    for season in range(1, totalSeasons + 1):
        check, response = getSeasonEpisodes(title, season)
        if check:
            episodes[season] = response
        else: return False, response
    return True, episodes