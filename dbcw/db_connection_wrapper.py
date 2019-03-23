class DBConnectionWrapper:
    '''
    Database connection wrapper.
    Allows you to connect to different types of databases.
    Supported engines:
        - PostgreSQL
    '''
    settings = {}  # type: dict

    def _check_settings(self):
        if self.engine == 'postgres':
            if 'dbname' not in self.settings:
                self.settings['dbname'] = 'postgres'

    def connect(self):
        if self.engine == 'postgres':
            try:
                import psycopg2
            except ImportError:
                raise ValueError('psycopg2 module not found')
            try:
                self.connection = psycopg2.connect(**self.settings)
            except psycopg2.Error as e:
                print(e)
                self.connection = None
        else:
            raise NotImplementedError(
                'Database engine {} not implemented!'.format(self.engine))
        if self.connection:
            self.cursor = self.connection.cursor()

    def __init__(self, engine='postgres', **kwargs):
        self.settings.update(**kwargs)
        self.engine = self.settings.pop('engine', engine)
        self._check_settings()
        self.connection = None
        self.cursor = None
        self.connect()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch(self):
        return self.cursor.fetchall()

    def execute_query(self, query):
        if not self.connection:
            return 'No database connection'
        self.cursor.execute(query)
        return self.fetch()

    def get_db_list(self):
        if self.engine == 'postgres':
            result = self.execute_query(
                "SELECT datname FROM pg_database WHERE datistemplate = 'f';")
            return [db_name[0] for db_name in result]

    def get_tables_list(self, db_name):
        if self.engine == 'postgres':
            if db_name == self.settings['dbname']:
                return self.execute_query(
                    "SELECT table_name FROM information_schema.tables \
                    WHERE table_schema = 'public';")
            else:
                settings_temp = self.settings
                settings_temp['dbname'] = db_name
                connection_temp = DBConnectionWrapper(self.engine,
                                                      **settings_temp)
                return connection_temp.get_tables_list(db_name)
                connection_temp.close()
                del connection_temp
        else:
            return 'Unknown database engine!'

    def get_table_rows(self, table_name):
        if self.engine == 'postgres':
            return self.execute_query('SELECT * FROM {};'.format(table_name))

    def get_table_columns(self, table_name):
        if self.engine == 'postgres':
            result = self.execute_query(
                "SELECT column_name FROM information_schema.columns \
                WHERE table_name = '{}';".format(table_name))
            return [column_name[0] for column_name in result]
