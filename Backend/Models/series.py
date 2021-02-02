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
        string = '{\"Title\": \"' + self.title + '\",' \
               + '\"Year\": \"' + self.year  + '\",' \
               + '\"Genre\": \"' + self.genre + '\",' \
               + '\"Director\": \"' + self.director + '\",' \
               + '\"Writer\": \"' + self.writer + '\",' \
               + '\"Plot\": \"' + self.plot + '\",' \
               + '\"Poster\": \"' + self.poster + '\",' \
               + '\"IMDbRating\": \"' + self.imdbRating + '\",' \
               + '\"TotalSeasons\": \"' + self.totalSeasons + '\",' \
               + '\"TotalEpisodes\": ['
        for season in range(0, int(self.totalSeasons) - 1):
            string += str(self.totalEpisodes[season]) + ', '
        string += str(self.totalEpisodes[int(self.totalSeasons) - 1]) + ']}'
        return string


class SearchSeries:

    # Class initialization
    def __init__(self, imdbID, title, poster):
        self.imdbID = imdbID
        self.title = title
        self.poster = poster

    # To json string
    def json(self):
        string = '{\"Title\": \"' + self.title + '\",' \
               + '\"Poster\": \"' + self.poster + '\"}'
        return string


class UserSeries:

    # Class initialization
    def __init__(self, totalSeasons, totalEpisodes):
        self.status = status[0]
        self.episodesSeen = [0] * totalSeasons
        self.rating = -1

    # Update rating
    def updateRating(self, newRating):
        self.rating = newRating


