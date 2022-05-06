#########///////////////////
from flask import request
from flask_app import app
from book import Book, topic_schema, item_schema, update_schema, dump_schema
from replication import replication, Replication
import cache
#########///////////////////
######Query-by-item
def query_by_item(book_id):
####Use the replication get method
    try:
        return replication.get(book_id)
    except (Replication.CouldNotGetUpdatedError, Replication.BookNotFoundError):
        return None

#########///////////////////
####Query by topic
#####The data returned by topic queries cannot be updated
###### doesn't need to be checked for different values at replicas
def query_by_topic(book_topic):
    return Book.search(book_topic)

#########///////////////////
####For each method
###1.  query handler which references the handler function
### 2. Aschema object which formats the response message
queries = {
    'item': {
        'query_handler': query_by_item,
        'schema': item_schema
    },
    'topic': {
        'query_handler': query_by_topic,
        'schema': topic_schema
    }
}

#########///////////////////

@app.route('/query/<method>/<param>', methods=['GET'])
def query(method, param):
    # If the query method specified in the URI does not exist, return an error message
    if method not in queries:
        return {'message': 'Invalid query method', 'supportedQueryMethods': list(queries.keys())}, 404

    # Call the query handler and pass it the parameter from the URI
    result = queries[method]['query_handler'](param)

    # If the result is None, the query was not successful, return an error message
    if result is None:
        return {'message': 'Not found'}, 404

    # Otherwise, return the query result, formatted using the schema object
    return queries[method]['schema'].jsonify(result)

#########///////////////////
@app.route('/update/<book_id>', methods=['PUT'])
def update(book_id):
    # Extract the JSON data from the request
    book_data = request.json

    # If no data was passed  treat it like an empty JSON object
    if book_data is None:
        book_data = {}

    book = Book.get(book_id)

    # If  book is None return an error message
    if book is None:
        return {'message': 'Not found'}, 404


#######Use the replication method to update the book and make sure all other replicas get the updated book
    try:
        book = replication.update(book_id, book_data)

########If the update failed, return a fail response
    except Replication.OutdatedError:
        return {'message': 'Update could not be processed because the item is not up to date'}, 409

######Invalidate cache
    cache.invalidate_item(book_id)
    cache.invalidate_topic(book.topic)


    return update_schema.jsonify(book)

#########///////////////////# Dump endpoint
@app.route('/dump/', methods=['GET'])
def dump():
    return dump_schema.jsonify(Book.dump())
