from flask_app import app
import requests
#############################################

CATALOG_ADDRESS = ('http://10.0.2.7:5000')
FRONT_END_ADDRESS = ('http://10.0.2.10:5000')
print(CATALOG_ADDRESS)



# 1.5 S timeout for all connection
# 150 millisecond timeout for connection establishment
# (assuming that the maximum time for an operation was calculated)
timeout = (0.15, 1.5)

#############################################

# Buy endpoint
@app.route('/buy/<book_id>', methods=['PUT'])
def buy(book_id):
    # If the ID is not a number then error
    if not book_id.isnumeric():
        return {'message': 'Book ID must be a number'}, 422

    while True:
        # or the ID is a number then
        try:
            book_response = requests.get(f'{CATALOG_ADDRESS}/query/item/{book_id}', timeout=timeout)
        except requests.RequestException:
            return {'message': 'Could not connect to the catalog server'}, 504
#############################################
        # If the response status is 404 not found, override the error message
        if book_response.status_code == 404:
            return {'message': 'Book with the specified ID does not exist'}, 404
#############################################
        # If any other non-OK response is received, return it as-is
        elif book_response.status_code != 200:
            return book_response.content, book_response.status_code, book_response.headers.items()
#############################################
        # Extract the book information from the response
        book = book_response.json()
#############################################
        # If the quantity is 0, return this message
        if book['quantity'] <= 0:
            return {'success': False, 'message': 'Book with the specified ID is out of stock'}

        # Otherwise, update book quantity on catalog using update message
        try:
            buy_response = requests.put(f'{CATALOG_ADDRESS}/update/{book_id}', json={'quantity': book['quantity'] - 1},
                                        timeout=timeout)
        except requests.RequestException:
            return {'message': 'Could not connect to the catalog server'}, 504
#############################################
        # if the buy request have any errors occure
        if buy_response.status_code == 409:
            continue
#############################################
        # errors while make updating
        elif buy_response.status_code != 200:
            return buy_response.text, buy_response.status_code, buy_response.headers.items()

        else:
            break

    # is message success return : 
    return {'success': True, 'message': 'Book with the specified ID purchased'}

