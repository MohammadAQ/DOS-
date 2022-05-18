import requests

ORDER_ADDRESS = ('http://10.0.2.11:5000 | http://10.0.2.15:5000').split(' | ')
FRONT_END_ADDRESS = ('http://10.0.2.10:5000')
CATALOG_ADDRESSES = ('http://10.0.2.7:5000 | http://10.0.2.8:5000').split(' | ')

################
#####Send request to  front  server to invalidate a book
def invalidate_item(book_id):
    requests.delete(f'{FRONT_END_ADDRESS}/invalidate/item/{book_id}')

###################
#####Send request to front  server to invalidate a topic

def invalidate_topic(book_topic):
    requests.delete(f'{FRONT_END_ADDRESS}/invalidate/topic/{book_topic}')
    #################
