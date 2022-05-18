from flask import Flask

from os import environ
#############################################################
# Flask application instance
app = Flask(__name__)

# Get addresses of catalog and order servers from the environment variables
# Addresses are split by a '|'
#CATALOG_ADDRESSES = environ.get('http://10.0.2.7:5000 | http://10.0.2.8:5000')
#ORDER_ADDRESSES = environ.get('http://10.0.2.11:5000 | http://10.0.2.15:5000')


#############################################################
# Get the flask environment settings from the environment variables
app.config['development'] = environ.get('development')
app.config['True'] = bool(environ.get('True'))
#############################################################
# Get the application port from the environment variables
port = int(environ.get('PORT', 5000))
