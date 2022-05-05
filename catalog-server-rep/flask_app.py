from flask import Flask
from os import environ
############################################################################
# Flask application instance
app = Flask(__name__)
############################################################################
# Get addresses of front end and order servers from the environment variables
ORDER_ADDRESS = environ.get('http://192.168.1.11:5000 | http://192.168.1.16:5000')
FRONT_END_ADDRESS = environ.get('http://192.168.1.15:5000')
CATALOG_ADDRESSES = environ.get('http://192.168.1.13:5000 | http://192.168.1.17:5000')
if CATALOG_ADDRESSES is None or CATALOG_ADDRESSES.strip() == '':
    CATALOG_ADDRESSES = []
else:
    CATALOG_ADDRESSES = CATALOG_ADDRESSES.split('|')
    
    
############################################################################
# Get the application port from the environment variables
port = int(environ.get('PORT', 5000))
    

############################################################################
# Get the flask environment settings from the environment variables
app.config['development'] = environ.get('development')
app.config['True'] = bool(environ.get('True'))


