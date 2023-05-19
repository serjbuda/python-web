from mongoengine import Document, fields

class Author(Document):
    fullname = fields.StringField(required=True)
    born_date = fields.StringField()
    born_location = fields.StringField()
    description = fields.StringField()

class Quote(Document):
    tags = fields.ListField(fields.StringField())
    author = fields.ReferenceField(Author)
    quote = fields.StringField()

class Contact(Document):
    fullname = fields.StringField(required=True)
    email = fields.EmailField(required=True)
    is_sent = fields.BooleanField(default=False)
