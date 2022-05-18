# Import the Flask application instance and port
from flask_app import app, port
#############################################################
# Import the error handler
import errorhandlers

# Import the routes
import routes


# Run Flask application instance
if __name__ == '__main__':
    app.run(host="10.0.2.10", port=port)
#############################################################
