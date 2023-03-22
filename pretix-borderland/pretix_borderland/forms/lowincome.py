from django import forms
from pretix.base.forms.widgets import DatePickerWidget
from ..models import LotteryEntry


class LowIncomeForm(forms.ModelForm):
    personal_income = forms.ChoiceField(widget=forms.ComboField(choices=LowIncomeEntry.IncomeChoices),
                                        label="Which of these describes your personal income last year?")
    household_income = forms.ChoiceField(widget=forms.ComboField(choices=LowIncomeEntry.IncomeChoices),
                                         label="Which of these describes your household income last year?")
    class Meta:
        model = LotteryEntry
        fields = ["email", "email_again", "first_name", "last_name", "dob"]