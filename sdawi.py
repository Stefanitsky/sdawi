'''
SDAWI - Simple Database Access Web Interface.
'''


from flask import Flask, render_template, request, \
redirect, session, url_for, jsonify, g
import psycopg2
import config


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def test():
    g.db_user = session.get('db_user')
    g.db_password = session.get('db_password')
    g.db_name = session.get('db_name', 'postgres')
    g.db_host = session.get('db_host', 'localhost')


@app.route('/')
def index():
    '''
	Main route.
	Returns authorization form or interface template depending on session.
	'''
    if get_db_connect() is not None:
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
    if hasattr(g, 'db_connect'):
        g.db_connect.close()
        g.db_connect = None
    return redirect(url_for('index'))


@app.route('/get_db_info', methods=['POST'])
def get_db_info():
    data_request = request.get_json()
    data_type = data_request.get('type', None)
    if data_type == 'db_tree':
    	return get_db_tree(data_request)
    else:
    	return 'Error'


def get_db_tree(data_request):
	db_names = (get_db_query_result(
                "SELECT datname FROM pg_database WHERE datistemplate = 'f';"))
	tables_for = data_request.get('get_tables_for_db')
	data = {}
	for db_name in db_names:
		data[db_name] = get_db_tables(db_name) if db_name in tables_for else []
	print('[get_db_tree]:', data)
	data = jsonify(data)
	return data


def get_db_tables(db_name):
	new_db_connect = db_connect(db_name)
	query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
	result = get_db_query_result(query, new_db_connect)
	new_db_connect.close()
	return result

# TODO: external db tools file
def db_connect(db_name='postgres'):
    connection_string = 'dbname={} user={} password={} host={}'.format(
        db_name, g.db_user, g.db_password, g.db_host)
    try:
        connect = psycopg2.connect(connection_string)
        return connect
    except psycopg2.Error:
        return None


def get_db_connect():
    if not hasattr(g, 'db_connect'):
        g.db_connect = db_connect(g.db_name)
    return g.db_connect


def db_close(exception):
    if hasattr(g, 'db_connect'):
        g.db_connect.close()


def get_db_query_result(query, db_connection=None):
    cursor = get_db_connect().cursor() if db_connection is None else db_connection.cursor()
    cursor.execute(query)
    # Sets value as value, not as tuple
    result = [value[0] for value in cursor.fetchall()]
    cursor.close()
    return result


if __name__ == '__main__':
    app.config.from_object(config.DevelopmentConfig)
    app.run()