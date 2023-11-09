import sqlite3

class Database:
    def __init__(self,database_name) -> None:  
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.connection = sqlite3.connect(database_name)
        # Create a cursor object to interact with the database
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, schema):
        # Create a table if it doesn't exist
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {schema}
            )
        ''')
        return 0

    def insert_data(self, table_name, data):
        """
        Inserts a row of data into the specified table.

        Args:
            table_name (str): The name of the table where data will be inserted.
            data (tuple): A tuple containing the values to be inserted.

        Returns:
            int: Returns 0 if the data was successfully inserted, or 1 if an error occurred.

        Raises:
            sqlite3.Error: If there is an error during the database operation.

        Example:
            # Insert a row into the 'users' table
            result = insert_data('users', ('John Doe', 30, 'john@example.com'))
            if result == 0:
                print("Data inserted successfully")
            else:
                print("Error occurred while inserting data")
        """
        try:
            self.cursor.execute(f'''
                INSERT INTO {table_name} VALUES ({','.join(['?']*len(data))})
            ''', data)
            # Commit changes to the database
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.insert_data.__name__} error occurred: {e}")
            return 1
        return 0
    
    def insert_multiple_data(self, table_name, data_list):
        """
        Insert multiple rows of data into the table.

        Args:
            table_name (str): Name of the table to insert data into.
            data_list (list of tuples): List of tuples, where each tuple represents a set of data to be inserted.

        Returns:
            int: 0 if successful, 1 if an error occurs.
        """
        try:
            self.cursor.executemany(f'''
                INSERT INTO {table_name} VALUES ({','.join(['?']*len(data_list[0]))})
            ''', data_list)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.insert_multiple_data.__name__} error occurred: {e}")
            return 1
        return 0

    def update_data(self, table_name, column_values, condition):
        """
        Update data in the specified table.

        Args:
            table_name (str): Name of the table to update.
            column_values (dict): A dictionary of column names and their corresponding values to be updated.
            condition (str): The condition for updating rows.

        Returns:
            int: 0 if the update is successful, 1 if an error occurs.

        Raises:
            sqlite3.Error: If an error occurs while executing the update query.

        Example:
            To update the 'name' and 'age' columns of a table where 'id' is 1, use:
            >>> update_data('your_table_name', {'name': 'John', 'age': 30}, 'id = 1')
        """
        try:
            set_values = ', '.join([f"{column} = ?" for column in column_values.keys()])
            values = list(column_values.values())
            self.cursor.execute(f'''
                UPDATE {table_name} SET {set_values} WHERE {condition}
            ''', values)
            # Commit changes to the database
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.update_data.__name__} error occurred: {e}")
            return 1
        return 0
    
    def update_multiple_rows(self, table_name, column_values_list, conditions_list):
        """
        Update data in the specified table for multiple rows.

        Args:
            table_name (str): Name of the table to update.
            column_values_list (list of dict): A list of dictionaries where each dictionary contains column names and their corresponding values to be updated.
            conditions_list (list of str): A list of conditions for updating rows.

        Returns:
            int: 0 if the update is successful, 1 if an error occurs.

        Raises:
            sqlite3.Error: If an error occurs while executing the update query.

        Example:
            To update the 'name' and 'age' columns of a table for multiple rows, use:
            >>> update_multiple_rows('your_table_name', [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}], ['id = 1', 'id = 2'])
        """
        try:
            for i in range(len(column_values_list)):
                set_values = ', '.join([f"{column} = ?" for column in column_values_list[i].keys()])
                values = list(column_values_list[i].values())
                condition = conditions_list[i]
                self.cursor.execute(f'''
                    UPDATE {table_name} SET {set_values} WHERE {condition}
                ''', values)

            # Commit changes to the database
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.update_multiple_rows.__name__} error occurred: {e}")
            return 1
        return 0


    def delete_data(self, table_name, condition):
        try:
            self.cursor.execute(f'''
                DELETE FROM {table_name} WHERE {condition}
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.delete_data.__name__} error occurred: {e}")
            return 1
        return 0
    
    def delete_multiple_rows(self, table_name, conditions_list):
        """
        Delete multiple rows from the specified table.

        Args:
            table_name (str): Name of the table to delete rows from.
            conditions_list (list of str): A list of conditions for deleting rows.

        Returns:
            int: 0 if the deletion is successful, 1 if an error occurs.

        Raises:
            sqlite3.Error: If an error occurs while executing the delete query.

        Example:
            To delete rows with IDs 1 and 2 from a table, use:
            >>> delete_multiple_rows('your_table_name', ['id = 1', 'id = 2'])
        """
        try:
            for condition in conditions_list:
                self.cursor.execute(f'''
                    DELETE FROM {table_name} WHERE {condition}
                ''')

            # Commit changes to the database
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An {self.delete_multiple_rows.__name__} error occurred: {e}")
            return 1
        return 0


    def select_data(self, table_name, columns=None, condition=None, join=None, order = None, limit = None):
        '''
        Retrieves the data from any table in our SQL Database
        '''
        if columns is None:
            columns = "*"

        query = f"SELECT {columns} FROM {table_name}"

        if join:
            query += f" {join}"

        if condition:
            query += f" WHERE {condition}"

        if order:
            order_coloumn,order_value = order
            query += f" ORDER BY {order_coloumn} {order_value.upper()}"

        if limit:
            query += f" LIMIT {limit}"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")
            return None

    def print_table_schema(self, table_name):
        try:
            self.cursor.execute(f'PRAGMA table_info({table_name})')
            schema_info = self.cursor.fetchall()

            print(f"Schema for table '{table_name}':")
            for column_info in schema_info:
                print(f"Column Name: {column_info[1]}, Type: {column_info[2]}, Nullable: {bool(column_info[3])}")
        except sqlite3.Error as e:
            print(f"An {self.print_table_schema.__name__} error occurred: {e}")

    def close_connection(self):
        # Close the database connection
        self.connection.close()