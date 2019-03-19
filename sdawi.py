from flask import Flask, render_template, request, \
redirect, session, url_for
import psycopg2

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    login = session.get('login')
    password = session.get('password')
    if login == 'root' and password == '9965':
        connect = db_connect('root', '9965')
        cursor = connect.cursor()
        cursor.execute('SELECT datname FROM pg_database;')
        db_data = cursor.fetchall()
        cursor.close()
        connect.close()
        return render_template('sdawi.html', login=login, db_data=db_data)
    else:
        return render_template('login.html', error='Wrong login or password')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        session['login'] = login
        session['password'] = password
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('password', None)
    return redirect(url_for('index'))


@app.route('/get_db_info', methods=['POST'])
def get_db_info():
	db_name = request.form['db_name']
	print(db_name)
	return 'Hai'


def db_connect(user, password, host='localhost', db_name='postgres'):
    connection_string = 'dbname={} user={} password={} host={}'.format(
        db_name, user, password, host)
    try:
        connect = psycopg2.connect(connection_string)
        return connect
    except:
        return None
