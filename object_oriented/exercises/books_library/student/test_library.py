"""
Test suite for the Library Management System.

This test file demonstrates pytest class-based test organization and
provides comprehensive testing for the Book and Library classes.

Run tests with: pytest test_library.py -v

32 tests covering:
- Static methods (ISBN validation)
- Class methods and attributes (book counter)
- Instance methods (checkout, return)
- Properties (status, book_count, available_count)
- Integration workflows
"""

import pytest
from library import Book, Library


class TestBookStaticMethods:
    """Test static methods of the Book class."""

    def test_is_valid_isbn_with_13_characters(self):
        """Test ISBN validation with 13 character ISBN."""
        assert Book.is_valid_isbn("9780451524935") is True

    def test_is_valid_isbn_with_17_characters(self):
        """Test ISBN validation with 17 character ISBN (with hyphens)."""
        assert Book.is_valid_isbn("978-0-451-52493-5") is True

    def test_is_valid_isbn_with_invalid_length(self):
        """Test ISBN validation with invalid length."""
        assert Book.is_valid_isbn("123") is False
        assert Book.is_valid_isbn("12345") is False
        assert Book.is_valid_isbn("") is False


class TestBookClassMethods:
    """Test class methods and class attributes of the Book class."""

    def setup_method(self):
        """Reset the book counter before each test."""
        Book._total_books = 0

    def test_total_books_starts_at_zero(self):
        """Test that the total books counter starts at zero."""
        assert Book.get_total_books() == 0

    def test_total_books_increments_on_creation(self):
        """Test that creating books increments the counter."""
        Book("Test Book 1", "Author 1", "9780451524935")
        assert Book.get_total_books() == 1

        Book("Test Book 2", "Author 2", "978-0-451-52493-5")
        assert Book.get_total_books() == 2


class TestBookInitialization:
    """Test Book class initialization."""

    def test_book_creation_with_valid_isbn(self):
        """Test creating a book with valid ISBN."""
        book = Book("1984", "George Orwell", "9780451524935")
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "9780451524935"

    def test_book_creation_with_invalid_isbn_raises_error(self):
        """Test that creating a book with invalid ISBN raises ValueError."""
        with pytest.raises(ValueError, match="Invalid ISBN format"):
            Book("Bad Book", "Bad Author", "123")

    def test_book_starts_not_checked_out(self):
        """Test that a new book is not checked out."""
        book = Book("1984", "George Orwell", "9780451524935")
        assert book._is_checked_out is False


class TestBookProperties:
    """Test Book class properties."""

    def test_status_property_when_available(self):
        """Test status property returns 'Available' for new book."""
        book = Book("1984", "George Orwell", "9780451524935")
        assert book.status == "Available"

    def test_status_property_when_checked_out(self):
        """Test status property returns 'Checked Out' after checkout."""
        book = Book("1984", "George Orwell", "9780451524935")
        book.checkout()
        assert book.status == "Checked Out"

    def test_status_property_is_read_only(self):
        """Test that status property cannot be set directly."""
        book = Book("1984", "George Orwell", "9780451524935")
        with pytest.raises(AttributeError):
            book.status = "Something"


class TestBookMethods:
    """Test Book class instance methods."""

    def test_checkout_available_book(self):
        """Test checking out an available book."""
        book = Book("1984", "George Orwell", "9780451524935")
        result = book.checkout()
        assert result is True
        assert book._is_checked_out is True

    def test_checkout_already_checked_out_book(self):
        """Test checking out a book that's already checked out."""
        book = Book("1984", "George Orwell", "9780451524935")
        book.checkout()
        result = book.checkout()
        assert result is False
        assert book._is_checked_out is True

    def test_return_checked_out_book(self):
        """Test returning a checked out book."""
        book = Book("1984", "George Orwell", "9780451524935")
        book.checkout()
        result = book.return_book()
        assert result is True
        assert book._is_checked_out is False

    def test_return_available_book(self):
        """Test returning a book that wasn't checked out."""
        book = Book("1984", "George Orwell", "9780451524935")
        result = book.return_book()
        assert result is False
        assert book._is_checked_out is False

    def test_checkout_and_return_cycle(self):
        """Test multiple checkout/return cycles."""
        book = Book("1984", "George Orwell", "9780451524935")

        # First cycle
        assert book.checkout() is True
        assert book.return_book() is True

        # Second cycle
        assert book.checkout() is True
        assert book.return_book() is True

        assert book._is_checked_out is False


class TestLibraryInitialization:
    """Test Library class initialization."""

    def test_library_creation(self):
        """Test creating a library."""
        library = Library("City Public Library")
        assert library.name == "City Public Library"

    def test_library_starts_with_empty_book_list(self):
        """Test that a new library has no books."""
        library = Library("City Library")
        assert len(library._books) == 0


