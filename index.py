import bottle
import pymongo
import guestbookDAO


class Index:
    def __init__(self):
        self.connection_string = 'mongodb://localhost'
        self.guestbook = None

    def _set_guestbook(self, guestbook):
        self.guestbook = guestbook

    # This is the default route, our index page. Here we need to read the documents from MongoDB
    @bottle.route('/')
    def guestbook_index(self):
        persons = self.guestbook.find_persons()

        return bottle.template('index', dict(persons=persons))

    # We will post new entries to this route so we can insert them into MongoDB
    @bottle.route('/newguest', method='POST')
    def insert_newguest(self):
        name = bottle.request.forms.get('name')
        email = bottle.request.forms.get('email')

        self.guestbook.insert_person(name, email)

        bottle.redirect('/')

    def run(self):
        connection = pymongo.MongoClient(self.connection_string)
        database = connection.persons

        guestbook = guestbookDAO.GuestbookDAO(database)
        self._set_guestbook(guestbook)

        bottle.debug(True)
        bottle.run(host='192.168.33.10', port=8082)


if __name__ == '__main__':
    index = Index()
    index.run()
