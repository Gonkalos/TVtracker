from flask import Flask, request, jsonify
import requests
import auxiliaries as aux
import Utils.configs as configs
import Utils.token as tokens
import Database.db_main as mydb

# Initialize database
mydb.createDatabase()

# Initialize a Flask server
app = Flask(__name__)

# Routes

# Create Account
@app.route('/CreateAccount', methods=['POST'])
def createAccount():
    # Get request data
    data = request.get_json()
    # Validate all body fields existence
    fields = ['username', 'email', 'password1', 'password2']
    if all(elem in list(data) for elem in fields) and len(data) >= 4:
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
    # Get request data
    data = request.get_json()
    # Validate all body fields existence
    fields = ['email', 'password']
    if all(elem in list(data) for elem in fields) and len(data) >= 2:
        # Get body fields
        email = data['email']
        password = data['password']
        # Validate data
        if mydb.validateUser(email, password): 
            token_generated, token = tokens.encode_auth_token(email)
            if token_generated: return token, 200
            else: return token, 500 
        else: return 'Invalid email or password', 400
    else: return 'Missing data', 400


# Change Password
@app.route('/ChangePassword', methods=['POST'])
def changePassword():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['old_password', 'new_password1', 'new_password2']
            if all(elem in list(data) for elem in fields) and len(data) >= 3:
                # Get body fields
                old_password = data['old_password']
                new_password1 = data['new_password1']
                new_password2 = data['new_password2']
                # Validate data
                if new_password1 == new_password2: 
                    if mydb.changePassword(decode, old_password, new_password1): return 'Success', 200
                    else: return 'Incorrect password', 400
                else: return 'Unmatched passwords', 400
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Search for a series by matching titles
@app.route('/SearchSeries', methods=['POST'])
def searchSeries():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['search']
            if all(elem in list(data) for elem in fields) and len(data) >= 1:
                # Get body fields
                search = data['search']
                # Send request to OMDb API
                jsonResponse = aux.searchSeries(search)
                results = []
                for result in jsonResponse['Search']:
                    series = {'imdbID': result['imdbID'], 'title': result['Title'], 'poster': result['Poster']}
                    results.append(series)
                return jsonify(results = results), 200
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Get series by IMDb id
@app.route('/GetSeries', methods=['POST'])
def getSeries():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID']
            if all(elem in list(data) for elem in fields) and len(data) >= 1:
                # Get body fields
                imdbID = data['imdbID']
                # Send request to OMDb API
                jsonResponse = aux.getSeries(imdbID)
                # Get number of episodes for each season
                episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                return jsonify(imdbID=jsonResponse['imdbID'], title=jsonResponse['Title'], year=jsonResponse['Year'], genre=jsonResponse['Genre'], 
                               director=jsonResponse['Director'], writer=jsonResponse['Writer'], plot=jsonResponse['Plot'], poster=jsonResponse['Poster'], 
                               imdbRating=jsonResponse['imdbRating'], episodes=episodes), 200
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Add Series
@app.route('/AddSeries', methods=['POST'])
def addSeries():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID']
            if all(elem in list(data) for elem in fields) and len(data) >= 1:
                # Get body fields
                imdbID = data['imdbID']
                # Check if series exists
                aux.checkSeries(imdbID)
                # Send to database
                return mydb.addSeries(decoding, imdbID)
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Remove Series
@app.route('/RemoveSeries', methods=['POST'])
def removeSeries():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID']
            if all(elem in list(data) for elem in fields) and len(data) >= 1:
                # Get body fields
                imdbID = data['imdbID']
                # Send to database
                return mydb.removeSeries(decoding, imdbID)
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Update series status
@app.route('/UpdateSeriesStatus', methods=['POST'])
def updateSeriesStatus():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID', 'status']
            if all(elem in list(data) for elem in fields) and len(data) >= 2:
                # Get body fields
                imdbID = data['imdbID']
                status = data['status']
                # Get number of episodes for each season
                episodes = aux.getTotalEpisodes(imdbID)
                # Send to database
                return mydb.updateSeriesStatus(decoding, imdbID, status, episodes)
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Rate Series
@app.route('/RateSeries', methods=['POST'])
def rankSeries():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID', 'rating']
            if all(elem in list(data) for elem in fields) and len(data) >= 2:
                # Get body fields
                imdbID = data['imdbID']
                rating = data['rating']
                # Send to database
                return mydb.rateSeries(decoding, imdbID, rating)
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401


# Check one episode as seen 
@app.route('/CheckEpisode', methods=['POST'])
def checkEpisode():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID']
            if all(elem in list(data) for elem in fields) and len(data) >= 1:
                # Get body fields
                imdbID = data['imdbID']
                # Send request to OMDb API
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
                jsonResponse = response.json()
                # Get number of episodes for each season
                episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                # Send to database
                return mydb.checkEpisode(decoding, imdbID, episodes)
            else: return 'Missing data', 400
        else: return decode, 400
    else: return token, 401


# Update number of episodes seen
@app.route('/UpdateEpisodes', methods=['POST'])
def updateEpisodes():
    # Validate Bearer Token existence / Get Bearer Token
    token_exists, token = aux.checkAuth(request.headers)
    if token_exists:
        # Validate Bearer Token authenticity / Get Beared Token decoding
        token_authentic, decoding = tokens.decode_auth_token(token)
        if token_authentic:
            # Get request data
            data = request.get_json()
            # Validate all body fields existence
            fields = ['imdbID', 'updated_episode', 'updated_season']
            if all(elem in list(data) for elem in fields) and len(data) >= 3:
                # Get body fields
                imdbID = data['imdbID']
                updated_episode = data['updated_episode']
                updated_season = data['updated_season']
                # Send request to OMDb API
                response = requests.get(configs.OMDB_API_URL, params={'apikey': configs.OMDB_API_KEY, 'i': imdbID, 'type': 'series'})
                jsonResponse = response.json()
                # Get number of episodes for each season
                episodes = aux.getTotalEpisodes(jsonResponse['Title'], int(jsonResponse['totalSeasons']))
                if updated_season in episodes.keys():
                    if updated_episode <= episodes[updated_season]:
                        # Send to database
                        return mydb.updateEpisodes(decoding, imdbID, episodes, updated_episode, updated_season)
                    else: return 'Invalid episode', 400
                else: return 'Invalid season', 400
            else: return 'Missing data', 400
        else: return decoding, 400
    else: return token, 401

# Error Handlers

@app.errorhandler(aux.OMDbException)
def badGateway(error):
    return str(error), 502


@app.errorhandler(500)
def internalServerError(error):
    return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
