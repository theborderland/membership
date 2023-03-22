from django import forms
from ..models import LotteryEntry, LowIncomeEntry


class LowIncomeForm(forms.ModelForm):
    personal_income = forms.ChoiceField(widget=forms.ComboField(choices=LowIncomeEntry.INCOME_CHOICES),
                                        label="Which of these describes your personal income last year?")
    household_income = forms.ChoiceField(widget=forms.ComboField(choices=LowIncomeEntry.INCOME_CHOICES),
                                         label="Which of these describes your household income last year?")
    income_source = forms.ChoiceField(widget=forms.ComboField(choices=LotteryEntry.YES_NO_PREFER_NOT_TO_SAY),
                                    label="Do you have income from any sources other than salary?")
    social_security = forms.ChoiceField(widget=forms.ComboField(choices=LotteryEntry.YES_NO_PREFER_NOT_TO_SAY),
                                      label="Do you receive social security benefits or disability income as your main income?")

    class Meta:
        model = LotteryEntry
        fields = ["personal_income",
                  "household_income",
                  "income_source",
                  "social_security"]