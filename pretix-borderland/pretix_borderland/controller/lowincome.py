from ..models import LowIncomeEntry, YesNo, YesNoDontKnowPreferNotToSay


def IsEligibleForLowIncome(entry: LowIncomeEntry):
    points = 0


    return points <= 10
