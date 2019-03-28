'''
SDAWI - Simple Database Access Web Interface.
'''

from flask import Flask, render_template, request
from flask import redirect, session, url_for, jsonify, g
import config
from dbcw import DBConnectionWrapper

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def before_request():
    update_db_connection()


def update_db_connection():
    g.db_user = session.get('db_user')
    g.db_password = session.get('db_password')
    g.db_name = session.get('db_name', 'postgres')
    g.db_host = session.get('db_host', 'localhost')
    g.connection = DBConnectionWrapper(
            dbname=g.db_name,
            user=g.db_user,
            password=g.db_password,
            host=g.db_host)


@app.route('/')
def index():
    '''
    Main route.
    Returns authorization form or interface template depending on session.
    '''
    if g.connection.connection:
        return render_template('sdawi.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    '''
    Login route.
    Checks the entered data from the authorization form
    and redirects to the main route.
    '''
    if request.method == 'POST':
        db_user = request.form['db_user']
        db_password = request.form['db_password']
        session['db_user'] = db_user
        session['db_password'] = db_password
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    '''
    Logout route.
    Deletes session data, closes db connection and redirects to the main route.
    '''
    session.pop('db_user', None)
    session.pop('db_password', None)
    session.pop('db_name', None)
    session.pop('db_host', None)
    if g.connection:
        g.connection.close()
        g.connection = None
    return redirect(url_for('index'))


@app.route('/get_db_info', methods=['POST'])
def get_db_info():
    # print(g.connection.get_current_connected_db())
    return get_response(request.get_json())


def get_response(data_request):
    data_type = data_request.get('type', None)
    if data_request.get('db_name', None) is not None:
        session['db_name'] = data_request['db_name']
        update_db_connection()
    if data_type == 'db_tree':
        result = g.connection.get_db_list()
        return build_db_tree(result,
                             data_request['request_tables_list_for_db'])
    elif data_type == 'table_data':
        columns, rows = g.connection.get_table_data(data_request['db_name'],
                                                    data_request['table_name'])
        return build_table_data(columns, rows)
    elif data_type == 'raw_sql':
        try:
            columns, rows = g.connection.execute_query(data_request['query'])
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


def build_db_tree(db_names, request_tables_list_for_db):
    data = [{'id': g.db_host, 'parent': '#',
        'text': g.db_host, 'a_attr': {'type': 'host'}}]
    for db_name in db_names:
        # database row
        row = {
            'id': db_name,
            'parent': g.db_host,
            'text': db_name,
            'a_attr': {
                'type': 'db'
            }
        }
        data.append(row)
        # tables row(s)
        if db_name in request_tables_list_for_db:
            for table in g.connection.get_tables_list(db_name):
                row = {
                    'id': table[0],
                    'parent': db_name,
                    'text': table[0],
                    'a_attr': {
                        'type': 'table'
                    }
                }
                data.append(row)
    return jsonify(data)


def build_table_data(columns, rows):
    print(columns, rows)
    data = {
        'colHeaders': columns,
        'columns': [{
            'data': column_name
        } for column_name in columns],
        'rows': [{k: v
                  for (k, v) in zip(columns, row)} for row in rows]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.config.from_object(config.DevelopmentConfig)
    app.run()