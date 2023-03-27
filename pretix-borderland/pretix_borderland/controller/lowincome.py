from ..models import LowIncomeEntry, YesNo, YesNoDontKnowPreferNotToSay


def IsEligibleForLowIncome(entry: LowIncomeEntry):
    minimum_wage_euro = 1000.0
    income = 0.0

    if entry.has_assets == YesNo.Yes:
        return False

    if entry.has_income == YesNo.Yes:
        income += entry.income

    return income <= minimum_wage_euro
