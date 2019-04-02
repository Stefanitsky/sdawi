import json


class DBConnectionWrapper:
    '''
    Database connection wrapper.
    Allows you to connect to different types of databases
    and contains methods for getting the necessary data.
    
    Supported engines:
        - PostgreSQL
        - MySQL

    Args:
        engine (string): engine name. Default = 'postgres'.
        Can be:
            - postgres
            - mysql
        kwargs (**kwargs): connection settings, depends on the engine.
        Base settings:
            - host (string): host address
            - port (string, optional): host port
            - user (string): db username
            - password (string): db password
            - dbname (string, optional): database name

    Attributes:
        settings (dict): connection settings
        engine (string): engine name
        engine_module (obj): engine module
        queries (dict): sql queries for methods, depends on engine
        connection (obj): created connection obj or None
        cursor (obj): cursor obj of the connection obj or None
        connection_error (string): error message on connection error

    Examples:
        - PostgreSQL
            connection = DBConnectionWrapper(
            host='localhost', user='root', password='1234')
        - MySQL
            connection = DBConnectionWrapper(
            engine='mysql', host='localhost', user='root', password='1234')
    '''

    def _check_settings(self):
        '''
        Checks settings to avoid unexpected connection errors.
        '''
        if self.engine == 'postgres':
            if 'dbname' not in self.settings:
                # Adds the standard db name for the pgsql connection
                # if it has not been specified before
                self.settings['dbname'] = 'postgres'
        elif self.engine == 'mysql':
            # Changes the password key in the settings,
            # because MySQL connection module requires 'passwd' key
            self.settings['passwd'] = self.settings.pop('password')

    def connect(self):
        '''
        Creates a connection and imports the required database module
        for the connection, depending on the selected engine.

        Raises:
            ImportError: if the engine module is not installed
            NotImplementedError: if the engine is not supported
        '''
        if self.engine == 'postgres':
            try:
                import psycopg2
                self.engine_module = psycopg2
            except ImportError:
                self.connection_error = 'psycopg2 module not found'
            try:
                self.connection = psycopg2.connect(**self.settings)
            except psycopg2.Error as e:
                self.connection_error = e
                self.connection = None
        elif self.engine == 'mysql':
            try:
                import mysql.connector
                self.engine_module = mysql.connector
                try:
                    self.connection = mysql.connector.connect(**self.settings)
                except mysql.connector.Error as e:
                    self.connection_error = e
                    self.connection = None
            except ImportError:
                self.connection_error = 'mysql module not found!'
        else:
            raise NotImplementedError(
                'Database engine {} not implemented!'.format(self.engine))
        if self.connection:
            self.cursor = self.connection.cursor()

    def __init__(self, engine='postgres', **kwargs):
        '''
        Called when a class object is created.
        Performs the initial configuration and creates a connection.
        '''
        self.settings = {}
        self.engine_module = None
        self.settings.update(**kwargs)
        self.engine = self.settings.pop('engine', engine)
        # Loads the necessary queries for the db depending on the engine
        with open('db_queries.json') as f:
            self.queries = json.load(f)[self.engine]
        self._check_settings()
        self.connection = None
        self.cursor = None
        self.connect()

    def close(self):
        '''
        Closes the connection.
        '''
        self.cursor.close()
        self.connection.close()

    def fetch(self):
        '''
        Fetches data from the cursor.

        Returns:
            The fetched data as a list of tuples.
        '''
        return self.cursor.fetchall()

    def update_current_connected_db(self, db_name):
        '''
        Updates current connected database and creates a new connection.

        Args:
            db_name (string): database name for check to update
        '''
        if self.engine == 'postgres':
            if db_name != self.settings['dbname']:
                self.settings['dbname'] = db_name
                self.connect()
        elif self.engine == 'mysql':
            self.settings['db'] = db_name
            self.connect()

    def get_current_connected_db(self):
        '''
        Returns current connected database name (string).
        '''
        if self.engine == 'postgres':
            return self.settings['dbname']
        elif self.engine == 'mysql':
            return self.settings.get('db', None)

    def execute_query(self, query, db_name=None):
        '''
        Executes a query to the database.

        Args:
            db_name (string, optional): name of the database
            in which the query will be executed. Important to MySQL,
            because it executes "USE db_name" query.

        Returns:
            columns (list): list with column names (string)
            rows (list): list of rows (tuples)

        Raises:
            Exception: if no database connection
        '''
        if not self.connection:
            raise Exception('No database connection!')
        if self.engine == 'postgres':
            self.cursor.execute(query)
            columns = [name[0] for name in self.cursor.description]
            return columns, self.fetch()
        if self.engine == 'mysql':
            if db_name is not None:
                self.cursor.execute("USE {};".format(db_name))
            self.cursor.execute(query)
            columns = [name[0] for name in self.cursor.description]
            return columns, self.fetch()

    def get_db_list(self):
        '''
        Returns a list of databases,
        performing the necessary database query depending on the engine.
        '''
        result = self.execute_query(self.queries['get_db_list'])
        return [db_name[0] for db_name in result[1]]

    def get_tables_list(self, db_name):
        '''
        Returns a list of tables from the database,
        performing the necessary database query depending on the engine.

        Args:
            db_name (string): db name from which need to return
            the list of tables
        '''
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            if self.get_current_connected_db() == db_name:
                return self.execute_query(self.queries['get_tables_list'])[1]
            else:
                # Creates a new connection with the specified db name
                # and requests a list of tables from it
                temp_settings = self.settings
                temp_settings['dbname'] = db_name
                temp_settings['engine'] = 'postgres'
                temp_connection = DBConnectionWrapper(temp_settings)
                return temp_connection.get_tables_list(db_name)
        elif self.engine == 'mysql':
            self.cursor.execute("USE {};".format(db_name))
            result = self.execute_query(self.queries['get_tables_list'])
            return result[1]

    def get_table_data(self, db_name, table_name):
        '''
        Returns data of a table,
        performing the necessary database query depending on the engine.

        Args:
            db_name (string): db name to which the table belongs
            table_name (string): table name from which to get data

        Returns:
            Returns the data received from the method execute_query(),
            which returns:
                columns (list): list with column names (string)
                rows (list): list of rows (tuples)
        '''
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres' or self.engine == 'mysql':
            return self.execute_query(self.queries['get_table_data']
                .format(table_name))

    def get_db_structure(self, db_name):
        '''
        Returns database structure,
        performing the necessary database query depending on the engine.

        Args:
            db_name (string): database name from which to get structure

        Returns:
            Returns the data received from the method execute_query(),
            which returns:
                columns (list): list with column names (string)
                rows (list): list of rows (tuples)
        '''
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            return self.execute_query(self.queries['get_db_structure'])
        elif self.engine == 'mysql':
            return self.execute_query(self.queries['get_db_structure'])

    def get_table_structure(self, db_name, table_name):
        '''
        Returns table structure,
        performing the necessary database query depending on the engine.

        Args:
            db_name (string): db name to which the table belongs
            table_name (string): table name from which to get structure

        Returns:
            Returns the data received from the method execute_query(),
            which returns:
                columns (list): list with column names (string)
                rows (list): list of rows (tuples)
        '''
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            return self.execute_query(self.queries['get_table_structure']
                .format(table_name))
        elif self.engine == 'mysql':
            return self.execute_query(self.queries['get_table_structure']
                .format(table_name))
