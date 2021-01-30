from serie import UserSerie

class User:

    # Class initialization
    def __init__(self, username):
        self.username = username
        self.list = {}

    # Update username
    def updateUsername(self, newUsername):
        self.username = newUsername

    # Add serie to user list
    def addSerie(self, serieID, totalSeasons, totalEpisodes):
        if serieID in self.list:
            raise Exception('The serie is already in user list.')
        else:
            self.list[serieID] = UserSerie(totalSeasons, totalEpisodes) 

    # Remove serie from user list
    def removeSerie(self, serieID):
        if serieID in self.list:
            self.list.pop(serieID)
        else:
            raise Exception('The serie is not in user list.')

    # Update serie rating
    def updateRating(self, serieID, newRating):
        if serieID in self.list:
            self.list[serieID].updateRating(newRating)
        else:
            raise Exception('The id does not corresponde to a serie in user list.')

