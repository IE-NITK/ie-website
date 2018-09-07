from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from accounts.models import Account, Profile
from accounts import forms as aforms
from accounts.forms import setup_field
from accounts.forms import BasicForm


class AddUserForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter last name')
    email = forms.EmailField(max_length=50, validators=[aforms.validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter password here")
    password_second = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter password again")
    member_type = forms.ChoiceField(required=False, choices=Account.USER_TYPES)
    setup_field(member_type)

    def clean(self):
        """
        This is to make sure both passwords fields have the same values in them. If they don't mark
        them as errous.
        :return:
        """
        cleaned_data = super(AddUserForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data