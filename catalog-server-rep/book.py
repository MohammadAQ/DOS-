#import database
from database import db, marshmallow, database_init
###########

######### Define the Book class that overrides SQLAlchemy's Model class
class Book(db.Model):
    ##############define database atttributes which will be mapped todatabase columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False,)
    topic = db.Column(db.String(200), nullable=False,)
    quantity = db.Column(db.Integer, nullable=False, default=0,)
    price = db.Column(db.Float, nullable=False)
#########
  ##### Replication field to creat  consistency
    sequence_number = db.Column(db.Integer, nullable=False, default=0,)
############################################################################
   #######creeate data base Constructor
    def __init__(self, title, topic, quantity, price):
        self.title = title
        self.quantity = quantity
        self.topic = topic
        self.price = price
        self.sequence_number = 0
##############
  ########## search for books based on book topic
    @classmethod
    def search(cls, topic):
  ############# Returns the book that contain the query string
        return Book.query.filter(Book.topic.ilike(f'%{topic}%'))
#################
   ######### get a book using  ID
    @classmethod
    def get(cls, id):
        return Book.query.get(id)
###############
 ########update the fields of a book given  ID
    @classmethod
    def update(cls, id, title=None, quantity=None, topic=None, price=None, sequence_number=None):
        book = Book.query.get(id)
        if book is None:
            return None
        book.title = title if title is not None else book.title
        book.quantity = quantity if quantity is not None and quantity >= 0 else book.quantity
        book.topic = topic if topic is not None else book.topic
        book.price = price if price is not None and price >= 0.0 else book.price
##########
     #####Update sequence number
        if sequence_number is None:
            if title is not None or quantity is not None or topic is not None or price is not None:
                book.sequence_number = book.sequence_number + 1
        else:
            book.sequence_number = sequence_number

        db.session.commit()
        return book
#############
######### view all rows
    @classmethod
    def dump(cls):
        return Book.query.all()

################
# Add the 7 books as an initial entry to the database
database_init += [
    Book('How to get a good grade in DOS in 40 minutes a day', 'Distributed Systems', 12, 10.00),
    Book('RPCs for Noobs', 'Distributed Systems', 5, 50.00),
    Book('Xen and the Art of Surviving Undergraduate School', 'Graduate School', 13, 10.00),
    Book('Cooking for the Impatient Undergrad', 'Graduate School', 55, 10.00),
    Book('How to finish Project 3 on time', 'new arrival', 40, 10.00),
    Book('Why theory classes are so hard', 'new arrival', 38, 10.00),
    Book('Spring in the Pioneer Valley', 'new arrival', 15, 10.00),
]

###############
###### Marshmallow  Schema for query-by-topic
class TopicSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'title', 'topic')

###################
######### Marshmallow  Schema  for query-by-item
class ItemSchema(marshmallow.Schema):
    class Meta:
        fields = ('title', 'quantity', 'price')

########
####### Marshmallow  Schema  for update
class UpdateSchema(marshmallow.Schema):
    class Meta:
        fields = ('title', 'quantity', 'topic', 'price')

#################
####### Marshmallow  Schema class for replication consistency
class ReplicationSchema(marshmallow.Schema):
    class Meta:
        fields = ('sequence_number', 'title', 'quantity', 'topic', 'price')
#################
######## create an object from each schema
item_schema = ItemSchema()
topic_schema = TopicSchema(many=True)
update_schema = UpdateSchema()
replication_schema = ReplicationSchema()

################
# Dump
class DumpSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'sequence_number', 'title', 'quantity', 'topic', 'price')


dump_schema = DumpSchema(many=True)

##############
