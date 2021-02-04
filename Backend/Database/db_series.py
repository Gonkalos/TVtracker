import mysql.connector
import Utils.configs as configs

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
            return 'Error: Series already added.'
    else: 
        mycursor.close()
        mydb.close()
        return 'Error: User not found.'

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
                if status == 'Watching' or status == 'Rewatching':
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