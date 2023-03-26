from django import forms
from pretix.base.forms.widgets import DatePickerWidget
from ..models import LotteryEntry


class RegisterForm(forms.ModelForm):
    dob = forms.DateField(
        required=True,
        label='Date of Birth',
        widget=DatePickerWidget(),
    )
    dob_again = forms.DateField(
        required=True,
        label='Date of Birth again',
        widget=DatePickerWidget(),
    )
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label="E-mail address")
    email_again = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  label="E-mail address again")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Legal First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="Legal Last Name")

    applied_low_income = forms.BooleanField(required=False,
                                            label="""
Pause a second and breathe, before clicking the following, ask yourself if you really need it.
<br>
Yes, I'd like to apply to a low income membership
""")

    class Meta:
        model = LotteryEntry
        fields = ["email", "email_again", "first_name", "last_name", "dob", "dob_again", "applied_low_income"]
