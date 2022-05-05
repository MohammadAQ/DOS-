# Import Flask application instance and port
from flask_app import app, port


#############################################
# Import error handler 
import errorhandlers


#############################################
# Import routes
import routes


#############################################
# Run Flask application instance
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
    
    
#############################################
