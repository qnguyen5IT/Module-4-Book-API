from flask import Flask, jsonify, request

app = Flask(__name__)

# Data
books = [
    {"id": 1, "book_name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publisher": "Charles Scribner's Sons"},
    {"id": 2, "book_name": "Dune", "author": "Frank Herbert", "publisher": "Chilton Books"}
]

# Helper function to find a book by ID
def find_book(id):
    return next((book for book in books if book["id"] == id), None)

@app.route('/')
def home():
    return "Book API is running!"

# GET all books/POST a new book
@app.route('/books', methods=['GET', 'POST'])
def books_route():
    if request.method == 'GET':
        return jsonify({"books": books})
    
    # POST: Add a new book
    new_book = request.get_json()
    new_book["id"] = books[-1]["id"] + 1 if books else 1
    books.append(new_book)
    return jsonify({"book": new_book}), 201

# GET, PUT, DELETE for a SINGLE book by ID
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def book_route(id):
    book = find_book(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    if request.method == 'GET':
        return jsonify({"book": book})
    
    if request.method == 'PUT':
        updated_data = request.get_json()
        book.update(updated_data)
        return jsonify({"book": book})
    
    # DELETE
    books[:] = [b for b in books if b["id"] != id]  # Modify list without global
    return jsonify({"message": "Book deleted"})

if __name__ == '__main__':
    app.run(debug=True)