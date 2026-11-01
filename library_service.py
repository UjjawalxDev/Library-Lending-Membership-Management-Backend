"""Rules for registering, borrowing, returning, and reporting."""

from datetime import date, timedelta
from models import LibraryItem, Member, Book, Magazine, ReferenceBook
from models import StudentMember, ResearchStudent, FacultyMember, NotifiedMember
from storage import load_records, save_records


class LibraryManager:
    library_name = "Friendly Neighbourhood Library"
    fine_per_day = 5

    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.items = {}
        self.members = {}
        self.loans = {}
        self._load()

    def add_item(self, item):
        if not isinstance(item, LibraryItem):
            raise TypeError("Only LibraryItem objects can be added.")
        if not item.item_id or not item.title:
            raise ValueError("Item ID and title are required.")
        if item.item_id in self.items:
            raise ValueError(f"Item ID '{item.item_id}' is already in use.")
        self.items[item.item_id] = item
        self.save()

    def add_member(self, member):
        if not isinstance(member, Member):
            raise TypeError("Only Member objects can be registered.")
        if not member.member_id or not member.name:
            raise ValueError("Member ID and name are required.")
        if member.member_id in self.members:
            raise ValueError(f"Member ID '{member.member_id}' is already in use.")
        self.members[member.member_id] = member
        self.save()

    def borrow_item(self, member_id, item_id):
        member = self.members[member_id]
        item = self.items[item_id]

        if not item.is_available:
            raise ValueError("That item is not available right now.")
        if item.loan_period_days() <= 0:
            raise ValueError("Reference books cannot be borrowed.")
        if not member.can_borrow():
            raise ValueError("This member has reached their borrowing limit.")

        issue_date = date.today()
        due_date = issue_date + timedelta(days=item.loan_period_days())
        item.checkout()
        member.add_loan(item_id)
        loan = {
            "item_id": item_id,
            "member_id": member_id,
            "issue_date": issue_date.isoformat(),
            "due_date": due_date.isoformat(),
        }
        self.loans[item_id] = loan
        self.save()
        return loan

    def return_item(self, member_id, item_id):
        loan = self.loans.get(item_id)
        if loan is None or loan["member_id"] != member_id:
            raise ValueError("No active loan matches that member and item.")

        due_date = date.fromisoformat(loan["due_date"])
        overdue_days = max((date.today() - due_date).days, 0)
        fine = self.calculate_fine(overdue_days)

        self.items[item_id].checkin()
        self.members[member_id].remove_loan(item_id)
        del self.loans[item_id]
        self.save()
        return {"overdue_days": overdue_days, "fine": fine}

    @staticmethod
    def calculate_fine(overdue_days):
        """A simple, easy-to-change fine rule: ₹5 per overdue day."""
        return max(0, int(overdue_days)) * LibraryManager.fine_per_day

    @classmethod
    def set_fine_per_day(cls, amount):
        if int(amount) < 0:
            raise ValueError("Fine cannot be negative.")
        cls.fine_per_day = int(amount)

    def overdue_loans(self):
        today = date.today()
        return [
            loan for loan in self.loans.values()
            if date.fromisoformat(loan["due_date"]) < today
        ]

    def save(self):
        save_records(self.data_file, self.items, self.members, self.loans)

    def _load(self):
        records = load_records(self.data_file)
        for row in records.get("items", []):
            item_type = row.get("type")
            item_class = {
                "Book": Book,
                "Magazine": Magazine,
                "ReferenceBook": ReferenceBook,
            }.get(item_type)
            if item_class:
                self.items[row["item_id"]] = item_class(
                    row["item_id"], row["title"], row.get("is_available", True)
                )

        member_classes = {
            "Member": Member,
            "StudentMember": StudentMember,
            "ResearchStudent": ResearchStudent,
            "FacultyMember": FacultyMember,
            "NotifiedMember": NotifiedMember,
        }
        for row in records.get("members", []):
            member_class = member_classes.get(row.get("type"))
            if member_class:
                member = member_class(
                    row["member_id"], row["name"], row.get("borrowing_limit")
                )
                self.members[member.member_id] = member

        for loan in records.get("loans", []):
            item_id = loan.get("item_id")
            member_id = loan.get("member_id")
            if item_id in self.items and member_id in self.members:
                self.loans[item_id] = loan
                self.members[member_id].add_loan(item_id)
                self.items[item_id]._is_available = False
