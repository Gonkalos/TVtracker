from series import UserSeries

class User:

    # Class initialization
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.list = {}

    # Update username
    def updateUsername(self, newUsername):
        self.username = newUsername

    # Add serie to user list
    def addSerie(self, seriesID, totalSeasons, totalEpisodes):
        if seriesID in self.list:
            raise Exception('The series is already in user list.')
        else:
            self.list[seriesID] = UserSeries(totalSeasons, totalEpisodes) 

    # Remove serie from user list
    def removeSerie(self, serieID):
        if serieID in self.list:
            self.list.pop(serieID)
        else:
            raise Exception('The series is not in user list.')

    # Update serie rating
    def updateRating(self, seriesID, newRating):
        if seriesID in self.list:
            self.list[seriesID].updateRating(newRating)
        else:
            raise Exception('The id does not corresponde to a series in user list.')

