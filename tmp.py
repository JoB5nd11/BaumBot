import sqlite3
import pandas as pd

book_db = sqlite3.connect('databases/books.db')
#
# book_db.execute('''CREATE TABLE BOOK
#             (ID INT PRIMARY KEY,
#              TITLE          TEXT,
#              AUTHOR         TEXT,
#              PUBLISHED      INT,
#              GENRE          TEXT,
#              PAGES          INT,
#              COMMENT        TEXT);''')
#
# book_db.execute('''CREATE TABLE CITE
#             (ID INT PRIMARY KEY,
#              CITE              TEXT,
#              BOOK_ID           INT,
#              FOREIGN KEY(BOOK_ID) REFERENCES BOOK(ID));''')
#
# book_db.execute("INSERT INTO BOOK (ID, TITLE, AUTHOR, PUBLISHED, GENRE, PAGES, COMMENT) \
#                  VALUES (2, 'The Nature of Code', 'Daniel Shiffman', 2012 ,'Computers & Programming', 480, NULL)");
#
# book_db.commit()

df = pd.read_sql_query("SELECT * FROM BOOK", book_db)
print(df.to_string())
