import mysql.connector
import sys

### Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#Rocketman84",
    database="blockchain"
)
cursor = connection.cursor()

### Commands

def TruncatePendingTransactions(tableName):
    ''''
    :param tableName: <string> Name of the table in MySQL db to truncate.
    '''
    sql_query = f"DELETE FROM {tableName}"
    cursor.execute(sql_query)
    connection.commit()
    
### Executing command
if (len(sys.argv) > 1):
    command = sys.argv[1]
    if (command == 'truncate'):
        if (len(sys.argv) > 2):
            TruncatePendingTransactions(sys.argv[2])
    
        else:
            print("Please provide a table name to truncate as a second argument.")

else:
    print("Please provide a command as the first argument.")

### close the cursor and connection
cursor.close()
connection.close()
