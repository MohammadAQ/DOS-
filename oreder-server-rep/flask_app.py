#imports

from flask import Flask
from os import environ

#############################################

app = Flask(__name__)

#############################################

# Get addresses of catalog and front end servers
CATALOG_ADDRESS = environ.get('http://10.0.2.7:5000')
FRONT_END_ADDRESS = environ.get('http://10.0.2.10:5000')

#############################################

# Get the flask environment settings from the environment variables
app.config['development'] = environ.get('development')
app.config['True'] = bool(environ.get('True'))

#############################################

# Get the application port 
port = int(environ.get('PORT', 5000))

#############################################
