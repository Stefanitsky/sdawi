'''
SDAWI - Simple Database Access Web Interface.
'''


from flask import Flask, render_template, request, \
redirect, session, url_for, jsonify, g
import config
from dbcw import DBConnectionWrapper

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def before_request():
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
    Checks the entered data from the authorization form and redirects to the main
    route.
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
    data_request = request.get_json()
    data_type = data_request.get('type', None)
    if data_type == 'db_tree':
        return build_db_tree(data_request)
    elif data_type == 'table_data':
        return build_table_data(data_request)
    else:
        return 'Error'


def build_db_tree(data_request):
    db_names = g.connection.get_db_list()
    data = {
        db_name: g.connection.get_tables_list(db_name)
        if db_name in data_request['request_tables_list_for_db'] else []
        for db_name in db_names
    }
    return jsonify(data)


def build_table_data(data_request):
    column_keys = ['id', 'name', 'field']
    db_name = data_request['db_name']
    table_name = data_request['table_name']
    columns = g.connection.get_table_columns(table_name)
    rows = g.connection.get_table_rows(table_name)
    data = {
        'columns': [{k: column_name
                     for k in column_keys} for column_name in columns],
        'rows': [{k: v for (k, v) in zip(columns, row)} for row in rows]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.config.from_object(config.DevelopmentConfig)
    app.run()