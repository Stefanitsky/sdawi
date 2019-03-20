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
    if get_db_connect():
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
    data = request.get_json()
    print(data)
    return get_db_tree()


# TODO: parse JSON data from request and return db tree as JSON
def get_db_tree():
	return jsonify(
            get_db_query_result(
                "SELECT datname FROM pg_database WHERE datistemplate = 'f';"))


# TODO: external db tools file
def db_connect():
    connection_string = 'dbname={} user={} password={} host={}'.format(
        g.db_name, g.db_user, g.db_password, g.db_host)
    try:
        connect = psycopg2.connect(connection_string)
        return connect
    except psycopg2.ProgrammingError as e:
        print(e.pgerror)
        return None


def get_db_connect():
    if not hasattr(g, 'db_connect'):
        g.db_connect = db_connect()
    return g.db_connect


@app.teardown_appcontext
def db_close(exception):
    if hasattr(g, 'db_connect'):
        g.db_connect.close()


def get_db_query_result(query):
    cursor = get_db_connect().cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


if __name__ == '__main__':
    app.config.from_object(config.DevelopmentConfig)
    app.run()