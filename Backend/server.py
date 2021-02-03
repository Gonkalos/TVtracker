from flask import Flask, request
import requests
import json
import Utils.constants as constants
import Utils.token as tokens
from Models.user import User
from Models.series import Series, SearchSeries
from Database.db import Database

# Initialize database
mydb = Database(constants.DB_USER, constants.DB_PASSWORD, constants.DB_NAME)
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
        if password1 != password2: return 'Error: The passwords don\'t match.'
        else: mydb.insertUser(username, email, password1)
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
        user_valitation = mydb.validateUser(email, password)
        if user_valitation == 'Success':
            login_check = mydb.checkLogin(email)
            if login_check == 'Success':
                token = tokens.encode_auth_token(email)
                if token != 'Error':
                    mydb.updateToken(email, token)
                    return token
                else: return 'Error: Problem generating token.'
            else: return login_check
        else: return user_valitation
    else: return 'Error: Missing data.'


# Logout
@app.route('/Logout', methods=['GET'])
def logout():
    # Get body parameters
    if 'Authorization' in request.headers:
        auth = request.headers['Authorization']
        data = str(auth).split()
        if data[0] == 'Bearer':
            return mydb.logout(data[1])
        else: return 'Error: Authorization type is not Bearer.'
    else: return 'Error: Missing Authorization.'


# Change Password
@app.route('/ChangePassword', methods=['POST'])
def changePassword():
    # Get Authorization Token
    if 'Authorization' in request.headers:
        auth = request.headers['Authorization']
        data = str(auth).split()
        if data[0] != 'Bearer': return 'Error: Authorization type is not Bearer.'
    else: return 'Error: Missing Authorization.'
    # Get body parameters
    data = request.get_json()
    parameters = ['token', 'old_password', 'new_password1', 'new_password2']
    if all(elem in list(data) for elem in parameters) and len(data) >= 4:
        token = data['token']
        old_password = data['old_password']
        new_password1 = data['new_password1']
        new_password2 = data['new_password2']
        # Validate Data
        if new_password1 != new_password2: return 'Error: The new passwords don\'t match.'
        return mydb.changePassword(token, old_password, new_password1)
    else: return 'Error: Missing data.'


# Get series by title
@app.route('/GetSeries')
def getSeries():
    # Get body parameters 
    parameters = ['imdbID']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
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
            series = Series(jsonResponse['imdbID'], jsonResponse['Title'], jsonResponse['Year'], jsonResponse['Genre'], 
                            jsonResponse['Director'], jsonResponse['Writer'], jsonResponse['Plot'], jsonResponse['Poster'], 
                            jsonResponse['imdbRating'], jsonResponse['totalSeasons'], totalEpisodes)
            return series.json()
        else: return 'Error: OMDb response status ' + str(status)
    else: return 'Error: Missing parameters'


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
    else: return 'Error: OMDb response status ' + str(status)


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
    parameters = ['search']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
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
        else: return 'Error: OMDb response status ' + str(status)
    else: return 'Error: Missing parameters'


# Add Series
@app.route('/AddSeries', methods=['POST'])
def addSeries():
    data = request.get_json()
    if 'imdbID' in data: 
        imdbID = data['imdbID']
        return imdbID
    else: return 'Error: Missing data.'







# Test
@app.route('/Test')
def test():
    if 'Authorization' in request.headers:
        auth = request.headers['Authorization']
        data = str(auth).split()
        if data[0] == 'Bearer':
            return str(tokens.decode_auth_token(data[1]))
        else: return 'Error: Authorization type is not Bearer.'
    else: return 'Error: Missing Authorization.'




if __name__ == '__main__':
    app.run(host='0.0.0.0')
