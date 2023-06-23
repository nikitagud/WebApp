import requests
from app import app, db, Book

url = "https://hapi-books.p.rapidapi.com/nominees/romance/2020"

headers = {
    "X-RapidAPI-Key": "d8715946e8msh42fa28aafc7694bp148111jsn76d51b494ed6",
    "X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

data = response.json()

with app.app_context():
    for book in data:
        name = book['name']
        author = book['author']
        book_id = book['book_id']

        # Create a Book object and add it to the database
        book_obj = Book(name=name, author=author, book_id=book_id)
        db.session.add(book_obj)

    # Commit the changes to the database
    db.session.commit()

    print("Data inserted successfully.")

