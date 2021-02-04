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
        dic = {}
        dic['Title'] = self.title
        dic['Year'] = self.year
        dic['Genre'] = self.genre
        dic['Director'] = self.director
        dic['Writer'] = self.writer
        dic['Plot'] = self.plot
        dic['Poster'] = self.poster
        dic['IMDbRating'] = self.imdbRating
        dic['TotalSeasons'] = self.totalSeasons
        dic['TotalEpisodes'] = self.totalEpisodes
        return json.dumps(dic)


class SearchSeries:

    # Class initialization
    def __init__(self, imdbID, title, poster):
        self.imdbID = imdbID
        self.title = title
        self.poster = poster

    # To json string
    def json(self):
        dic = {}
        dic['IMDbID'] = self.imdbID
        dic['Title'] = self.title
        dic['Poster'] = self.poster
        return json.dumps(dic)


class UserSeries:

    # Class initialization
    def __init__(self, totalSeasons, totalEpisodes):
        self.status = status[0]
        self.episodesSeen = [0] * totalSeasons
        self.rating = -1

    # Update rating
    def updateRating(self, newRating):
        self.rating = newRating


