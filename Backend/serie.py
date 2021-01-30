# Serie status enumerator
status = ['Watching', 'Rewatching', 'Completed', 'Plan To Watch']

class Serie:

    # Class initialization
    def __init__(self, imdbID, title, year, genre, director, writer, plot, poster, imdbRating, type, totalSeasons, totalEpisodes):
        self.imdbID = imdbID
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.writer = writer
        self.plot = plot
        self.poster = poster
        self.imdbRating = imdbRating
        self.type = type
        self.totalSeasons = totalSeasons
        self.totalEpisodes = totalEpisodes

    # To string
    def toString(self):
        string = 'Title: ' + self.title + '\n' \
               + 'Year: ' + self.year  + '\n' \
               + 'Genre: ' + self.genre + '\n' \
               + 'Director: ' + self.director + '\n' \
               + 'Writer: ' + self.writer + '\n' \
               + 'Plot: ' + self.plot + '\n' \
               + 'Poster: ' + self.poster + '\n' \
               + 'IMDb Rating: ' + self.imdbRating + '\n' \
               + 'Type: ' + self.type + '\n' \
               + 'Number of Seasons: ' + self.totalSeasons + '\n' \
               + 'Episodes: ' + str(self.totalEpisodes)
        return string

class UserSerie:

    # Class initialization
    def __init__(self, totalSeasons, totalEpisodes):
        self.status = status[0]
        self.totalEpisodes = totalEpisodes # nember of episodes in each season
        self.episodesSeen = [0] * totalSeasons # number of episodes seen in each season 
        self.rating = -1

    # Update rating
    def updateRating(self, newRating):
        self.rating = newRating


