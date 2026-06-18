from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base
from pydantic import BaseModel
from datetime import date

# SQLAlchemy Model
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    amount = Column(Float, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)

# Pydantic Schemas
class ExpenseBase(BaseModel):
    date: date
    amount: float
    category: str
    description: str

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
