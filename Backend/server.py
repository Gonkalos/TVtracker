from flask import Flask, request, jsonify
import requests
import json
import auxiliaries as aux
import Utils.configs as configs
import Utils.token as tokens
import Database.db_main as mydb

# Initialize database
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
            if mydb.insertUser(username, email, password1): return 'Success', 200
            else: return 'Username or email already in use', 400
        else: return 'Unmatched passwords', 400
    else: return 'Missing data', 400


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
        if mydb.validateUser(email, password): 
            generated_check, token = tokens.encode_auth_token(email)
            if generated_check: return token, 200
            else: return token, 500 
        else: return 'Invalid email or password', 400
    else: return 'Missing data', 400


# Change Password
@app.route('/ChangePassword', methods=['POST'])
def changePassword():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
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
                if new_password1 == new_password2: 
                    if mydb.changePassword(decode, old_password, new_password1): return 'Success', 200
                    else: return 'Incorrect password', 400
                else: return 'Unmatched passwords', 400
            else: return 'Missing data', 400
        else: return decode, 400
    else: return token, 400


# Get series by title
@app.route('/GetSeries', methods=['POST'])
def getSeries():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
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
                    episodes_check, episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                    if episodes_check:
                        # Create series
                        return jsonify(imdbID=jsonResponse['imdbID'], title=jsonResponse['Title'], year=jsonResponse['Year'], genre=jsonResponse['Genre'], 
                                       director=jsonResponse['Director'], writer=jsonResponse['Writer'], plot=jsonResponse['Plot'], poster=jsonResponse['Poster'], 
                                       imdbRating=jsonResponse['imdbRating'], episodes=episodes), 200
                    else: return episodes, 502
                else: return 'OMDb response status code ' + str(status), 502
            else: return 'Missing data', 400
        else: return decode, 400
    else: return token, 400


# Search for a series by matching titles
@app.route('/SearchSeries', methods=['POST'])
def searchSeries():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
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
                    for result in jsonResponse['Search']:
                        series = {'imdbID': result['imdbID'], 'title': result['Title'], 'poster': result['Poster']}
                        results.append(series)
                    return jsonify(results = results), 200
                else: return 'OMDb response status code ' + str(status), 502
            else: return 'Missing data', 400
        else: return decode, 400
    else: return token, 400


# Add Series
@app.route('/AddSeries', methods=['POST'])
def addSeries():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID']
            if all(elem in list(data) for elem in parameters) and len(data) >= 1:
                imdbID = data['imdbID']
                return mydb.addSeries(decode, imdbID)
            else: return 'Missing data', 400
        else: return decode, 400
    else: return token, 400


# Remove Series
@app.route('/RemoveSeries', methods=['POST'])
def removeSeries():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID']
            if all(elem in list(data) for elem in parameters) and len(data) >= 1:
                imdbID = data['imdbID']
                return mydb.removeSeries(decode, imdbID)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Update series status
@app.route('/UpdateSeriesStatus', methods=['POST'])
def updateSeriesStatus():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID', 'status']
            if all(elem in list(data) for elem in parameters) and len(data) >= 2:
                imdbID = data['imdbID']
                seriesStatus = data['status']
                # Send request
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
                # Get response status code
                status = response.status_code
                # Check response status 
                if status == 200:
                    jsonResponse = response.json()
                    # Get number of episodes for each season
                    episodes_check, episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                    if episodes_check: return mydb.updateSeriesStatus(decode, imdbID, seriesStatus, episodes)
                    else: return episodes
                else: return 'Error: OMDb response status ' + str(status)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Rate Series
@app.route('/RateSeries', methods=['POST'])
def rankSeries():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID', 'rating']
            if all(elem in list(data) for elem in parameters) and len(data) >= 2:
                imdbID = data['imdbID']
                rating = data['rating']
                return mydb.rateSeries(decode, imdbID, rating)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Check one episode as seen 
@app.route('/CheckEpisode', methods=['POST'])
def checkEpisode():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID']
            if all(elem in list(data) for elem in parameters) and len(data) >= 1:
                imdbID = data['imdbID']
                # Send request
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
                # Get response status code
                status = response.status_code
                # Check response status 
                if status == 200:
                    jsonResponse = response.json()
                    # Get number of episodes for each season
                    episodes_check, episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                    if episodes_check: return mydb.checkEpisode(decode, imdbID, episodes)
                    else: return episodes
                else: return 'Error: OMDb response status ' + str(status)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


# Update number of episodes seen
@app.route('/UpdateEpisodes', methods=['POST'])
def updateEpisodes():
    # Validate Authorization Token
    bearer_check, token = aux.checkAuth(request.headers)
    if bearer_check:
        valid_check, decode = tokens.decode_auth_token(token)
        if valid_check:
            # Get body parameters
            data = request.get_json()
            parameters = ['imdbID', 'updated_episode', 'updated_season']
            if all(elem in list(data) for elem in parameters) and len(data) >= 3:
                imdbID = data['imdbID']
                updated_episode = data['updated_episode']
                updated_season = data['updated_season']
                # Send request
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
                # Get response status code
                status = response.status_code
                # Check response status 
                if status == 200:
                    jsonResponse = response.json()
                    # Get number of episodes for each season
                    episodes_check, episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                    if episodes_check: 
                        if updated_season in episodes.keys():
                            if updated_episode <= episodes[updated_season]:
                                return mydb.updateEpisodes(decode, imdbID, episodes, updated_episode, updated_season)
                            else: return 'Error: Invalid episode.'
                        else: return 'Error: Invalid season.'
                    else: return episodes
                else: return 'Error: OMDb response status ' + str(status)
            else: return 'Error: Missing data.'
        else: return decode
    else: return token


if __name__ == '__main__':
    app.run(host='0.0.0.0')
