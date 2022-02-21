import os
import sqlite3

class BookClient:
    def __init__(self):
        self.book_db = sqlite3.connect(os.getcwd() + '\\databases\\books.db')

    def get_book_list(self, head=-1, tail=-1, unread="yes", sort="id"):
        result = "```ID | Title                        | Author                        | Published | Genre                        | Pages | Comment\n"
        cursor = self.book_db.execute("SELECT ID, TITLE, AUTHOR, PUBLISHED, GENRE, PAGES, COMMENT FROM BOOK")
        distances = [3, 29, 30, 10, 29, 6, 20]

        for row in cursor:
            for i, cell in enumerate(row):
                if row:
                    result += str(cell) + (" " * (distances[i] - len(str(cell)))) + "| "
                else:
                    result += "-" + (" " * (distances[i] - len("-"))) + "| "
            result += "\n"

        result += "```"
        return result

    def get_cite_list(self, tail=-1):
        pass

    def add_book_to_db(self, title, author=None, link=None, year=None):
        pass

    def add_cite_to_db(self, cite, book_title=None):
        pass

    def remove_book_from_db(self, index):
        pass

    def remove_cite_from_db(self, index):
        pass

    #Net so wichtig!
    def get_unread_books(self, username):
        pass

    def mark_as_read(self, username, book):
        pass
