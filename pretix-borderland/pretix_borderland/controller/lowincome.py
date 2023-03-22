from ..models import LowIncomeEntry, IncomeChoices, YesNoDontKnowPreferNotToSay


def IsEligibleForLowIncome(entry: LowIncomeEntry):
    points = 0

    # Personal income scoring
    if entry.personal_income == IncomeChoices.NoIncome:
        points -= 10
    elif entry.personal_income == IncomeChoices.LessThanTenKSEK:
        points -= 5
    elif entry.personal_income == IncomeChoices.LessThanThirtyKSEK:
        points += 0
    elif entry.personal_income == IncomeChoices.LessThanFiftyKSEK:
        points += 10
    elif entry.personal_income == IncomeChoices.MoreThanFiftyKSEK:
        points += 100

    # Household income scoring
    if entry.household_income == IncomeChoices.NoIncome:
        points -= 15
    elif entry.household_income == IncomeChoices.LessThanTenKSEK:
        points -= 10
    elif entry.household_income == IncomeChoices.LessThanThirtyKSEK:
        points -= 5
    elif entry.household_income == IncomeChoices.LessThanFiftyKSEK:
        points += 5
    elif entry.household_income == IncomeChoices.MoreThanFiftyKSEK:
        points += 50

    # Income source scoring
    if entry.income_source == YesNoDontKnowPreferNotToSay.Yes:
        points += 10
    elif entry.income_source == YesNoDontKnowPreferNotToSay.No:
        points += 0
    elif entry.income_source == YesNoDontKnowPreferNotToSay.DontKnow:
        points += 0
    else:
        points += 0

    # Social security scoring
    if entry.social_security == YesNoDontKnowPreferNotToSay.Yes:
        points -= 10
    elif entry.social_security == YesNoDontKnowPreferNotToSay.No:
        points += 0
    elif entry.social_security == YesNoDontKnowPreferNotToSay.DontKnow:
        points += 0
    else:
        points += 0

    return points <= 10
