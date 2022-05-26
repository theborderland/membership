from django import forms
from pretix.base.forms.widgets import DatePickerWidget
from ..models import WaitingList


class JoinWaitingList(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Legal First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="Legal Last Name")
    email = forms.EmailField()
    dob = forms.DateField(
        required=True,
        label='Date of Birth',
        widget=DatePickerWidget(),
    )

    class Meta:
        model = WaitingList
        fields = ["email", "first_name", "last_name", "dob"]
