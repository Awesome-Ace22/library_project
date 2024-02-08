import urllib.request
import urllib.parse
import json
from books import create
from bookdetails import create as create_book_details


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
        volume_info = data['items'][0]['volumeInfo']
        # Uses get method at each level to handle missing keys
        title = volume_info.get("title", "N/A")
        authors = ",".join(volume_info.get("authors", "N/A"))
        publisher = volume_info.get("publisher", "N/A")
        published_date = volume_info.get("publishedDate", "N/A")
        description = volume_info.get("description", "N/A")
        image_links = volume_info.get("imageLinks", {})
        thumbnail = image_links.get("thumbnail", "N/A")
        book_info = [isbn, title, authors, publisher, published_date, description, thumbnail]

        # Creates a dictionary with book information
        book_data = {
            "isbn": isbn,
            "title": title,
            "authors": authors,
            "publisher": publisher,
            "publishedDate": published_date,
            "description": description,
            "thumbnail": thumbnail
        }
        return book_data
    else:
        # Returns default values if 'items' is not present
        book_info = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A","N/A",]
        return book_info


