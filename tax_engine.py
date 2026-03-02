from deductions import *

def calculate_total_deductions(data):

    d80c = calculate_80C(data["80C"])
    nps = calculate_80CCD1B(data["80CCD1B"])
    d80d = calculate_80D(data["80D_self"], data["80D_parents"], data["senior_parents"])
    d80g = calculate_80G(data["80G"])
    hra = calculate_HRA(data["hra_received"], data["rent_paid"], data["basic_salary"], data["metro"])

    total = d80c + nps + d80d + d80g + hra

    return total


def calculate_new_regime(income):
    slabs = [
        (300000, 0),
        (600000, 0.05),
        (900000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (float('inf'), 0.30)
    ]

    tax = 0
    prev = 0

    for limit, rate in slabs:
        if income > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (income - prev) * rate
            break

    if income <= 700000:
        tax = 0

    return apply_surcharge_and_cess(tax, income)


def calculate_old_regime(income, age, deductions):

    if age < 60:
        basic = 250000
    elif age < 80:
        basic = 300000
    else:
        basic = 500000

    taxable = max(0, income - deductions - basic)

    slabs = [
        (250000, 0.05),
        (500000, 0.20),
        (float('inf'), 0.30)
    ]

    tax = 0
    prev = 0

    for limit, rate in slabs:
        if taxable > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (taxable - prev) * rate
            break

    if income <= 500000:
        tax = 0

    return apply_surcharge_and_cess(tax, income)


def apply_surcharge_and_cess(tax, income):

    surcharge = 0

    if income > 50000000:
        surcharge = tax * 0.37
    elif income > 20000000:
        surcharge = tax * 0.25
    elif income > 10000000:
        surcharge = tax * 0.15
    elif income > 5000000:
        surcharge = tax * 0.10

    tax += surcharge
    tax += tax * 0.04  # cess

    return tax