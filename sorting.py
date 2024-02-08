from models import Book, books_schema, book_schema
#9780872204843
def sort_info(dict):
    desired_order = ['id', 'isbn', 'title', 'authors',("id", "book_id", "publisher", "publishedDate", "description", "thumbnail"), 'timestamp']
    def custom_order(key):
        for i, order in enumerate(desired_order):
            if isinstance(order, list) and key in order:
                return i
            elif key == order:
                return i
        return len(desired_order)

    sorted_dict = dict[sorted(dict.items(), key=lambda item: custom_order(item[0]))]
    return sorted_dict

