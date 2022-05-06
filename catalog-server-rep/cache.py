from flask_app import FRONT_END_ADDRESS
import requests

################
#####Send request to  front  server to invalidate a book
def invalidate_item(book_id):
    requests.delete(f'{FRONT_END_ADDRESS}/invalidate/item/{book_id}')

###################
#####Send request to front  server to invalidate a topic

def invalidate_topic(book_topic):
    requests.delete(f'{FRONT_END_ADDRESS}/invalidate/topic/{book_topic}')
    #################
