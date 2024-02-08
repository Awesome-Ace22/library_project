
import urllib.request
import urllib.parse
import json
from flask import jsonify


def isbn_look_up(isbn):
    def build_api_url(base, isbn, key):
        return f"{base}q=isbn:{isbn}&key={key}"

    base_url = 'https://www.googleapis.com/books/v1/volumes?'
    api_key = "AIzaSyCPzScaBHj4osIL8kEn9sZtSy1vDVsUVvg"

    url = build_api_url(base_url, isbn, api_key)
    response = urllib.request.urlopen(url)

    data = json.loads(response.read())
    # Checks if 'items' is present in the response
    if 'items' in data:
        id = data['items'][0]["id"]
        volume_info = data['items'][0]['volumeInfo']
        # Uses get method at each level to handle missing keys
        title = volume_info.get("title", "N/A")
        authors = ",".join(volume_info.get("authors", "N/A"))
        publisher = volume_info.get("publisher", "N/A")
        published_date = volume_info.get("publishedDate", "N/A")
        description = volume_info.get("description", "N/A")
        pageCount = volume_info.get("pageCount", "N/A")
        image_links = volume_info.get("imageLinks", {})
        thumbnail = image_links.get("thumbnail", "N/A")

        book_info = [isbn, title, authors, publisher, published_date, description, thumbnail]

        # Creates a dictionary with book information
        book_data = {
            "id": id,
            "isbn": isbn,
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "publishedDate": published_date,
            "description": description,
            "pageCount": pageCount,
            "thumbnail": thumbnail
        }
        return book_data
    else:
        # Returns default values if 'items' is not present
        book_info = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A",]
        return book_info


BOOKS_NOTES = []

test_data = [9780063237483, 9780872204843, 9781796356304, 9781529091427, 9781627791229]
for isbn in test_data:
    results = isbn_look_up(isbn)
    BOOKS_NOTES.append(results)

for bk in BOOKS_NOTES:
    for key in bk:
        format_string = '"' + key + '"' + ": {" + key + "}"
        print(format_string.format(**bk))

# print(BOOKS_NOTES)