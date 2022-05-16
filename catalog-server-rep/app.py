######### get ready the instance and port
from flask_app import app, port
###########

########## Import error handler instance
import errorhandles
###########

# Import routes
import routes
###########

########### bring data base and if not existed create new
from database import create_database
create_database()

###########
# Run Flask application on local host and port number
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5011)
###########

