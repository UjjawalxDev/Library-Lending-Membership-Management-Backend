"""A small, friendly command-line library system.

Run with: python main.py
The first run creates data.json automatically.
"""

from datetime import date
from library_service import LibraryManager
from models import Book, Magazine, ReferenceBook, StudentMember, FacultyMember, ResearchStudent, NotifiedMember


def ask(prompt):
    """Read a non-empty answer from the user."""
    while True:
        answer = input(prompt).strip()
        if answer:
            return answer
        print("Please enter something; this field can't be empty.")


def add_item(library):
    item_id = ask("Item ID: ")
    title = ask("Title: ")
    print("1. Book  2. Magazine  3. Reference book")
    kind = input("Item type: ").strip()

    if kind == "1":
        item = Book(item_id, title)
    elif kind == "2":
        item = Magazine(item_id, title)
    elif kind == "3":
        item = ReferenceBook(item_id, title)
    else:
        print("That item type isn't recognised.")
        return

    try:
        library.add_item(item)
        print(f"Added '{title}'.")
    except ValueError as error:
        print(f"Could not add item: {error}")


def add_member(library):
    member_id = ask("Member ID: ")
    name = ask("Member name: ")
    print("1. Student  2. Research student  3. Faculty  4. Notified member")
    kind = input("Member type: ").strip()

    if kind == "1":
        member = StudentMember(member_id, name)
    elif kind == "2":
        member = ResearchStudent(member_id, name)
    elif kind == "3":
        member = FacultyMember(member_id, name)
    elif kind == "4":
        member = NotifiedMember(member_id, name)
    else:
        print("That member type isn't recognised.")
        return

    try:
        library.add_member(member)
        print(f"Registered {name}.")
    except ValueError as error:
        print(f"Could not register member: {error}")


def borrow_item(library):
    member_id = ask("Member ID: ")
    item_id = ask("Item ID: ")
    try:
        loan = library.borrow_item(member_id, item_id)
        print(f"Borrow successful. Due date: {loan['due_date']}")
        member = library.members[member_id]
        if hasattr(member, "send_notice"):
            member.send_notice(f"'{library.items[item_id].title}' is due on {loan['due_date']}.")
    except (ValueError, KeyError) as error:
        print(f"Could not borrow item: {error}")


def return_item(library):
    member_id = ask("Member ID: ")
    item_id = ask("Item ID: ")
    try:
        result = library.return_item(member_id, item_id)
        print(f"Returned. Overdue days: {result['overdue_days']} | Fine: ₹{result['fine']}")
    except (ValueError, KeyError) as error:
        print(f"Could not return item: {error}")


def show_reports(library):
    print("\n--- All items ---")
    for item in library.items.values():
        status = "Available" if item.is_available else "On loan"
        print(f"{item.item_id}: {item.title} ({item.__class__.__name__}) - {status}")

    print("\n--- Available items ---")
    available = [item for item in library.items.values() if item.is_available]
    if not available:
        print("No items are currently available.")
    for item in available:
        print(f"{item.item_id}: {item.title}")

    print("\n--- Active loans ---")
    if not library.loans:
        print("No active loans.")
    for loan in library.loans.values():
        print(f"{loan['item_id']} | {loan['member_id']} | Due: {loan['due_date']}")

    print("\n--- Overdue loans ---")
    overdue = library.overdue_loans()
    if not overdue:
        print("No overdue loans.")
    for loan in overdue:
        print(f"{loan['item_id']} | {loan['member_id']} | Due: {loan['due_date']}")

    print("\n--- Members ---")
    for member in library.members.values():
        print(f"{member.member_id}: {member.name} | Borrowed: {member.borrowed_count}/{member.borrowing_limit}")


def main():
    library = LibraryManager()
    print(f"Welcome to {LibraryManager.library_name}!")

    while True:
        print("\n1. Register item")
        print("2. Register member")
        print("3. Borrow item")
        print("4. Return item")
        print("5. View reports")
        print("6. Save and exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_item(library)
        elif choice == "2":
            add_member(library)
        elif choice == "3":
            borrow_item(library)
        elif choice == "4":
            return_item(library)
        elif choice == "5":
            show_reports(library)
        elif choice == "6":
            library.save()
            print("Your library records have been saved. See you next time!")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
