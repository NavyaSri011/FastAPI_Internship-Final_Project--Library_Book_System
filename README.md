Library Book System - FastAPI Backend Project

Project Overview
This is a fully functional FastAPI backend project built as part of a 6-day FastAPI internship training program.
The project implements a Library Book System that enables users to manage books, handle borrow requests, and track member activity.
It covers core backend concepts including GET and POST APIs, Pydantic validation, CRUD operations, and multi-step workflows. 
The system also supports a queue mechanism that automatically assigns returned books to waiting members. 
Advanced features like keyword search, sorting, and pagination are also included.

Tech Stack
Python 3.10 or above
FastAPI
Uvicorn
Pydantic


Project Structure
main.py
requirements.txt
README.md
screenshots/


How to Run the Project
Step 1 - Clone the repository
git clone (https://github.com/NavyaSri011/FastAPI_Internship-Final_Project--Library_Book_System)

Step 2 - Install dependencies
pip install -r requirements.txt

Step 3 - Start the server
uvicorn main:app --reload

Step 4 - Open Swagger UI
Visit http://127.0.0.1:8000/docs to test all endpoints.


Requirements File Contents
fastapi
uvicorn
pydantic


API Endpoints
Day 1 - GET APIs
GET / - Welcome message for the library
GET /books - Returns all books with total count and available count
GET /books/summary - Returns total books, available count, borrowed count, and genre breakdown
GET /books/{book_id} - Returns a single book by ID or an error if not found
GET /borrow-records - Returns all borrow records with total count

Day 2 and Day 3 - POST with Pydantic Validation and Helper Functions
POST /borrow - Borrow a book using BorrowRequest model with member_name, book_id, borrow_days, member_id, and member_type
GET /books/filter - Filter books by genre, author, and availability using optional query parameters

Day 4 - CRUD Operations
POST /books - Add a new book (rejects duplicate titles, returns 201 Created)
PUT /books/{book_id} - Update genre or availability of an existing book
DELETE /books/{book_id} - Delete a book by ID and return confirmation message

Day 5 - Multi-Step Workflow
POST /queue/add - Add a member to the waitlist for an unavailable book
GET /queue - View the current borrow queue
POST /return/{book_id} - Return a book and auto-assign it to the next person in the queue if one exists

Day 6 - Advanced APIs
GET /books/search - Search books by keyword across title and author fields
GET /books/sort - Sort books by title, author, or genre in ascending or descending order
GET /books/page - Paginate the book list with page and limit parameters
GET /borrow-records/search - Search borrow records by member name
GET /borrow-records/page - Paginate borrow records
GET /books/browse - Combined endpoint with keyword search, sorting, and pagination together


Key Concepts Implemented
GET APIs with route ordering rules
POST endpoints with Pydantic model validation and field constraints
Helper functions: find_book, calculate_due_date, filter_books_logic
CRUD operations with proper status codes 201 and 404
Multi-step borrow and return workflow with queue management
Keyword search, result sorting, and pagination
Combined browse endpoint integrating all Day 6 features

Route Order Rules Followed
Fixed routes like /books/summary, /books/search, /books/filter, /books/sort, /books/page, and /books/browse are all placed above the variable route /books/{book_id} to avoid routing conflicts.


Screenshots
All 20 questions have been tested in Swagger UI at http://127.0.0.1:8000/docs and screenshots are saved in the screenshots folder.

Q1_home_route.png
Q2_get_all_books.png
Q3_get_book_by_id.png
Q4_get_borrow_records.png
Q5_books_summary.png
Q6_borrow_request_validation.png
Q7_helper_functions.png
Q8_post_borrow.png
Q9_member_type_premium.png
Q10_filter_books.png
Q11_post_new_book.png
Q12_update_book.png
Q13_delete_book.png
Q14_queue_add.png
Q15_return_book.png
Q16_search_books.png
Q17_sort_books.png
Q18_paginate_books.png
Q19_borrow_records_search_and_page.png
Q20_browse_combined.png
