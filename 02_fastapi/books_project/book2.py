from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int 

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description 
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None) 
    title: str = Field(min_length=3)
    author: str = Field(min_length=1) 
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2027)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithshizi",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }
    }

BOOKS = [
    Book(1, 'Cosmos', 'Carl Sagan', 'Exploration of the universe and humanity place in it', 5, 2020),
    Book(2, 'A Brief History of Time', 'Stephen Hawking', 'Insights into cosmology and black holes', 5, 2023),
    Book(3, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'History of human evolution and societies', 4, 2016),
    Book(4, 'Gödel, Escher, Bach', 'Douglas Hofstadter', 'Connections between math, art, and music', 5, 2012),
    Book(5, 'Principia Mathematica', 'Isaac Newton', 'Foundational work in mathematics and physics', 5, 2020),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def fetch_books_by_published_date(year: int = Query(gt=1999, lt=2027)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == year:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")



@app.get("/book/book_rating", status_code=status.HTTP_200_OK)
async def fetch_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_total = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_total.append(book)
    return books_total


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if book_id == BOOKS[i].id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")