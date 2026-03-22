from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

app = FastAPI()
borrow_records = []
record_counter = 1
queue=[]

#pydantic model for borrow request-6
class BorrowRequest(BaseModel):
    member_name: str=Field(..., min_length=2)
    book_id: int=Field(..., gt=0)
    borrow_days: int=Field(..., gt=0, le=60)  
    member_id: str=Field(..., min_length=4)
    member_type: str="regular"  # New field for member type with validation

#pydantic model for newbook
class NewBook(BaseModel):
    title: str=Field(..., min_length=2)
    author: str=Field(..., min_length=2)
    genre: str=Field(..., min_length=2)
    is_available: bool=True


#Helper function-7 : to find a book by ID
def find_book(book_id):
    for book in books_list:
        if book["id"] == book_id:
            return book
    return None

def calculate_due_date(borrow_days, member_type):
    if member_type == "premium":
        max_days = 60
    else:
        max_days=30
    allowed_days = min(borrow_days, max_days)
    due_date = datetime.now() + timedelta(days=allowed_days)

    if borrow_days > max_days:
        message = f"{member_type.capitalize()} members can borrow for maximum of {max_days} days. Due date adjusted."
    else:
        message = f"Book borrowed for {allowed_days} days."

    return {
        "due_date": due_date.strftime("%Y-%m-%d"),
        "message": message
    }

#helper function to filter books by genre
def filter_books_logic(genre=None, author=None, is_available=None):
    filtered = books_list

    if genre is not None:
        filtered = [
            book for book in filtered
            if genre.lower().replace(" ", "-") in book["genre"].lower()
        ]

    if author is not None:
        filtered = [
            book for book in filtered
            if author.lower() in book["author"].lower()
        ]

    if is_available is not None:
        filtered = [
            book for book in filtered
            if book["is_available"] == is_available
        ]

    return filtered

books_list= [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "is_available": True},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "is_available": True},
    {"id": 3, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "is_available": False},
    {"id": 4, "title": "Mockingbird", "author": "Harper Lee", "genre": "Fiction", "is_available": True},
    {"id": 5, "title": "The Satvic Revolution", "author": "Harshvardhan Saraf and Subah Saraf", "genre": "Self-Help", "is_available": False},
    {"id": 6, "title": "The 48 Laws of POWER", "author": "Robert Greene", "genre": "Self-Help", "is_available": True}
]

#End point-1 for the home page
@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}

#End point-2 to get the list of all books
@app.get("/books")
def get_books():
   return {"books": books_list, "total": len(books_list), "available": sum(book["is_available"] for book in books_list)}

#End point-5 summary
@app.get("/summary")
def summary():
    total_books = len(books_list)
    available_books = sum(book["is_available"] for book in books_list)
    borrowed_books = total_books - available_books
    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "borrow_records": borrow_records,
        "books_per_genre": {genre: sum(book["genre"] == genre for book in books_list) for genre in set(book["genre"] for book in books_list)}
    }

#endpoint-16 to search books by title or author
@app.get("/books/search")
def search_books(keyword: str):
    results = [
        b for b in books_list
        if keyword.lower() in b["title"].lower()
        or keyword.lower() in b["author"].lower()
    ]

    return {
        "results": results,
        "total_found": len(results)
    }

#endpoint-17 to return sorted books with sort metadata
@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):
    if sort_by not in {"title", "author", "genre"}:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid sort order")

    sorted_books = sorted(books_list, key=lambda x: x[sort_by], reverse=(order == "desc"))

    return {
        "sorted_by": sort_by,
        "order": order,
        "books": sorted_books
    }

#endpoint-18 pagination
@app.get("/books/page")
def get_books_page(page: int = 1, limit: int = 3):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid page or limit")

    total = len(books_list)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit
    page_books = books_list[start:end]

    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "books": page_books
    }

#endpoint-19 to search borrow records by member name
@app.get("/borrow-records/search")
def search_borrow_records(member_name: str):
    k = member_name.lower()
    results = [r for r in borrow_records if k in r["member_name"].lower()]
    return {"results": results, "total_found": len(results)}

#endpoint- to paginate borrow records
@app.get("/borrow-records/page")
def paginate_borrow_records(page: int, limit: int):
    start = (page - 1) * limit
    end = start + limit
    data = borrow_records[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": len(borrow_records),
        "records": data
    }

