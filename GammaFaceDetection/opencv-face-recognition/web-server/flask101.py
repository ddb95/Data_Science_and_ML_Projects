# First we imported the Flask class. An instance of this class will be our WSGI application.
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Love, Welcome to Index Page'


@app.route('/details')
def details():
    return 'Details Page Baby'


'''
You can add variable sections to a URL by marking sections with <variable_name>. 
Your function then receives the <variable_name> as a keyword argument. 
Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>.
'''


@app.route('/users/<string:username>/<int:age>')
def variables(username, age):
    return "Username: {} and Age: {}".format(username, age)


'''
    HTTP methods [GET and POST]
'''


@app.route('/methods', methods=['GET', 'POST'])
def loginMethods():
    if request.method == 'POST':
        return 'POST'
    else:
        return 'GET'
