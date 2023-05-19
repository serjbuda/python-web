import json
from models import Author, Quote

with open('authors.json', 'r') as file:
    authors_data = json.load(file)

for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

with open('quotes.json', 'r') as file:
    quotes_data = json.load(file)

for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data['author']).first()
    quote = Quote(
        tags=quote_data['tags'],
        author=author,
        quote=quote_data['quote']
    )
    quote.save()
