from flask import Flask, request
import requests
import Utils.constants as constants
from Models.user import User
from Models.series import Series, SearchSeries
from Database.db import Database

# Initialize database
mydb = Database(constants.DB_USER, constants.DB_PASSWORD, constants.DB_NAME)
mydb.createDatabase()

# Initialize a Flask server
app = Flask(__name__)


# Create Account
@app.route('/CreateAccount')
def createAccount():
    # Get body parameters
    parameters = ['username', 'email', 'password1', 'password2']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
        username = request.args.get('username')
        email = request.args.get('email')
        password1 = request.args.get('password1')
        password2 = request.args.get('password2')
        # Validate data
        if password1 != password2: return 'Error: The passwords don\'t match.'
        return mydb.insertUser(username, email, password1)
    else: return 'Error: Missing parameters'


# Login
@app.route('/Login')
def login():
    # Get body parameters
    parameters = ['email', 'password']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
        email = request.args.get('email')
        password = request.args.get('password')
        # Validate data
        user_valitation = mydb.validateUser(email, password)
        if user_valitation == 'Success':
            login_check = mydb.checkLogin(email)
            if login_check == 'Success':
                token = mydb.generateToken()
                mydb.updateToken(email, token)
                return token
            else: return login_check
        else: return user_valitation
    else: return 'Error: Missing parameters'


# Logout
@app.route('/Logout')
def logout():
    # Get body parameters
    parameters = ['token']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
        token = request.args.get('token')
        #token = request.headers.get('Authorization')
        return mydb.logout(token)
    else: return 'Error: Missing parameters'


# Change Password
@app.route('/ChangePassword')
def changePassword():
    # Get body parameters
    parameters = ['token', 'old_password', 'new_password1', 'new_password2']
    if all(elem in parameters for elem in request.args) and len(request.args) > 0:
        token = request.args.get('token')
        old_password = request.args.get('old_password')
        new_password1 = request.args.get('new_password1')
        new_password2 = request.args.get('new_password2')
        # Validate Data
        if new_password1 != new_password2: return 'Error: The new passwords don\'t match.'
        return mydb.changePassword(token, old_password, new_password1)
    else: return 'Error: Missing parameters'


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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
