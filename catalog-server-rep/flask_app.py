from flask import Flask
from os import environ

##########
#####Flask application instance
app = Flask(__name__)
#######################
#### addresses of front  and order servers from the environment variables
ORDER_ADDRESS = environ.get('http://127.0.0.1:5003 | http://127.0.0.1:5022')
FRONT_END_ADDRESS = environ.get('http://127.0.0.1:5002')
CATALOG_ADDRESSES = environ.get('http://127.0.0.1:5000 | http://127.0.0.1:5011')
if CATALOG_ADDRESSES is None or CATALOG_ADDRESSES.strip() == '':
    CATALOG_ADDRESSES = []
else:
    CATALOG_ADDRESSES = CATALOG_ADDRESSES.split('|')

##################
###Get port from the environment variables
port = int(environ.get('PORT', 5011))

################################
######flask environment settings from  environment variables
app.config['development'] = environ.get('development')
app.config['True'] = bool(environ.get('True'))


