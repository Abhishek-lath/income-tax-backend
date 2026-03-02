from fastapi import FastAPI
from pydantic import BaseModel
from tax_engine import *

app = FastAPI(title="Income Tax Pro API")


class TaxInput(BaseModel):
    salary: float
    business: float
    capital: float
    other: float
    age: int

    d80c: float = 0
    nps: float = 0
    d80d_self: float = 0
    d80d_parents: float = 0
    senior_parents: bool = False
    d80g: float = 0
    hra_received: float = 0
    rent_paid: float = 0
    basic_salary: float = 0
    metro: bool = False


@app.get("/")
def home():
    return {"message": "Income Tax Pro API Running"}


@app.post("/calculate")
def calculate_tax(data: TaxInput):

    total_income = data.salary + data.business + data.capital + data.other

    deduction_data = {
        "80C": data.d80c,
        "80CCD1B": data.nps,
        "80D_self": data.d80d_self,
        "80D_parents": data.d80d_parents,
        "senior_parents": data.senior_parents,
        "80G": data.d80g,
        "hra_received": data.hra_received,
        "rent_paid": data.rent_paid,
        "basic_salary": data.basic_salary,
        "metro": data.metro
    }

    total_deductions = calculate_total_deductions(deduction_data)

    # Taxable Income
    taxable_income_old = max(total_income - total_deductions, 0)
    taxable_income_new = total_income  # New regime typically no deductions

    # Base tax (without cess)
    old_tax = calculate_old_regime(total_income, data.age, total_deductions)
    new_tax = calculate_new_regime(total_income)

    # 4% Health & Education Cess
    cess_old = old_tax * 0.04
    cess_new = new_tax * 0.04

    # Final tax payable
    final_tax_old = old_tax + cess_old
    final_tax_new = new_tax + cess_new

    better_option = "Old Regime" if final_tax_old < final_tax_new else "New Regime"

    return {
        "total_income": total_income,
        "total_deductions": total_deductions,
        "taxable_income_old": taxable_income_old,
        "taxable_income_new": taxable_income_new,
        "old_regime_tax": old_tax,
        "new_regime_tax": new_tax,
        "cess_old": cess_old,
        "cess_new": cess_new,
        "final_tax_old": final_tax_old,
        "final_tax_new": final_tax_new,
        "better_option": better_option
    }