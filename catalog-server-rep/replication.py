############
import random

from flask_app import CATALOG_ADDRESSES, app
from requests import RequestException
from book import Book, replication_schema
from flask import request

import requests
############

##########1 second timeout for all connection
#######100 millisecond timeout for connection establishment
timeout = (0.1, 1)

############
class Replication:

    class CouldNotGetUpdatedError(RuntimeError):
        pass

    class OutdatedError(RuntimeError):
        pass

    class BookNotFoundError(RuntimeError):
        pass

    def __init__(self, catalog_addresses):
        self.catalog_addresses = catalog_addresses
        if type(self.catalog_addresses) is not list:
            self.catalog_addresses = []
        self.updated_ids = set([])

    def update(self, id, book_info) -> Book:
 ######If no other catalog servers are registered, no need for replication measures
        if len(self.catalog_addresses) == 0:
            return Book.update(id,
                               quantity=book_info.get('quantity'),
                               price=book_info.get('price'))

        book = Book.get(id)
        if book is None:
            raise self.BookNotFoundError()

        sequence_number = book.sequence_number
######If book is not recorded
        if id not in self.updated_ids:
     ####### Check servers for latest version
            max_sequence_number = sequence_number
            max_item = None

            for server in self.catalog_addresses:
    ##### spawn threads to handle multiple concurrent requests
                try:
       #####Request other servers to check the book sequence_number
                    data = {'sequence_number': sequence_number}
                    response = requests.get(f'{server}/rep/check/{id}',
                                            json=data, timeout=timeout)

     #######If object is out of date, update the object of maximum sequence number
                    if response.status_code == 409:
                        if max_sequence_number < response.json()['sequence_number']:
                            max_sequence_number = response.json()['sequence_number']
                            max_item = response.json()

                except RequestException:
                    pass



            self.updated_ids.add(id)

            if max_item is not None:

                Book.update(id, **max_item)

                raise self.OutdatedError()

        for server in self.catalog_addresses:

            try:

                data = {'sequence_number': sequence_number, **book_info}
                response = requests.put(f'{server}/rep/update/{id}',
                                        json=data, timeout=timeout)


                if response.status_code == 409:
                    raise self.OutdatedError()

            except RequestException:
                pass

        book = Book.update(id, **book_info)

        self.updated_ids.add(id)

        return book

    def get(self, id, max_sequence_number: int = None, requesters: list = None) -> Book:

        book = Book.get(id)

        if id in self.updated_ids:
            return book

        if book is None:
            raise self.BookNotFoundError

        sequence_number = book.sequence_number

        if requesters is None:
            requesters = []

        available_servers = self.catalog_addresses if requesters is None else \
            [server for server in self.catalog_addresses if server not in requesters]

        if len(available_servers) == 0:
            return Book.get(id)

        server = None
        while len(available_servers) > 0:
            try:
                server = random.choice(available_servers)
                response = requests.get(f'{server}/rep/get/{id}',
                                        json={
                                            'requesters': requesters if requesters is not None else [],
                                            'sequence_number':
                                                max_sequence_number
                                                if max_sequence_number is not None
                                                and max_sequence_number > sequence_number
                                                else sequence_number
                                        },
                                        timeout=timeout)
                break
            except RequestException:
                if server is not None:
                    available_servers.remove(server)

        else:
            self.updated_ids.add(id)
            return book

        if response.status_code == 409:


            if max_sequence_number is not None and max_sequence_number > sequence_number:
                raise self.OutdatedError

            else:
                self.updated_ids.add(id)
                return book

        if response.status_code != 200:
            raise self.CouldNotGetUpdatedError()


        Book.update(id, **response.json())

        self.updated_ids.add(id)

        return Book.get(id)

    def get_catalog_addresses_pure(self):
        return [address.replace('http://', "").replace('https://', "") for address in self.catalog_addresses]


replication = Replication(CATALOG_ADDRESSES)


@app.route('/rep/update/<book_id>', methods=['PUT'])
def replication_update(book_id):
    book_info = request.json

    book_id = int(book_id)

    book = Book.get(book_id)

    if book.sequence_number > book_info['sequence_number']:
        return replication_schema.jsonify(book), 409  # 409 Conflict

    Book.update(book_id, **book_info)

    response = replication_schema.jsonify(Book.get(book_id))

    Book.update(book_id, sequence_number=book_info['sequence_number']+1)

    return response

############
@app.route('/rep/get/<book_id>', methods=['GET'])
def replication_get(book_id):

####### list of servers that are requesting this item
    requesters = []
    if request.json is dict and 'requesters' in request.json:
        requesters = list(request.json['requesters'])

########## the max sequence number between all hops
    sequence_number = 0
    if request.json is dict and 'sequence_number' in request.json:
        sequence_number = request.json['sequence_number']
############
####### Add the remote address  to the list
    requesters.extend([address for address in replication.catalog_addresses if request.remote_addr in address])

    try:
######## Get the book from replication
        book = replication.get(int(book_id), max_sequence_number=sequence_number, requesters=requesters)

######### If book could not be retrieved (nobody has it)
    except Replication.CouldNotGetUpdatedError:
        return {'message': 'Not found'}, 404

########### If no newer book was found
    except Replication.OutdatedError:
        return {'message': 'No book with newer version was found'}, 409

    if book is None:
        return {'message': 'Not found'}, 404

    return replication_schema.jsonify(book)

############
@app.route('/rep/check/<book_id>', methods=['GET'])
def replication_check(book_id):
    book_info = request.json

    book_id = int(book_id)

    book = Book.get(book_id)

############If local book is newer than the check request
    if book.sequence_number > book_info['sequence_number']:
        return replication_schema.jsonify(book), 409  # 409 Conflict

    return {}
