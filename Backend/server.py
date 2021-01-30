from flask import Flask
import requests
import constants
from series import Series
from user import User

# Initialize a Flask server
app = Flask(__name__)

# Get serie by title
@app.route('/getSeries/<title>')
def getSerie(title):
    # Send GET request
    response = requests.get(constants.OMDB_API_URL, params={'apikey': constants.OMDB_API_KEY, 't': title})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        json = response.json()
        # Get number of episodes for each season
        totalSeasons = int(json['totalSeasons'])
        totalEpisodes = [0] * totalSeasons
        for season in range(1, totalSeasons + 1):
            numberEpisodes = getSeason(json['Title'], season)
            if numberEpisodes.isdigit():
                totalEpisodes[season - 1] = numberEpisodes
        # Create series
        series = Series(json['imdbID'], json['Title'], json['Year'], json['Genre'], json['Director'], json['Writer'], json['Plot'], json['Poster'], json['imdbRating'], json['Type'], json['totalSeasons'], totalEpisodes)
        return series.toString()
    else:
        return 'Response Error ' + str(status)

# Get the number of episodes of a season from a series
@app.route('/getSeasonEpisodes/<title>&<number>')
def getSeason(title, number):
    # Send GET request
    response = requests.get(constants.OMDB_API_URL, params={'apikey': constants.OMDB_API_KEY, 't': title, 'Season': number})
    # Get response status code
    status = response.status_code
    # Check response status 
    if status == 200:
        json = response.json()
        totalEpisodes = len(json['Episodes'])
        return str(totalEpisodes)
    else:
        return 'Response Error ' + str(status)

# Update series rating
@app.route('/rateSeries/<seriesID>&<rating>')
def updateRating(seriesID, rating):
    return 'OK'


if __name__ == '__main__':
    app.run()
