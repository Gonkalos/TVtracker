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
        mycursor.execute(f'SELECT * FROM Series WHERE UserID = \'{userID}\' LIMIT 1')
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
        mycursor.execute(f'SELECT * FROM Series WHERE UserID = \'{userID}\' LIMIT 1')
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