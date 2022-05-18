from flask import Flask
from os import environ
##########
#####Flask application instance
app = Flask(__name__)
#######################
#### addresses of front  and order servers from the environment variables
#ORDER_ADDRESS = ('http://10.0.2.11:5000 | http://10.0.2.15:5000').split(' | ')
#FRONT_END_ADDRESS = ('http://10.0.2.10:5000')
#CATALOG_ADDRESSES = ('http://10.0.2.7:5000 | http://10.0.2.8:5000').split(' | ')
#if CATALOG_ADDRESSES is None or CATALOG_ADDRESSES.strip() == '':
#    CATALOG_ADDRESSES = []
#else:
#    CATALOG_ADDRESSES = CATALOG_ADDRESSES.split('|')
    
    
##################
###Get port from the environment variables
port = int(environ.get('PORT', 5000))
    

################################
######flask environment settings from  environment variables
app.config['development'] = environ.get('development')
app.config['True'] = bool(environ.get('True'))


