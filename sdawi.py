'''
SDAWI - Simple Database Access Web Interface.
Allows you to work with different types of databases
through a web interface.
'''

from flask import Flask, render_template, request
from flask import redirect, session, url_for, jsonify, g
import config
from dbcw import DBConnectionWrapper

app = Flask(__name__)

app.secret_key = config.secret_key


@app.before_request
def update_db_connection():
    '''
    Updates the database connection before each request,
    saving data from the session to the global (g) object.
    '''
    g.connection_args = dict()
    g.connection_args['engine'] = session.get('db_engine')
    g.connection_args['host'] = session.get('db_host')
    g.connection_args['port'] = session.get('db_port')
    g.connection_args['user'] = session.get('db_user')
    g.connection_args['password'] = session.get('db_password')
    # If all session data is NOT None, create new connection
    if all(g.connection_args.values()):
        if session.get('tried_to_login', False):
            try:
                print(g.connection_args)
                g.connection = DBConnectionWrapper(**g.connection_args)
            except Exception as exception:
                g.connection_error = exception


@app.errorhandler(404)
def page_not_found(error):
    '''
    Page not found (404) route.
    Redirects to the index route if requested page not found.
    '''
    return redirect(url_for('index'))


@app.route('/')
def index():
    '''
    Index route.
    Returns page template (login or interface) depending on session data.
    '''
    if g.get('connection', None) is not None:
        if g.connection.connection is not None:
            return render_template(
                'sdawi.html', title='Simple Database Access Web Interface')
    else:
        error = g.connection_error if session.get(
                                            'tried_to_login') else None
        return render_template('login.html', title='Login', error=error)


@app.route('/login', methods=['POST'])
def login():
    '''
    Login route.
    Saves the received data from the login form to the session
    and redirects to the index route.
    '''
    if request.method == 'POST':
        session['db_engine'] = request.form['db_engine']
        session['db_host'] = request.form['db_host']
        session['db_port'] = request.form['db_port']
        session['db_user'] = request.form['db_user']
        session['db_password'] = request.form['db_password']
        session['tried_to_login'] = True
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    '''
    Logout route.
    Deletes session data,
    closes db connection and redirects to the index route.
    '''
    session.pop('db_engine', None)
    session.pop('db_host', None)
    session.pop('db_port', None)
    session.pop('db_user', None)
    session.pop('db_password', None)
    session.pop('tried_to_login', False)
    g.connection_args = dict()
    if hasattr(g, 'connection'):
        g.connection.close()
        g.connection = None
    return redirect(url_for('index'))


@app.route('/get_db_info', methods=['POST'])
def get_db_info():
    '''
    Receives a request from a client in JSON format and returns
    a response in JSON format, depending on the type of request.

    To obtain the necessary data, a db_connection_wrapper is used to connect
    to different types of databases, which has built-in methods for returning
    the necessary data.

    Request types:
        - db_tree:
            Request database tree in JSON format that is read by the jsTree.
            More about jsTree: https://www.jstree.com/
        - table_data / raw_sql / table_structure / database_structure:
            Request table rows and columns in JSON format
            that is read by the Handsontable.
            More about Handsontable: https://handsontable.com/
        - None:
            Returns an error.
    '''
    data_request = request.get_json()
    data_type = data_request.get('type', None)
    # Check incoming request type and return response
    if data_type == 'db_tree':
        return build_db_tree(data_request['request_tables_list_for_db'])
    elif data_type == 'table_data':
        columns, rows = g.connection.get_table_data(data_request['db_name'],
                                                    data_request['table_name'])
        return build_table_data(columns, rows)
    elif data_type == 'raw_sql':
        try:
            selected_db = data_request.get('selected_db', None)
            columns, rows = g.connection.execute_query(
                data_request['query'], selected_db)
            if columns is None and rows is not None:
                return jsonify({'error': rows})
            elif columns is not None and rows is None:
                return jsonify({'success': columns})
            elif columns is None and rows is None:
                return jsonify({'error': 'Unknown error'})
            return build_table_data(columns, rows)
        except Exception as e:
            return jsonify({'error': str(e)})
    elif data_type == 'table_structure':
        columns, rows = g.connection.get_table_structure(
            data_request['db_name'], data_request['table_name'])
        return build_table_data(columns, rows)
    elif data_type == 'database_structure':
        columns, rows = g.connection.get_db_structure(data_request['db_name'])
        return build_table_data(columns, rows)
    else:
        return jsonify({'error': 'Unknown error'})


def build_db_tree(request_tables_list_for_db):
    '''
    Creates and returns database tree in JSON format
    that is read by the jsTree.
    More about jsTree: https://www.jstree.com/

    Args:
        request_tables_list_for_db (list): contains a list of databases
        for which it's necessary to return the list of tables
    '''
    db_names = g.connection.get_db_list()
    # Creates the main host node
    data = [{
        'id': g.connection_args['host'],
        'parent': '#',
        'text': g.connection_args['host'],
        'icon': '/static/sdawi/icons/host.png',
        'a_attr': {
            'type': 'host'
        }
    }]
    for db_name in db_names:
        # Creates database node
        row = {
            'id': db_name,
            'parent': g.connection_args['host'],
            'text': db_name,
            'icon': '/static/sdawi/icons/database.png',
            'a_attr': {
                'type': 'db'
            }
        }
        data.append(row)
        # Creates table nodes if they were requested
        if db_name in request_tables_list_for_db:
            for table in g.connection.get_tables_list(db_name):
                row = {
                    'id': table[0],
                    'parent': db_name,
                    'text': table[0],
                    'icon': '/static/sdawi/icons/table.png',
                    'a_attr': {
                        'type': 'table'
                    }
                }
                data.append(row)
    return jsonify(data)


def build_table_data(columns, rows):
    '''
    Creates and returns table rows and columns in JSON format
    that is read by the Handsontable.
    More about Handsontable: https://handsontable.com/

    Args:
        columns (list): list of columns for the table
        rows (list): list of rows (tuples) for the table
    '''
    # If there are no rows in the table,
    # then 1 row will be returned with the data that the table is empty
    if len(rows) == 0:
        rows = [(['Empty table'] for k in columns)]
    data = {
        'colHeaders': columns,
        'columns': [{'data': column_name} for column_name in columns],
        'rows': [{k: v for (k, v) in zip(columns, row)} for row in rows]
    }
    return jsonify(data)


if __name__ == '__main__':
    # Loads the selected config when the application starts
    app.config.from_object(config.DevelopmentConfig)
    app.run()
