# Expense Tracker

A full-stack expense tracking application built with FastAPI (Backend) and HTML/CSS/Vanilla JS (Frontend).

## Features
- Add, view, and delete expenses
- Monthly summary reports
- Export all expenses to Excel (.xlsx)

## Setup Instructions

### Prerequisites
- Python 3.9+
- A modern web browser

### Backend Setup

1. Open a terminal and navigate to the project root directory (`C:\projects\expense_tracker`).
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Start the FastAPI server:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   The backend will run at `http://localhost:8000`. The database `expenses.db` will be created automatically on the first run.

### Frontend Setup

1. Simply open the `frontend/index.html` file in your preferred web browser. You can do this by double-clicking the file in your file explorer.
2. The frontend is configured to communicate with the backend at `http://localhost:8000`.

## Usage
- **Add Expense**: Fill out the form to add a new expense.
- **Monthly Reports**: The side panel automatically updates to show your total expenses per month.
- **Export Data**: Click "Export to Excel" to download all your expenses in an Excel spreadsheet.
