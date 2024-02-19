from django import forms
from pretix.base.forms.widgets import DatePickerWidget
from ..models import LotteryEntry


class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus', 'autocomplete': 'email', 'size': '80%'}),
                            required=True,
                            max_length=100,
                            label="E-mail address")
    email_again = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
                                  required=True,
                                  max_length=100,
                                  label="E-mail address again")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'given-name'}),
                                 required=True,
                                 max_length=100,
                                 label="Legal First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'family-name'}),
                                required=True,
                                max_length=100,
                                label="Legal Last Name")

    dob = forms.DateField(
        required=True,
        label='Date of Birth',
        widget=DatePickerWidget(attrs={'autocomplete':'bday'}))

    dob_again = forms.DateField(
        required=True,
        label='Date of Birth again',
        widget=DatePickerWidget(),
    )

    applied_low_income = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                            initial=False,
                                            required=False,
                                            disabled=False,
                                            label="Low income membership?")

    class Meta:
        model = LotteryEntry
        fields = ["email", "email_again", "first_name", "last_name", "dob", "dob_again"] #, "applied_low_income"]
