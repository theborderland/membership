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

    class Meta:
        model = LotteryEntry
        fields = ["email", "email_again", "first_name", "last_name", "dob"]
