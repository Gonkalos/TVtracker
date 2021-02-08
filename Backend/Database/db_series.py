import mysql.connector
import Utils.configs as configs

# Series status enumerator
status = ['Watching', 'Rewatching', 'Completed', 'Plan To Watch']

# Add series to user's list
def addSeries(email, imdbID):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None':
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT * FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result == 'None':
            mycursor.execute(f'INSERT INTO Series (IMDbID, Status, Rating, UserID) VALUES (\'{imdbID}\', \'Plan To Watch\', -1, {userID});')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else:
            mycursor.close()
            mydb.close()
            return 'Series already added'
    else: 
        mycursor.close()
        mydb.close()
        return 'User not found'

# Remove series from user's list
def removeSeries(email, imdbID):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None': 
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT * FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result != 'None':
            mycursor.execute(f'DELETE FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
            mydb.commit()
            mycursor.execute(f'DELETE FROM Episodes WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else:
            mycursor.close()
            mydb.close()
            return 'Error: Series not in list.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'

# Update series status
def updateSeriesStatus(email, imdbID, status, episodes):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None': 
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT Status FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result != 'None':
            current_status = result[2:].split('\'')[0]
            if status != current_status:
                # Update Episodes
                if status in ['Watching', 'Rewatching']:
                    for season in episodes:
                        mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({int(season)}, {0}, {userID}, \'{imdbID}\');')
                        mydb.commit()
                elif status == 'Completed':
                    for season in episodes:
                        mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({int(season)}, {episodes[season]}, {userID}, \'{imdbID}\');')
                        mydb.commit()
                elif status == 'Plan To Watch':
                    mycursor.execute(f'DELETE FROM Episodes WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
                    mydb.commit()
                else:
                    mycursor.close()
                    mydb.close()
                    return 'Error: Series status is invalid.'
                mycursor.execute(f'UPDATE Series SET Status = \'{status}\' WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
                mydb.commit()
                mycursor.close()
                mydb.close()
                return 'Success'
            else: 
                mycursor.close()
                mydb.close()
                return 'Error: Series status is the same.'
        else:
            mycursor.close()
            mydb.close()
            return 'Error: Series not in list.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'

# Update series rating
def rateSeries(email, imdbID, rating):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None': 
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT * FROM Series WHERE UserID = \'{userID}\' AND (Status = \'Completed\' OR Status = \'Rewatching\') LIMIT 1')
        result = str(mycursor.fetchone())
        if result != 'None':
            mycursor.execute(f'UPDATE Series SET Rating = {rating} WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else:
            mycursor.close()
            mydb.close()
            return 'Error: Series not in list or not completed.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'

# Check one episode as seen
def checkEpisode(email, imdbID, episodes):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None': 
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT Status FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result != 'None':
            current_status = result[2:].split('\'')[0]
            if current_status in ['Watching', 'Rewatching']:
                # Update Episodes
                last_season = len(episodes)
                for season in episodes:
                    mycursor.execute(f'SELECT EpisodesSeen FROM Episodes WHERE Season = {int(season)} AND IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
                    result = str(mycursor.fetchone())
                    episodesSeen = int(result[1:].split(',')[0])
                    if episodes[season] > episodesSeen:
                        if int(season) == last_season and episodes[season] == episodesSeen + 1:
                            mycursor.execute(f'UPDATE Series SET Status = \'Completed\' WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
                            mydb.commit()
                        mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({int(season)}, {episodesSeen + 1}, {userID}, \'{imdbID}\');')
                        mydb.commit()
                        break
                mycursor.close()
                mydb.close()
                return 'Success'
            else: 
                mycursor.close()
                mydb.close()
                return 'Error: Series status invalid.'
        else:
            mycursor.close()
            mydb.close()
            return 'Error: Series not in list.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'

# Update number of episodes seen
def updateEpisodes(email, imdbID, episodes, updated_episode, updated_season):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT UserID FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result != 'None': 
        userID = result[1:].split(',')[0]
        mycursor.execute(f'SELECT Status FROM Series WHERE IMDbID = \'{imdbID}\' AND UserID = \'{userID}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result != 'None':
            current_status = result[2:].split('\'')[0]
            if current_status != 'Plan To Watch':
                if current_status == 'Completed':
                    mycursor.execute(f'UPDATE Series SET Status = \'Rewatching\' WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
                    mydb.commit()
                # Update episodes before the updated one
                for season in range(1, updated_season):
                    mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({season}, {episodes[season]}, {userID}, \'{imdbID}\');')
                    mydb.commit()
                mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({updated_season}, {updated_episode}, {userID}, \'{imdbID}\');')
                mydb.commit()
                last_season = len(episodes)
                # Update episodes after the updated one
                if updated_season < last_season:
                    for season in range(updated_season + 1, last_season + 1):
                        mycursor.execute(f'REPLACE INTO Episodes (Season, EpisodesSeen, UserID, IMDbID) VALUES ({season}, {0}, {userID}, \'{imdbID}\');')
                        mydb.commit()
                else:
                    if updated_episode == episodes[last_season]:
                        mycursor.execute(f'UPDATE Series SET Status = \'Completed\' WHERE IMDbID = \'{imdbID}\' AND UserID = {userID};')
                        mydb.commit()
                mycursor.close()
                mydb.close()
                return 'Success'
            else: 
                mycursor.close()
                mydb.close()
                return 'Error: Series status invalid.'
        else:
            mycursor.close()
            mydb.close()
            return 'Error: Series not in list.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'
