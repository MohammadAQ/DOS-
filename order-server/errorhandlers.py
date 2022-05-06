from flask_app import app



@app.errorhandler(404)
def not_found(e):
    return {'message': 'The requested URL was not found on the server'}, 404

@app.errorhandler(500)
def internal_server_error(e):
    return {'message': ' internal error and was unable to complete your request'}, 500

@app.errorhandler(405)
def method_not_allowed(e):
    return {'message': 'The method is not allowed for URL.'}, 405

