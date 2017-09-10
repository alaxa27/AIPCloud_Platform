from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'junior data consulting'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CLOUDSQL_USER = 'admin'
CLOUDSQL_PASSWORD = 'Dfgdfg1.'
CLOUDSQL_DATABASE = 'aipcloud'
CLOUDSQL_CONNECTION_NAME = 'aipcloud-179518:europe-west1-c:aipcloud'
CLOUDSQL_IP = '35.187.165.12'
# instance.
app.config['CLOUDSQL_USER'] = CLOUDSQL_USER
app.config['CLOUDSQL_PASSWORD'] = CLOUDSQL_PASSWORD
app.config['CLOUDSQL_DATABASE'] = CLOUDSQL_DATABASE
#   "project:region:cloudsql-instance".
app.config['CLOUDSQL_CONNECTION_NAME'] = CLOUDSQL_CONNECTION_NAME

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://{user}:{password}@' + CLOUDSQL_IP + '/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
