from flask import Flask, request
import requests
import constants
from series import Series, SearchSeries
from user import User

# Initialize a Flask server
app = Flask(__name__)

# Get series by title
@app.route('/GetSeries')
def getSeries():
    # Get body parameters  
    imdbID = request.args.get('imdbID')
    # Send request
    response = requests.get(constants.OMDB_API_URL, params={'apikey': constants.OMDB_API_KEY, 'i': imdbID, 'type': 'series', 'plot': 'full'})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        jsonResponse = response.json()
        # Get number of episodes for each season
        totalEpisodes = getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
        # Create series
        series = Series(jsonResponse['imdbID'], jsonResponse['Title'], jsonResponse['Year'], jsonResponse['Genre'], jsonResponse['Director'], 
                        jsonResponse['Writer'], jsonResponse['Plot'], jsonResponse['Poster'], jsonResponse['imdbRating'], jsonResponse['totalSeasons'], totalEpisodes)
        return series.json()
    else:
        return 'Response Error ' + str(status)

# Get the number of episodes of a season from a series
def getSeasonEpisodes(title, season):
    # Send request
    response = requests.get(constants.OMDB_API_URL, params={'apikey': constants.OMDB_API_KEY, 't': title, 'Season': season})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        jsonResponse = response.json()
        totalEpisodes = len(jsonResponse['Episodes'])
        return str(totalEpisodes)
    else:
        return 'Response Error ' + str(status)

# Get the number of episodes of all seasons from a series
def getTotalEpisodes(title, totalSeasons):
    totalEpisodes = [0] * totalSeasons
    for season in range(1, totalSeasons + 1):
        numberEpisodes = getSeasonEpisodes(title, season)
        if numberEpisodes.isdigit():
            totalEpisodes[season - 1] = numberEpisodes
    return totalEpisodes

# Search for a series by matching titles
@app.route('/SearchSeries')
def searchSeries():
    # Get body parameters  
    search = request.args.get('search')
    # Send request
    response = requests.get(constants.OMDB_API_URL, params={'apikey': constants.OMDB_API_KEY, 's': search, 'type': 'series'})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        jsonResponse = response.json()
        results = []
        for result in jsonResponse['Search']:
            series = SearchSeries(result['imdbID'], result['Title'], result['Poster'])
            results.append(series)
        return results[0].json()
    else:
        return 'Response Error ' + str(status)



# Update series rating
@app.route('/rateSeries')
def updateRating():
    # Get body parameters  
    seriesID = request.args.get('seriesID')
    rating = request.args.get('rating')
    return 'OK'


if __name__ == '__main__':
    app.run()
