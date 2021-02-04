import mysql.connector
import Utils.configs as configs
import Database.db_users as users
import Database.db_series as series

# Create database 
def createDatabase():
    # Create user
    mydb = mysql.connector.connect(host='localhost', user='root')
    mycursor = mydb.cursor()
    mycursor.execute(f'CREATE USER IF NOT EXISTS \'{configs.DB_USERNAME}\'@\'localhost\' IDENTIFIED BY \'{configs.DB_PASSWORD}\';')
    mycursor.execute(f'GRANT ALL PRIVILEGES ON *.* TO \'{configs.DB_USERNAME}\'@\'localhost\';')
    mycursor.close()
    mydb.close()
    # Create database
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD)
    mycursor = mydb.cursor()
    mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {configs.DB_NAME}')
    mycursor.close()
    mydb.close()
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    # Create users table
    mycursor.execute('CREATE TABLE IF NOT EXISTS Users (UserID int NOT NULL AUTO_INCREMENT, \
                                                        Username varchar(45) NOT NULL, \
                                                        Email varchar(100) NOT NULL, \
                                                        Password varchar(200) NOT NULL, \
                                                        PRIMARY KEY (UserID));')
    # Create series table
    mycursor.execute('CREATE TABLE IF NOT EXISTS Series (IMDbID varchar(9) NOT NULL, \
                                                         Status varchar(13) NOT NULL, \
                                                         Rating int NOT NULL, \
                                                         UserID int NOT NULL, \
                                                         PRIMARY KEY (IMDbID), \
                                                         FOREIGN KEY (UserID) REFERENCES Users(UserID), \
                                                         UNIQUE(IMDbID, UserID));')
    # Create episodes table
    mycursor.execute('CREATE TABLE IF NOT EXISTS Episodes (Season int NOT NULL, \
                                                           EpisodesSeen int NOT NULL, \
                                                           UserID int NOT NULL, \
                                                           IMDbID varchar(9) NOT NULL, \
                                                           FOREIGN KEY (UserID) REFERENCES Users(UserID), \
                                                           FOREIGN KEY (IMDbID) REFERENCES Series(IMDbID), \
                                                           UNIQUE(Season, IMDbID, UserID));')
    mycursor.close()
    mydb.close()

# Validate user
def validateUser(email, password):
    return users.validateUser(email, password)

# Insert user 
def insertUser(username, email, password):
    return users.insertUser(username, email, password)

# Change user's password
def changePassword(email, old_password, new_password):
    return users.changePassword(email, old_password, new_password)

# Add series to user's list
def addSeries(email, imdbID):
    return series.addSeries(email, imdbID)

# Remove series from user's list
def removeSeries(email, imdbID):
    return series.removeSeries(email, imdbID)

# Update series rating
def rateSeries(email, imdbID, rating):
    return series.rateSeries(email, imdbID, rating)

# Update series status
def updateSeriesStatus(email, imdbID, status, episodes):
    return series.updateSeriesStatus(email, imdbID, status, episodes)
