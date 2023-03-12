import mysql.connector
from mysql.connector import errorcode


class DbUtils:
    @staticmethod
    def get_connection(user, password, host, database):
        # Try to connect to the database with the given credentials
        # If the connection is successful, return the connection
        # If the connection is unsuccessful, return None
        try:
            connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=database
            )
            return connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None

    @staticmethod
    def get_all_databases(connection):
        try:
            # Get all databases and return them
            cursor = connection.cursor()

            cursor.execute("SHOW DATABASES")
            result = cursor.fetchall()

            databases = [database[0] for database in result]

            # Close the connection
            cursor.close()

            return databases
        except mysql.connector.Error as err:
            print(err)
            return None

    @staticmethod
    def get_all_tables(connection):
        try:
            # Get all tables and return them
            cursor = connection.cursor()

            cursor.execute("SHOW TABLES")
            result = cursor.fetchall()

            tables = [table[0] for table in result]

            # Close the connection
            cursor.close()

            return tables
        except mysql.connector.Error as err:
            print(err)
            return None

    @staticmethod
    def get_table(connection, table):
        try:
            # Get every row from the table and return them
            cursor = connection.cursor()
            print(table)

            cursor.execute("SELECT * FROM {}".format(table))
            content = cursor.fetchall()
            headers = [header[0] for header in cursor.description]

            # Close the connection
            cursor.close()

            return headers, content
        except mysql.connector.Error as err:
            print(err)
            return None

    @staticmethod
    def create_database(connection, database):
        try:
            # Create a new database
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE {}".format(database))

            # Close the connection
            cursor.close()

            return database
        except mysql.connector.Error as err:
            print(err)
            return None

    @staticmethod
    def delete_database(connection, database):
        try:
            # Delete a database
            cursor = connection.cursor()

            cursor.execute("DROP DATABASE {}".format(database))

            # Close the connection
            cursor.close()

            return True
        except mysql.connector.Error as err:
            print(err)
            return None

    @staticmethod
    def create_table(connection, table, columns):
        try:
            # Create a new table
            cursor = connection.cursor()

            executed_string = "CREATE TABLE {} ({})".format(table, columns)

            cursor.execute("CREATE TABLE {} ({})".format(table, columns))

            # Close the connection
            cursor.close()

            return table
        except mysql.connector.Error as err:
            print(err)
            return [None, err]

    @staticmethod
    def delete_table(connection, table):
        try:
            # Delete a table
            cursor = connection.cursor()

            cursor.execute("DROP TABLE {}".format(table))

            # Close the connection
            cursor.close()

            return True
        except mysql.connector.Error as err:
            print(err)
            return None