class TestLibraryProperties:
    """Test Library class properties."""

    def setup_method(self):
        """Set up a library with books for testing."""
        Book._total_books = 0
        self.library = Library("Test Library")
        self.book1 = Book("Book 1", "Author 1", "9780451524935")
        self.book2 = Book("Book 2", "Author 2", "978-0-061-12008-4")
        self.book3 = Book("Book 3", "Author 3", "978-0-743-27356-5")

    def test_book_count_property(self):
        """Test book_count property."""
        assert self.library.book_count == 0

        self.library.add_book(self.book1)
        assert self.library.book_count == 1

        self.library.add_book(self.book2)
        assert self.library.book_count == 2

    def test_available_count_property_all_available(self):
        """Test available_count when all books are available."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        assert self.library.available_count == 2

    def test_available_count_property_some_checked_out(self):
        """Test available_count when some books are checked out."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)

        self.book1.checkout()
        assert self.library.available_count == 2

        self.book2.checkout()
        assert self.library.available_count == 1

    def test_available_count_property_all_checked_out(self):
        """Test available_count when all books are checked out."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        self.book1.checkout()
        self.book2.checkout()
        assert self.library.available_count == 0


class TestLibraryMethods:
    """Test Library class instance methods."""

    def setup_method(self):
        """Set up a library with books for testing."""
        Book._total_books = 0
        self.library = Library("Test Library")
        self.book1 = Book("1984", "George Orwell", "9780451524935")
        self.book2 = Book("To Kill a Mockingbird", "Harper Lee", "978-0-061-12008-4")

    def test_add_book(self):
        """Test adding a book to the library."""
        self.library.add_book(self.book1)
        assert self.library.book_count == 1
        assert self.book1 in self.library._books

    def test_add_multiple_books(self):
        """Test adding multiple books to the library."""
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        assert self.library.book_count == 2

    def test_find_book_by_title(self):
        """Test finding a book by exact title."""
        self.library.add_book(self.book1)
        found_book = self.library.find_book("1984")
        assert found_book is self.book1

    def test_find_book_case_insensitive(self):
        """Test that find_book is case insensitive."""
        self.library.add_book(self.book1)
        found_book = self.library.find_book("to kill a mockingbird")
        assert found_book is None  # Book1 is "1984", not "To Kill..."

        self.library.add_book(self.book2)
        found_book = self.library.find_book("to kill a mockingbird")
        assert found_book is self.book2

    def test_find_book_not_in_library(self):
        """Test finding a book that doesn't exist."""
        self.library.add_book(self.book1)
        found_book = self.library.find_book("Nonexistent Book")
        assert found_book is None

    def test_checkout_book_by_title(self):
        """Test checking out a book using its title."""
        self.library.add_book(self.book1)
        result = self.library.checkout_book("1984")
        assert result is True
        assert self.book1._is_checked_out is True

    def test_checkout_book_not_in_library(self):
        """Test checking out a book that doesn't exist."""
        result = self.library.checkout_book("Nonexistent Book")
        assert result is False


class TestIntegration:
    """Integration tests combining multiple classes and features."""

    def setup_method(self):
        """Reset counters and set up test data."""
        Book._total_books = 0

    def test_complete_library_workflow(self):
        """Test a complete workflow of library operations."""
        # Create library
        library = Library("City Library")
        assert library.name == "City Library"

        # Create books
        book1 = Book("1984", "George Orwell", "9780451524935")
        book2 = Book("Sapiens", "Yuval Noah Harari", "9780062316097")

        # Add books to library
        library.add_book(book1)
        library.add_book(book2)

        # Check counts
        assert library.book_count == 2
        assert library.available_count == 2
        assert Book.get_total_books() == 2

        # Checkout a book
        result = library.checkout_book("1984")
        assert result is True
        assert library.available_count == 1

        # Return the book
        book1.return_book()
        assert library.available_count == 2

    def test_multiple_libraries(self):
        """Test working with multiple libraries."""
        library1 = Library("City Library")
        library2 = Library("County Library")

        book1 = Book("Book 1", "Author 1", "9780451524935")
        book2 = Book("Book 2", "Author 2", "978-0-061-12008-4")

        library1.add_book(book1)
        library2.add_book(book2)

        assert library1.book_count == 1
        assert library2.book_count == 1
        assert Book.get_total_books() == 2

    def test_class_attributes_shared_across_instances(self):
        """Test that class attributes are truly shared."""
        # Reset counters
        Book._total_books = 0
        Library._all_libraries = []

        # Create books and check counter
        book1 = Book("Book 1", "Author 1", "9780451524935")
        initial_count = Book.get_total_books()

        book2 = Book("Book 2", "Author 2", "978-0-061-12008-4")
        new_count = Book.get_total_books()

        assert new_count == initial_count + 1
        assert book1.get_total_books() == book2.get_total_books()
