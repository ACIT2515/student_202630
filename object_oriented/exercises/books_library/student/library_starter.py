"""
Library Management System Exercise
===================================

This is your starter file. Implement the Book and Library classes above the
main() function to make the program run successfully.

Your task:
1. Create a Book class with all required attributes and methods
2. Create a Library class with all required attributes and methods
3. Run `python library.py` to test your implementation
4. Run `pytest test_library.py -v` to verify all tests pass
"""

# TODO: Implement your Book class here
# Requirements:
# - __init__(title, author, isbn) - Initialize book attributes
# - Static method: is_valid_isbn(isbn) - Validate ISBN format
# - Class method: get_total_books() - Return total books created
# - Class attribute: _total_books - Track total books created
# - Instance attributes: title, author, isbn, _is_checked_out
# - Property: status - Return "Available" or "Checked Out"
# - Method: checkout() - Check out the book
# - Method: return_book() - Return the book


# TODO: Implement your Library class here
# Requirements:
# - __init__(name) - Initialize library with name
# - Instance attributes: name, _books (list)
# - Method: add_book(book) - Add a book to the library
# - Method: find_book(title) - Find a book by title
# - Property: book_count - Return total number of books
# - Property: available_count - Return number of available books
# - Method: checkout_book(title) - Check out a book by title


def main():
    """Demonstration of the library management system."""
    # 1. Print header
    print("Library Management System Demo")
    print("=" * 50)

    # 2. Test static methods
    print("\nTesting ISBN validation...")
    print(f"Is '978-0-451-52493-5' valid? {Book.is_valid_isbn('978-0-451-52493-5')}")
    print(f"Is '123' valid? {Book.is_valid_isbn('123')}")

    # 3. Display initial book statistics
    print(f"\nInitial book count: {Book.get_total_books()}")

    # 4. Create library
    library = Library("City Public Library")

    # 5. Create three books
    book1 = Book("1984", "George Orwell", "978-0-451-52493-5")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "978-0-061-12008-4")
    book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-743-27356-5")

    # 6. Add books to library
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # 7. Display library statistics
    print(f"\nLibrary statistics:")
    print(f"Total books: {library.book_count}")
    print(f"Available: {library.available_count}")

    # 8. Display updated book statistics
    print(f"Total books created: {Book.get_total_books()}")

    # 9. Demonstrate checkout
    print(f"\nChecking out '1984'...")
    library.checkout_book("1984")
    print(f"Available books: {library.available_count}")

    # 10. Demonstrate return
    print(f"\nReturning '1984'...")
    book1.return_book()
    print(f"Available books: {library.available_count}")

    # 11. Test invalid ISBN (error handling)
    print("\nTesting invalid ISBN...")
    try:
        bad_book = Book("Test", "Author", "123")
    except ValueError as e:
        print(f"Error caught: {e}")

    # 12. Print closing message
    print("\n" + "=" * 50)
    print("Demo complete!")


if __name__ == "__main__":
    main()
