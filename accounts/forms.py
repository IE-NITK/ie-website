from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Account, Profile, Status
from captcha.fields import ReCaptchaField
from django.conf import settings

def validate_username_available(username):
    """
    validator that throws an error if the given username already exists.
    :param username:
    :return:
    """
    if User.objects.filter(username__icontains=username).count():
        raise forms.ValidationError("This email is already registered")


def validate_username_exists(username):
    """
    alidator that throws an error if the given username doesn't exists.
    :param username:
    :return:
    """
    if not User.objects.filter(username__icontains=username).count():
        raise forms.ValidationError("This email does not exist")


def setup_field(field, placeholder=None):
    """
    This configures the given field to play nice with the bootstrap theme. Additionally, you can add
    an additional argument to set a placeholder text on the field.
    :param field:
    :param placeholder:
    :return:
    """
    field.widget.attrs['class'] = 'form-control'
    if placeholder is not None:
        field.widget.attrs['placeholder'] = placeholder


class BasicForm(forms.Form):
    def disable_field(self, field):
        """
        marks field as disabled
        :param field:
        :return:
        """
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        """
        Marks the given field as errous. The given description is displayed when the form it generated
        :param field: name of the field
        :param description: The error description
        :return:
        """
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]

    def clear_errors(self):
        self._errors = {}


class LoginForm(BasicForm):
    email = forms.EmailField(max_length=50, validators=[validate_username_exists])
    setup_field(email, 'Enter Email here')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    setup_field(password, 'Enter password here')
    captcha_box = ReCaptchaField(
                            public_key=settings.RECAPTCHA_PUBLIC_KEY,
                            private_key=settings.RECAPTCHA_PRIVATE_KEY
                        )
    def clean(self):
        """
        To make sure the password is valid for given email
        :return:
        """
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.mark_error('password', 'Incorrect Password')
        return cleaned_data


class AccountRegisterForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter last name here')
    email = forms.EmailField(max_length=50, validators=[validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter password here")
    password_second = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter password again")
    phone = forms.CharField(label='Phone Number', min_length=1, max_length=10)
    setup_field(phone, "Enter phone number")
    roll_no = forms.CharField(label='Roll Number', min_length=1, max_length=10)
    setup_field(roll_no, "Enter Roll number")
    def clean(self):
        """
        To make sure both passwords fields have the same values in them. If they don't mark
        them as erroneous.
        :return:
        """
        cleaned_data = super(AccountRegisterForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data


class PasswordForm(BasicForm):
    password_current = forms.CharField(label='Current', max_length=50, widget=forms.PasswordInput())
    setup_field(password_current, 'Enter your current password here')
    password_first = forms.CharField(label='New', max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter new password here")
    password_second = forms.CharField(label='', max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter new password again")

    def clean(self):
        """
        To make sure both passwords fields have the same values in them. If they don't, mark
        them as erroneous. Also check if the current and new passwords are they same. If they are, then
        mark them as erroneous (we want different passwords).
        :return:
        """
        cleaned_data = super(PasswordForm, self).clean()
        password_current = cleaned_data.get('password_current')
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_second and password_first:
            if password_second != password_first:
                self.mark_error('password_second', 'Passwords do not match')
            if password_current and password_current == password_first:
                self.mark_error('password_current', 'Your current and new passwords must be different')
        return cleaned_data


class ProfileForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter last name here')
    sex = forms.ChoiceField(required=False, choices=Profile.GENDER)
    setup_field(sex)
    phone = forms.CharField(required=False, max_length=10)
    setup_field(phone, 'Enter phone number here')

    def assign(self, profile):
        profile.firstname = self.cleaned_data['firstname']
        profile.lastname = self.cleaned_data['lastname']
        profile.sex = self.cleaned_data['sex']
        profile.phone = self.cleaned_data['phone']


class SIGForm(BasicForm):
    SigMain1 = forms.ChoiceField(label='Core SIG First Priority', choices=Status.SIG_TYPES_MAIN, required=True)
    setup_field(SigMain1, 'Select first Core SIG')
    SigMain2 = forms.ChoiceField(label='Core SIG Second Priority', choices=Status.SIG_TYPES_MAIN, required=False)
    setup_field(SigMain2, 'Select second Core SIG')
    SigAux1 = forms.ChoiceField(label='Auxiliary SIG First Priority', choices=Status.SIG_TYPES_AUX, required=False)
    setup_field(SigAux1, 'Select first Auxiliary SIG')
    SigAux2 = forms.ChoiceField(label='Auxiliary SIG Second Priority', choices=Status.SIG_TYPES_AUX, required=False)
    setup_field(SigAux2, 'Select second Auxiliary SIG')
    media = forms.BooleanField(label='Select to apply for Media SIG', required=False)

