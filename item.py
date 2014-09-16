class Item(object):

    def __init__(self):
        self.data = {}
        self.table = "Items"

    def insert(self):
        question_marks = "?, " * (len(fields)-1) + "?"

        values = ()
        fields = ()
        for key, value in sorted(self.data.iteritems()):
            values += (value,)
            fields += (key,)

        statement = "Insert into {0}{1} Values ({2})".format(self.table, fields, question_marks)
        effect_db(db, statement, args=values)

class Book(Item):

    def __init__(self):
        self.fields = ("Category", "ISBN", "Title", "Author", "Image")
        self.table = "Books"