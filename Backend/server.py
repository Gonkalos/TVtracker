from flask import Flask, request
import requests
import json
import Utils.configs as configs
import Utils.token as tokens
from Models.user import User
from Models.series import Series, SearchSeries
from Database.db import Database

# Initialize database
mydb = Database(configs.DB_USER, configs.DB_PASSWORD, configs.DB_NAME)
mydb.createDatabase()

# Initialize a Flask server
app = Flask(__name__)


# Create Account
@app.route('/CreateAccount', methods=['POST'])
def createAccount():
    # Get body parameters
    data = request.get_json()
    parameters = ['username', 'email', 'password1', 'password2']
    if all(elem in list(data) for elem in parameters) and len(data) >= 4:
        username = data['username']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        # Validate data
        if password1 == password2:
            return mydb.insertUser(username, email, password1)
        else: return 'Error: The passwords don\'t match.'
    else: return 'Error: Missing data.'


# Login
@app.route('/Login', methods=['POST'])
def login():
    # Get body parameters
    data = request.get_json()
    parameters = ['email', 'password']
    if all(elem in list(data) for elem in parameters) and len(data) >= 2:
        email = data['email']
        password = data['password']
        # Validate data
        if mydb.validateUser(email, password): return tokens.encode_auth_token(email)
        else: return 'Error: Invalid email or password'
    else: return 'Error: Missing data.'


# Change Password
@app.route('/ChangePassword', methods=['POST'])
def changePassword():
    # Validate Authorization Token
    bearer_check, token = checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            data = request.get_json()
            parameters = ['old_password', 'new_password1', 'new_password2']
            if all(elem in list(data) for elem in parameters) and len(data) >= 3:
                old_password = data['old_password']
                new_password1 = data['new_password1']
                new_password2 = data['new_password2']
                # Validate Data
                if new_password1 == new_password2: return mydb.changePassword(data[1], old_password, new_password1)
                else: return 'Error: The new passwords don\'t match.'
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Get series by title
@app.route('/GetSeries', methods=['POST'])
def getSeries():
    # Validate Authorization Token
    bearer_check, token = checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID']
            if all(elem in list(data) for elem in parameters) and len(data) >= 1:
                imdbID = data['imdbID']
                # Send request
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series', 'plot': 'full'})
                # Get response status code
                status = response.status_code
                # Check response status 
                if status == 200:
                    jsonResponse = response.json()
                    # Get number of episodes for each season
                    totalEpisodes = getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                    # Create series
                    series = Series(jsonResponse['imdbID'], jsonResponse['Title'], jsonResponse['Year'], jsonResponse['Genre'], 
                                    jsonResponse['Director'], jsonResponse['Writer'], jsonResponse['Plot'], jsonResponse['Poster'], 
                                    jsonResponse['imdbRating'], jsonResponse['totalSeasons'], totalEpisodes)
                    return series.json()
                else: return 'Error: OMDb response status ' + str(status)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Search for a series by matching titles
@app.route('/SearchSeries', methods=['POST'])
def searchSeries():
    # Validate Authorization Token
    bearer_check, token = checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['search']
            if all(elem in list(data) for elem in parameters) and len(data) >= 1:
                search = data['search']
                # Send request
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 's': search, 'type': 'series'})
                # Get response status code
                status = response.status_code
                # Check response status 
                if status == 200:
                    jsonResponse = response.json()
                    results = []
                    string = '['
                    for result in jsonResponse['Search']:
                        series = SearchSeries(result['imdbID'], result['Title'], result['Poster'])
                        string = string + series.json() + ','
                    return string[:-1] + ']'
                else: return 'Error: OMDb response status ' + str(status)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Add Series
@app.route('/AddSeries', methods=['POST'])
def addSeries():
    pass


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
        return str(totalEpisodes)
    else: return 'Error: OMDb response status ' + str(status)


# Get the number of episodes of all seasons from a series
def getTotalEpisodes(title, totalSeasons):
    totalEpisodes = [0] * totalSeasons
    for season in range(1, totalSeasons + 1):
        numberEpisodes = getSeasonEpisodes(title, season)
        if numberEpisodes.isdigit():
            totalEpisodes[season - 1] = numberEpisodes
    return totalEpisodes


if __name__ == '__main__':
    app.run(host='0.0.0.0')
