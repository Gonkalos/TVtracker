import json

# Series status enumerator
status = ['Watching', 'Rewatching', 'Completed', 'Plan To Watch']

class Series:

    # Class initialization
    def __init__(self, imdbID, title, year, genre, director, writer, plot, poster, imdbRating, totalSeasons, totalEpisodes):
        self.imdbID = imdbID
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.writer = writer
        self.plot = plot
        self.poster = poster
        self.imdbRating = imdbRating
        self.totalSeasons = totalSeasons
        self.totalEpisodes = totalEpisodes

    # To json string
    def json(self):
        attributes = {}
        attributes['Title'] = self.title
        attributes['Year'] = self.year
        attributes['Genre'] = self.genre
        attributes['Director'] = self.director
        attributes['Writer'] = self.writer
        attributes['Plot'] = self.plot
        attributes['Poster'] = self.poster
        attributes['IMDbRating'] = self.imdbRating
        attributes['TotalSeasons'] = self.totalSeasons
        attributes['TotalEpisodes'] = self.totalEpisodes
        return json.dumps(attributes)


class SearchSeries:

    # Class initialization
    def __init__(self, imdbID, title, poster):
        self.imdbID = imdbID
        self.title = title
        self.poster = poster

    # To json string
    def json(self):
        attributes = {}
        attributes['IMDbID'] = self.imdbID
        attributes['Title'] = self.title
        attributes['Poster'] = self.poster
        return json.dumps(attributes)


class UserSeries:

    # Class initialization
    def __init__(self, totalSeasons, totalEpisodes):
        self.status = status[0]
        self.episodesSeen = [0] * totalSeasons
        self.rating = -1

    # Update rating
    def updateRating(self, newRating):
        self.rating = newRating


