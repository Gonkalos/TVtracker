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
        mycursor.execute(f'CREATE USER IF NOT EXISTS \'{self.db_username}\'@\'localhost\' IDENTIFIED BY \'{self.db_password}\';')
        mycursor.execute(f'GRANT ALL PRIVILEGES ON *.* TO \'{self.db_username}\'@\'localhost\';')
        mycursor.close()
        mydb.close()
        # Create database
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password)
        mycursor = mydb.cursor()
        mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_name}')
        mycursor.close()
        mydb.close()
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Create users table
        mycursor.execute('CREATE TABLE IF NOT EXISTS Users (UserID int NOT NULL AUTO_INCREMENT, \
                                                            Username varchar(45) NOT NULL, \
                                                            Email varchar(100) NOT NULL, \
                                                            Password varchar(200) NOT NULL, \
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

    # Validate user
    def validateUser(self, email, password):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate user
        mycursor.execute(f'SELECT Password FROM Users WHERE Email = \'{email}\' LIMIT 1')
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if myhash.verify_password(result[0], password): return True 
        else: return False

    # Insert user 
    def insertUser(self, username, email, password):
        hashed_password = myhash.hash_password(password) 
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate username
        mycursor.execute(f'SELECT * FROM Users WHERE Username = \'{username}\' LIMIT 1')
        result = mycursor.fetchone()
        if str(result) != 'None': return 'Error: Username or email already in use.'
        # Validate email
        mycursor.execute(f'SELECT * FROM Users WHERE Email = \'{email}\' LIMIT 1')
        result = mycursor.fetchone()
        if str(result) != 'None': return 'Error: Username or email already in use.'
        # Insert user
        mycursor.execute(f'INSERT INTO Users (Username, Email, Password) VALUES (\'{username}\', \'{email}\', \'{hashed_password}\');')
        mydb.commit()
        mycursor.close()
        mydb.close()
        return 'Success'
        
    # Change user's password
    def changePassword(self, email, old_password, new_password):
        mydb = mysql.connector.connect(host='localhost', user=self.db_username, passwd=self.db_password, database=self.db_name)
        mycursor = mydb.cursor()
        # Validate old password
        mycursor.execute(f'SELECT Password FROM Users WHERE Email = \'{email}\' LIMIT 1')
        result = mycursor.fetchone()
        if myhash.verify_password(result[0], old_password):
            hashed_password = myhash.hash_password(new_password) 
            mycursor.execute(f'UPDATE Users SET Password = \'{hashed_password}\' WHERE Email = \'{email}\';')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else: 
            mycursor.close()
            mydb.close()
            return 'Error: Incorrect password.'