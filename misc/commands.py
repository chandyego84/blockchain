import mysql.connector
import sys

### Necessary arguments to make mysql connection
password = ""
database = ""

### Commands
def TruncatePendingTransactions(tableName):
    ''''
    :param tableName: <string> Name of the table in MySQL db to truncate.
    '''
    ### Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database=database
    )
    cursor = connection.cursor()

    ### Execute truncating
    sql_query = f"TRUNCATE {tableName}"
    cursor.execute(sql_query)
    connection.commit()

    ### close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    ### Executing command
    if (len(sys.argv) > 1):
        # calling the script with command
        command = sys.argv[1]
        if (command == 'truncate'):
            if (len(sys.argv) > 3):
                password = sys.argv[2]
                database = sys.argv[3]
                TruncatePendingTransactions(sys.argv[4])
        
            else:
                print("Please make sure to provide the arguments: password, database, table")

    else:
        print("Please provide a command to execute.")