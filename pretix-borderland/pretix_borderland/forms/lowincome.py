from django import forms
from ..models import LotteryEntry
from ..models import LowIncomeEntry, IncomeChoices, YesNoDontKnowPreferNotToSay


class LowIncomeForm(forms.ModelForm):
    personal_income = forms.ComboField(fields=IncomeChoices,
                                       label="Which of these describes your personal income last year?")
    household_income = forms.ComboField(fields=IncomeChoices,
                                        label="Which of these describes your household income last year?")
    income_source = forms.ComboField(fields=YesNoDontKnowPreferNotToSay,
                                     label="Do you have a regular income source?")
    social_security = forms.ComboField(fields=YesNoDontKnowPreferNotToSay,
                                       label="Do you receive social security?")

    class Meta:
        model = LotteryEntry
        fields = ["personal_income", "household_income", "income_source", "social_security"]
