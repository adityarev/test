import bottle
import pymongo
import guestbookDAO


class Index(object):
    def __init__(self):
        self.connection_string = 'mongodb://localhost'
        self.guestbook = None

    def _set_guestbook(self, guestbook):
        self.guestbook = guestbook

    # Read entries from MongoDB
    def guestbook_index(self):
        persons = self.guestbook.find_persons()

        return bottle.template('index', dict(persons=persons))

    # Create new entry and insert it into MongoDB
    def insert_newguest(self):
        name = bottle.request.forms.get('name')
        email = bottle.request.forms.get('email')

        self.guestbook.insert_person(name, email)

        bottle.redirect('/')

    # Delete an entry from MongoDB
    def delete_guest(self):
        person_id = bottle.request.forms.get('_id')

        self.guestbook.delete_person(person_id)

        bottle.redirect('/')

    def run(self):
        connection = pymongo.MongoClient(self.connection_string)
        database = connection.persons

        guestbook = guestbookDAO.GuestbookDAO(database)
        self._set_guestbook(guestbook)

        # Set Route
        bottle.route('/', callback=self.guestbook_index)
        bottle.route('/newguest', method='POST', callback=self.insert_newguest)
        bottle.route('/delete', method='POST', callback=self.delete_guest)

        bottle.debug(True)
        bottle.run(host='192.168.33.10', port=8082)


if __name__ == '__main__':
    index = Index()
    index.run()
