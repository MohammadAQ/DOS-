from flask_app import app
from os import environ
CATALOG_ADDRESSES = ('http://10.0.2.7:5000|http://10.0.2.8:5000').split('|')
ORDER_ADDRESSES = ('http://10.0.2.11:5000|http://10.0.2.15:5000').split('|')


print(CATALOG_ADDRESSES)
#############################################################
# Manages replication
class Replication:
    def __init__(self, catalog_addresses, order_addresses):
        self.catalog_addresses = catalog_addresses
        self.order_addresses = order_addresses
        self.catalog_address_turn = 0
        self.order_address_turn = 0
       
    def get_catalog_address(self):
        # Get address of the current catalog server
        address = self.catalog_addresses[self.catalog_address_turn]

        # Round Robin policy
        self.catalog_address_turn += 1
        if self.catalog_address_turn >= len(self.catalog_addresses):
            self.catalog_address_turn = 0
		
        return address

    def get_order_address(self):
        # Get address of the current order server
        address = self.order_addresses[self.order_address_turn]

        # Round Robin policy
        self.order_address_turn += 1
        if self.order_address_turn >= len(self.order_addresses):
            self.order_address_turn = 0

        return address

    def get_catalog_count(self):
        return len(self.catalog_addresses)

    def get_order_count(self):
        return len(self.order_addresses)


replication = Replication(CATALOG_ADDRESSES, ORDER_ADDRESSES)
#############################################################
# 2 second timeout for all connection
# 200 millisecond timeout for connection establishment
# (assuming that the maximum time for an operation was calculated)
timeout = (0.2, 2.0)
