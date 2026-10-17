import json
import os

class Book:
    def __init__(self, book_id, title, author, is_borrowed=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed
        }

class Member:
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books else []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }

class Library:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = {}
        self.members = {}
        self.load_data()

    def load_data(self):
        """Load books and members from JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    for b_data in data.get("books", []):
                        self.books[b_data["book_id"]] = Book(**b_data)
                    for m_data in data.get("members", []):
                        self.members[m_data["member_id"]] = Member(**m_data)
            except json.JSONDecodeError:
                pass

    def save_data(self):
        """Save current library state to JSON file."""
        data = {
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()]
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            return "Error: Book ID already exists!"
        self.books[book_id] = Book(book_id, title, author)
        self.save_data()
        return "Book added successfully!"

    def register_member(self, member_id, name):
        if member_id in self.members:
            return "Error: Member ID already exists!"
        self.members[member_id] = Member(member_id, name)
        self.save_data()
        return "Member registered successfully!"

    def borrow_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Error: Member not found!"
        if book_id not in self.books:
            return "Error: Book not found!"
        
        book = self.books[book_id]
        member = self.members[member_id]

        if book.is_borrowed:
            return f"Error: '{book.title}' is already borrowed."

        book.is_borrowed = True
        member.borrowed_books.append(book_id)
        self.save_data()
        return f"Success: '{book.title}' borrowed by {member.name}."

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Error: Member not found!"
        if book_id not in self.books:
            return "Error: Book not found!"
        
        book = self.books[book_id]
        member = self.members[member_id]

        if book_id not in member.borrowed_books:
            return f"Error: Member did not borrow this book."

        book.is_borrowed = False
        member.borrowed_books.remove(book_id)
        self.save_data()
        return f"Success: '{book.title}' returned by {member.name}."

def main():
    library = Library()
    
    while True:
        print("\n==============================")
        print("   LIBRARY MANAGEMENT CLI     ")
        print("==============================")
        print("1. Add Book")
        print("2. Register Member")
        print("3. View All Books")
        print("4. View All Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            b_id = input("Enter Book ID: ").strip()
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            print(library.add_book(b_id, title, author))
            
        elif choice == "2":
            m_id = input("Enter Member ID: ").strip()
            name = input("Enter Member Name: ").strip()
            print(library.register_member(m_id, name))
            
        elif choice == "3":
            print("\n--- Book Catalog ---")
            if not library.books:
                print("No books available.")
            for b in library.books.values():
                status = "Borrowed" if b.is_borrowed else "Available"
                print(f"ID: {b.book_id} | Title: {b.title} | Author: {b.author} | Status: {status}")
                
        elif choice == "4":
            print("\n--- Registered Members ---")
            if not library.members:
                print("No members registered.")
            for m in library.members.values():
                print(f"ID: {m.member_id} | Name: {m.name} | Borrowed Books: {m.borrowed_books}")
                
        elif choice == "5":
            m_id = input("Enter Member ID: ").strip()
            b_id = input("Enter Book ID to borrow: ").strip()
            print(library.borrow_book(m_id, b_id))
            
        elif choice == "6":
            m_id = input("Enter Member ID: ").strip()
            b_id = input("Enter Book ID to return: ").strip()
            print(library.return_book(m_id, b_id))
            
        elif choice == "7":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()