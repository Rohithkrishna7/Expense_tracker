from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import pandas as pd
import os

from backend import models, database
from backend.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/expenses", response_model=models.ExpenseResponse)
def create_expense(expense: models.ExpenseCreate, db: Session = Depends(database.get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model=List[models.ExpenseResponse])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).order_by(models.Expense.date.desc()).offset(skip).limit(limit).all()
    return expenses

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(database.get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@app.get("/reports/monthly")
def get_monthly_report(db: Session = Depends(database.get_db)):
    # Group by month (YYYY-MM) and calculate total amount
    # SQLite doesn't have a direct strftime that returns a date object easily groupable in all ORMs without raw SQL sometimes,
    # but we can do it directly with sqlite's strftime
    results = db.query(
        func.strftime('%Y-%m', models.Expense.date).label('month'),
        func.sum(models.Expense.amount).label('total')
    ).group_by('month').order_by('month').all()
    
    return [{"month": r[0], "total": r[1]} for r in results if r[0]]

@app.get("/export/excel")
def export_excel(db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).order_by(models.Expense.date.desc()).all()
    
    data = []
    for exp in expenses:
        data.append({
            "Date": exp.date,
            "Category": exp.category,
            "Description": exp.description,
            "Amount": exp.amount
        })
        
    df = pd.DataFrame(data)
    file_path = "expenses_export.xlsx"
    df.to_excel(file_path, index=False)
    
    return FileResponse(path=file_path, filename="expenses.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
