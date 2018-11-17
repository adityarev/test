import bottle
import pymongo
import guestbookDAO

@bottle.route('/')
def guestbook_index():

