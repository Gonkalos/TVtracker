import mysql.connector
import Utils.hash as myhash
import Utils.configs as configs

# Validate user
def validateUser(email, password):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    # Validate user
    mycursor.execute(f'SELECT Password FROM Users WHERE Email = \'{email}\' LIMIT 1')
    result = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if (str(result) != 'None'):
        if myhash.verify_password(result[0], password): return True 
        else: return False
    else: return False

# Insert user 
def insertUser(username, email, password):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
    mycursor = mydb.cursor()
    # Validate username
    mycursor.execute(f'SELECT * FROM Users WHERE Username = \'{username}\' LIMIT 1')
    result = str(mycursor.fetchone())
    if result == 'None':
        # Validate email
        mycursor.execute(f'SELECT * FROM Users WHERE Email = \'{email}\' LIMIT 1')
        result = str(mycursor.fetchone())
        if result == 'None':
            # Insert user
            hashed_password = myhash.hash_password(password) 
            mycursor.execute(f'INSERT INTO Users (Username, Email, Password) VALUES (\'{username}\', \'{email}\', \'{hashed_password}\');')
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 'Success'
        else: 
            mycursor.close()
            mydb.close()
            return 'Error: Username or email already in use.'
    else:
        mycursor.close()
        mydb.close() 
        return 'Error: Username or email already in use.'
        
# Change user's password
def changePassword(email, old_password, new_password):
    mydb = mysql.connector.connect(host='localhost', user=configs.DB_USERNAME, passwd=configs.DB_PASSWORD, database=configs.DB_NAME)
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