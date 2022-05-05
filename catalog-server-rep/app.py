# Import instance and port
from flask_app import app, port
############################################################

# Import error handler
import errorhandles
############################################################
# Import routes
import routes
############################################################
# This creates the database file if it does not exist
#and adds the books to it 
from database import create_database
create_database()

############################################################
# Run Flask application instance
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
############################################################
