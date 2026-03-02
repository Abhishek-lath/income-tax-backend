def calculate_80C(amount):
    return min(amount, 150000)

def calculate_80CCD1B(nps_amount):
    return min(nps_amount, 50000)

def calculate_80D(self_family, parents, senior_parents=False):
    limit_self = 25000
    limit_parents = 25000

    if senior_parents:
        limit_parents = 50000

    return min(self_family, limit_self) + min(parents, limit_parents)

def calculate_80G(donation):
    # simplified 50% deduction
    return donation * 0.5

def calculate_HRA(hra_received, rent_paid, basic_salary, metro=True):
    percent_salary = 0.5 if metro else 0.4
    exemption = min(
        hra_received,
        rent_paid - (0.1 * basic_salary),
        percent_salary * basic_salary
    )
    return max(0, exemption)