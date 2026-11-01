"""The objects that represent library items and people."""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Common details shared by every item the library owns."""

    def __init__(self, item_id, title, is_available=True):
        self.item_id = str(item_id).strip()
        self.title = str(title).strip()
        self._is_available = bool(is_available)

    @property
    def is_available(self):
        """Availability is readable, but changes go through checkout/return."""
        return self._is_available

    def checkout(self):
        if not self._is_available:
            raise ValueError("This item is already checked out.")
        self._is_available = False

    def checkin(self):
        self._is_available = True

    @abstractmethod
    def loan_period_days(self):
        """Return how many days this item may be borrowed."""


class Book(LibraryItem):
    def loan_period_days(self):
        return 14


class Magazine(LibraryItem):
    def loan_period_days(self):
        return 7


class ReferenceBook(LibraryItem):
    """Reference books stay in the library and cannot be borrowed."""

    def loan_period_days(self):
        return 0


class Member:
    """Base account for anyone who has a library card."""

    default_borrowing_limit = 3

    def __init__(self, member_id, name, borrowing_limit=None):
        self.member_id = str(member_id).strip()
        self.name = str(name).strip()
        self.borrowing_limit = (
            self.default_borrowing_limit if borrowing_limit is None else int(borrowing_limit)
        )
        self._active_loans = set()

    @property
    def borrowed_count(self):
        return len(self._active_loans)

    def can_borrow(self):
        return self.borrowed_count < self.borrowing_limit

    def add_loan(self, item_id):
        self._active_loans.add(str(item_id))

    def remove_loan(self, item_id):
        self._active_loans.discard(str(item_id))

    @classmethod
    def set_default_borrowing_limit(cls, limit):
        if int(limit) < 1:
            raise ValueError("The borrowing limit must be at least 1.")
        cls.default_borrowing_limit = int(limit)


class StudentMember(Member):
    def __init__(self, member_id, name, borrowing_limit=None):
        super().__init__(member_id, name, borrowing_limit)


class ResearchStudent(StudentMember):
    """Research students get a little more time and a higher default limit."""

    def __init__(self, member_id, name, borrowing_limit=None):
        super().__init__(member_id, name, borrowing_limit if borrowing_limit is not None else 5)


class FacultyMember(Member):
    def __init__(self, member_id, name, borrowing_limit=None):
        super().__init__(member_id, name, borrowing_limit if borrowing_limit is not None else 5)


class NotificationMixin:
    """A small mixin for members who can receive checkout reminders."""

    def send_notice(self, message):
        print(f"[Notice for {self.name}] {message}")


class NotifiedMember(Member, NotificationMixin):
    # MRO: NotifiedMember -> Member -> NotificationMixin -> object.
    # Member has no send_notice(), so Python finds it on NotificationMixin.
    pass
