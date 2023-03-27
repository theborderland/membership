from django import forms
from django_countries.fields import CountryField
from ..models import LowIncomeEntry, YesNoDontKnowPreferNotToSay, YesNo


class LowIncomeForm(forms.ModelForm):
    country = CountryField().formfield(initial='SE',
                                       required=True,
                                       label="Which country do you live in?")

    has_income = forms.TypedChoiceField(choices=[(tag.value, tag.name) for tag in YesNo],
                                        coerce=str,
                                        initial=YesNo.No,
                                        required=True,
                                        label="Do you have a job, are self-employed, or "
                                              "receive any form of benefits (e.g., unemployment benefits, "
                                              "dividends, family support)?")

    income = forms.DecimalField(label="How much a month do you earn/receive right now (in Euro and before tax)?",
                                min_value=0.0,
                                max_digits=10,
                                decimal_places=2,
                                required=True,
                                initial=0.00,
                                localize=False)

    income_last_year = forms.DecimalField(
        label="How much a month did you earn/receive on average last year (in Euro and before tax)?",
        min_value=0.0,
        max_digits=20,
        decimal_places=2,
        required=True,
        initial=0.00,
        localize=False)

    has_assets = forms.TypedChoiceField(choices=[(tag.value, tag.name) for tag in YesNoDontKnowPreferNotToSay],
                                        coerce=str,
                                        initial=YesNoDontKnowPreferNotToSay.DontKnow,
                                        label="Do you own any assets (house, cash, crypto, stocks, unicorns, etc.)?")

    assets = forms.DecimalField(label="What is the value of the assets that you own (in Euro)?",
                                min_value=0.0,
                                max_digits=20,
                                decimal_places=2,
                                required=True,
                                initial=0.00,
                                localize=False)

    class Meta:
        model = LowIncomeEntry
        fields = ["country", "has_income", "income", "income_last_year", "has_assets", "assets"]
