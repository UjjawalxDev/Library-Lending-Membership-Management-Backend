# Library Lending & Membership Management

A beginner-friendly Python OOP mini-project based on the Module 8 brief.

## Run it

1. Make sure Python 3.9+ is installed.
2. Open a terminal in this folder.
3. Run:

   ```bash
   python main.py
   ```

The program uses only Python's standard library. It creates `data.json` the first time you save records.

## What's included

- `models.py` — abstract library item, item types, member types, and notification mixin.
- `library_service.py` — registration, checkout, returns, overdue reports, and fines.
- `storage.py` — JSON save/load helpers.
- `main.py` — simple command-line menu.
- `data.json` — starter data; the program updates it as you use the menu.

## Borrowing rules

- Books: 14 days.
- Magazines: 7 days.
- Reference books: not lendable.
- Standard member limit: 3 active loans.
- Research students and faculty: default limit of 5.
- Fine: ₹5 per overdue day.

The code uses plain names and short comments to make it easier to read and explain in a viva.
