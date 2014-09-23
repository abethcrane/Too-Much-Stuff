from db_functions import *

class Item(object):

    def __init__(self, db, identifier=None):
        self.db = db
        self.id = identifier
        self.data = {}
        self.table = "Items"

    @classmethod
    def generic_item(self, db, identifier, category, id_type):
        item = Item(db, identifier)
        item.id_type = id_type
        item.data = {"Category": category, item.id_type: item.id}
        #item.table = "{0}s".format(category)
	return item

    def insert(self):
        question_marks = "?, " * (len(fields)-1) + "?"

        values = ()
        fields = ()
        for key, value in sorted(self.data.iteritems()):
            values += (value,)
            fields += (key,)

        statement = "Insert into {0}{1} Values ({2})".format(self.table, fields, question_marks)
        effect_db(self.db, statement, args=values)

    def get_db_id(self):
        id = query_db(self.db, "Select Item_ID from {0} where {1}=?".format(self.table, self.id_type), (self.id,), one=True)
        if id is None:
            return id
        else:
            return id["Item_ID"]

class Book(Item):

    def __init__(self, identifier):
        super(Book, self).__init(identifier)
        self.id_type="ISBN"
        self.data["Category"] = "Book"
        self.data["ISBN"] = self.id
        self.data["Title"], self.data["Author"], self.data["Image"] = get_book_data(self.id)
        # TODO: possibly consider self.fields and we can set that to list all the things we want to look up
        # TODO: For now we don't want to use different tables, because we haven't set that up in the database.
        #self.table = "Books"

    def get_book_data(self, ISBN):
        data = self.lookup_ISBN(ISBN)
        title = self. get_title(data)
        author = self.get_author(data)
        image = self.get_image(data)

        return title, author, image

    def lookup_ISBN(self, ISBN):
        try:
            ISBN10 = self.get_ISBN10(ISBN)
            url = "https://www.googleapis.com/books/v1/volumes?q=isbn:{0}".format(ISBN10)
            data = json.load(urllib2.urlopen(url))["items"][0]["volumeInfo"]
        except TypeError as e:
            data = None
        finally:
            return data

    def check_digit(self, ISBN):
        total = 0
        if len(ISBN) is not 9:
            return ''
        for i in range (0, 9):
            total += (10-i) * int(ISBN[i])
        return str(11 - (total % 11))

    def get_ISBN10(self, ISBN):
        length = len(ISBN)
        if length is 9:
            return ISBN + self.check_digit(ISBN)
        elif length is 10:
            return ISBN
        elif length is 12 or length is 13:
            ISBN10 = ISBN[3:12]
            return ISBN10 + self.check_digit(ISBN10)
        else:
            raise TypeError

    def get_title(self, data):
        try:
            title = data["items"][0]["volumeInfo"]["title"]
        except Exception as e:
            title = "Unkown Title"
        finally:
            return title

    def get_author(self, data):
        try:
            author = data["items"][0]["volumeInfo"]["author"]
        except Exception as e:
            try:
                authors = data["items"][0]["volumeInfo"]["authors"]
                author = ""
                for i in authors:
                    author = author + i + ", "
                author = author[:-2]
            except Exception as e:
                author = "Unknown Author"
        finally:
            return author

    def get_image(self, data):
        try:
            image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        except Exception as e :
            image = "http://placehold.it/140x140"
        finally:
            return image
