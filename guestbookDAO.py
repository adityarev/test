import string


class GuestbookDAO:
    def __init__(self, database):
        self.database = database
        self.persons = database.persons

    # Handle the finding of persons
    def find_persons(self):
        result = []
        persons = self.persons.find()

        for person in persons:
            result.append({'name': person['name'], 'email': person['email']})

        return result

    # Handle the insertion of person
    def insert_person(self, name, email):
        new_person = {'name': name, 'email': email}
        self.persons.insert(new_person)