#endpoint-20 to combine search, sort, and pagination for books
@app.get("/books/browse")
def browse_books(
    keyword: str = None,
    sort_by: str = "title",
    order: str = "asc",
    page: int = 1,
    limit: int = 10
):
    data = books_list

    if keyword:
        k = keyword.lower()
        data = [b for b in data if k in b["title"].lower() or k in b["author"].lower()]

    if sort_by not in ["title", "author", "genre"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = True if order == "desc" else False
    data = sorted(data, key=lambda b: b[sort_by].lower(), reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    paginated = data[start:end]

    return {
        "keyword": keyword,
        "sorted_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": len(data),
        "results": paginated
    }

#endpoint-10 to filter books by genre, author, and availability
@app.get("/books/filter")
def filter_books(
    genre: Optional[str] = None,
    author: Optional[str] = None,
    is_available: Optional[bool] = None
):
    filtered_books = filter_books_logic(genre, author, is_available)

    return {
        "count": len(filtered_books),
        "books": filtered_books
    }


#End point -3 to get details of a specific book by its ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_list:
        if book["id"] == book_id:
            return {"book": book}
    return {"error": "Book not found"}

#End point-4 to borrow record
@app.get("/borrow-records")
def get_borrow_records():
    return {
        "total": len(borrow_records),
        "records": borrow_records
    }

#End point-8 to borrow a book with detailed information
@app.post("/borrow")
def borrow_book_with_details(request: BorrowRequest):
    global record_counter   

    book = find_book(request.book_id)
    if not book:
        return {"error": "Book not found"}

    if not book["is_available"]:
        return {"message": f"Sorry, '{book['title']}' is currently not available"}
    
    due_info = calculate_due_date(request.borrow_days, request.member_type)

    book["is_available"] = False

    borrow_record = {
        "record_id": record_counter,
        "member_name": request.member_name,
        "member_id": request.member_id,
        "member_type": request.member_type,
        "book_id": request.book_id,
        "title": book["title"],
        "borrow_days": request.borrow_days,
        "due_date": due_info["due_date"]
    }

    borrow_records.append(borrow_record)

    record_counter += 1

    return {
        "message": due_info["message"],
        "record": borrow_record
    }


#endpoint-11 to add a new book to the library
@app.post("/books")
def add_book(new_book: NewBook):
    new_id = max(book["id"] for book in books_list) + 1 if books_list else 1
    book_entry = {
        "id": new_id,
        "title": new_book.title,
        "author": new_book.author,
        "genre": new_book.genre,
        "is_available": new_book.is_available
    }
    books_list.append(book_entry)
    return {"message": f"Book '{new_book.title}' added successfully", "book": book_entry}

#endpoint-12 to return updated book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: NewBook):
    for book in books_list:
        if book["id"] == book_id:
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            book["genre"] = updated_book.genre
            book["is_available"] = updated_book.is_available
            return {"message": f"Book ID {book_id} updated successfully", "book": book}
    return {"error": "Book not found"}

#endpoint-13 to delete a book by its ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_list):
        if book["id"] == book_id:
            deleted_book = books_list.pop(index)
            return {"message": f"Book ID {book_id} deleted successfully", "book": deleted_book}
    return {"error": "Book not found"}

#endpoint-14 to return waitlist for a book
@app.post("/queue/add")
def add_to_queue(member_name: str, book_id: int):
    book = next((b for b in books_list if b["id"] == book_id), None)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book["is_available"]:
        raise HTTPException(status_code=400, detail="Book is available, no need to queue")

    queue.append({
        "member_name": member_name,
        "book_id": book_id
    })

    return {"message": "Added to queue", "queue": queue}

#endpoint- to view the queue for a book
@app.get("/queue")
def get_queue():
    return {"queue": queue}

#endpoint-15 return book id
@app.post("/return/{book_id}")
def return_book(book_id: int):
    book = next((b for b in books_list if b["id"] == book_id), None)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book["is_available"] = True

    for i in range(len(queue)):
        if queue[i]["book_id"] == book_id:
            user = queue.pop(i)
            borrow_records.append({
                "member_name": user["member_name"],
                "book_id": book_id
            })
            book["is_available"] = False
            return {
                "message": "returned and re-assigned",
                "assigned_to": user["member_name"]
            }

    return {"message": "returned and available"}