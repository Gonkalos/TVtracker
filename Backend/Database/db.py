import mysql.connector
import Utils.hash as myhash

class Database:

    # Class initialization
    def __init__(self, username, password, db_name):
        self.db_username = username
        self.db_password = password
        self.db_name = db_name

    # Create database 
    def createDatabase(self):
        # Create user
        mydb = mysql.connector.connect(host='localhost', user='root')
        mycursor = mydb.cursor()
        mycursor.execute('CREATE USER IF NOT EXISTS \'' + self.db_username + '\'@\'localhost\' IDENTIFIED BY \'' + self.db_password + '\';')
        mycursor.execute('GRANT ALL PRIVILEGES ON *.* TO \'' + self.db_username + '\'@\'localhost\';')
        mycursor.close()
        mydb.close()
        # Create database
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password)
        mycursor = mydb.cursor()
        mycursor.execute('CREATE DATABASE IF NOT EXISTS ' + self.db_name)
        mycursor.close()
        mydb.close()
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Create users table
        mycursor.execute('CREATE TABLE IF NOT EXISTS Users (UserID int NOT NULL AUTO_INCREMENT, \
                                                            Username varchar(45) NOT NULL, \
                                                            Email varchar(100) NOT NULL, \
                                                            Password varchar(200) NOT NULL, \
                                                            Token varchar(200), \
                                                            PRIMARY KEY (UserID));')
        #mydb.commit()
        # Create series table
        mycursor.execute('CREATE TABLE IF NOT EXISTS Series (IMDbID int NOT NULL, \
                                                             Status varchar(100) NOT NULL, \
                                                             Rating int NOT NULL, \
                                                             UserID int NOT NULL, \
                                                             PRIMARY KEY (IMDbID), \
                                                             FOREIGN KEY (UserID) REFERENCES Users(UserID));')
        #mydb.commit()
        # Create episodes table
        mycursor.execute('CREATE TABLE IF NOT EXISTS Episodes (Season int NOT NULL, \
                                                               EpisodesSeen int NOT NULL, \
                                                               UserID int NOT NULL, \
                                                               IMDbID int NOT NULL, \
                                                               FOREIGN KEY (UserID) REFERENCES Users(UserID), \
                                                               FOREIGN KEY (IMDbID) REFERENCES Series(IMDbID));')
        #mydb.commit()
        mycursor.close()
        mydb.close()

    # Insert user 
    def insertUser(self, username, email, password):
        hashed_password = myhash.hash_password(password) 
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate username
        mycursor.execute('SELECT * FROM Users WHERE Username = \'' + username + '\' LIMIT 1')
        result = mycursor.fetchone()
        if str(result) != 'None': return 'Error: The username already exists in the system.'
        # Validate email
        mycursor.execute('SELECT * FROM Users WHERE Email = \'' + email + '\' LIMIT 1')
        result = mycursor.fetchone()
        if str(result) != 'None': return 'Error: The email already exists in the system.'
        # Insert user
        mycursor.execute('INSERT INTO Users (Username, Email, Password) VALUES (\'' + username + '\', \'' + email + '\', \'' + hashed_password + '\');')
        mydb.commit()
        mycursor.close()
        mydb.close()
        return 'Sucess'

    # Validate user
    def validateUser(self, email, password):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate user
        mycursor.execute('SELECT Password FROM Users WHERE Email = \'' + email + '\' LIMIT 1')
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if myhash.verify_password(result[0], password): return 'Success' 
        else: return 'Error: The login parameters do not correspond to an existing user in the system.'

    # Check if user is logged in
    def checkLogin(self, email):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM Users WHERE Email = \'' + email + '\' AND Token IS NOT NULL LIMIT 1')
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if str(result) == 'None': return 'Success' 
        else: return 'Error: The user is already logged in the system.'

    # Update login token
    def updateToken(self, email, token):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE Users SET Token = \'' + token + '\' WHERE Email = \'' + email + '\';')
        mydb.commit()
        mycursor.close()
        mydb.close()

    # Logout user
    def logout(self, token):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM Users WHERE Token = \'' + token + '\' LIMIT 1')
        result = mycursor.fetchone()
        if (str(result) == 'None'):
            mycursor.close()
            mydb.close()
            return 'Error: The token is not in the system.'
        else:
            mycursor.execute('UPDATE Users SET Token = NULL WHERE Token = \'' + token + '\';')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        
    # Change user's password
    def changePassword(self, token, old_password, new_password):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate old password
        mycursor.execute('SELECT Password FROM Users WHERE Token = \'' + token + '\' LIMIT 1')
        result = mycursor.fetchone()
        if myhash.verify_password(result[0], old_password):
            hashed_password = myhash.hash_password(new_password) 
            mycursor.execute('UPDATE Users SET Password = \'' + hashed_password + '\' WHERE Token = \'' + token + '\';')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else: 
            mycursor.close()
            mydb.close()
            return 'Error: The inserted password is incorrect.'



        

    