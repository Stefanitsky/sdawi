class DBConnectionWrapper:
    '''
    Database connection wrapper.
    Allows you to connect to different types of databases.
    Supported engines:
        - PostgreSQL
    '''
    def _check_settings(self):
        if self.engine == 'postgres':
            if 'dbname' not in self.settings:
                self.settings['dbname'] = 'postgres'
        elif self.engine == 'mysql':
            self.settings['passwd'] = self.settings.pop('password')

    def connect(self):
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
        self.settings = {}
        self.engine_module = None
        self.settings.update(**kwargs)
        self.engine = self.settings.pop('engine', engine)
        self._check_settings()
        print(self.settings)
        self.connection = None
        self.cursor = None
        self.connect()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch(self):
        return self.cursor.fetchall()

    def update_current_connected_db(self, db_name):
        if db_name != self.settings['dbname']:
            self.settings['dbname'] = db_name
            self.connect()

    def get_current_connected_db(self):
        return self.settings['dbname']

    def execute_query(self, query):
        if not self.connection:
            raise Exception('No database connection!')
        if self.engine == 'postgres':
            self.cursor.execute(query)
            columns = [name[0] for name in self.cursor.description]
            return columns, self.fetch()

    def get_db_list(self):
        if self.engine == 'postgres':
            result = self.execute_query(
                "SELECT datname FROM pg_database WHERE datistemplate = 'f';")
            return [db_name[0] for db_name in result[1]]
        if self.engine == 'mysql':
            self.cursor.execute("SHOW DATABASES")
            print('DB_LIST:', self.cursor)
            return self.cursor

    def get_tables_list(self, db_name):
        if self.engine == 'postgres':
            if self.get_current_connected_db() == db_name:
                return self.execute_query(
                    "SELECT table_name FROM information_schema.tables \
                    WHERE table_schema = 'public';")[1]
            else:
                temp_settings = self.settings
                temp_settings['dbname'] = db_name
                temp_settings['engine'] = 'postgres'
                temp_connection = DBConnectionWrapper(temp_settings)
                return temp_connection.get_tables_list(db_name)
        elif self.engine == 'mysql':
            self.cursor.execute('USE {}'.format(db_name))
            self.cursor.execute('SHOW TABLES')
            return self.cursor
        else:
            raise Exception('Unknown database engine!')

    def get_table_data(self, db_name, table_name):
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            return self.execute_query('SELECT * FROM {};'.format(table_name))

    def get_db_structure(self, db_name):
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            return self.execute_query(
                "SELECT * FROM pg_tables where schemaname = 'public';")

    def get_table_structure(self, db_name, table_name):
        self.update_current_connected_db(db_name)
        if self.engine == 'postgres':
            return self.execute_query(
                "SELECT * FROM information_schema.columns \
                WHERE table_name = '{}'".format(table_name))
