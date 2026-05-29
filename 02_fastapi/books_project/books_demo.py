from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'category': 'science'},
    {'title': 'Cosmos', 'author': 'Carl Sagan', 'category': 'science'},
    {'title': 'Guns, Germs, and Steel', 'author': 'Jared Diamond', 'category': 'history'},
    {'title': 'Sapiens: A Brief History of Humankind', 'author': 'Yuval Noah Harari', 'category': 'history'},
    {'title': 'Gödel, Escher, Bach: An Eternal Golden Braid', 'author': 'Douglas Hofstadter', 'category': 'math'},
    {'title': 'Principia Mathematica', 'author': 'Isaac Newton', 'category': 'math'},
    {'title': 'The Universe in a Nutshell', 'author': 'Stephen Hawking', 'category': 'philosophy'},
    {'title': 'Pale Blue Dot', 'author': 'Carl Sagan', 'category': 'astronomy'},
    {'title': 'Collapse: How Societies Choose to Fail or Succeed', 'author': 'Jared Diamond', 'category': 'environment'},
    {'title': 'Homo Deus: A Brief History of Tomorrow', 'author': 'Yuval Noah Harari', 'category': 'future studies'},
    {'title': 'I Am a Strange Loop', 'author': 'Douglas Hofstadter', 'category': 'cognitive science'},
    {'title': 'Opticks', 'author': 'Isaac Newton', 'category': 'physics'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/title/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/category")
async def read_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



@app.get("/books/author")
async def fetch_books_by_authorname(author_name: str):
    books_info = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_info.append(book)
    return books_info



@app.get("/books/author/filter")
async def read_author_category_by_query(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return BOOKS


@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break