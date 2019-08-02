from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER = (
        ('M', "Male"),
        ('F', "Female"),
    )

    @staticmethod
    def to_gender(key):
        for item in Profile.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    sex = models.CharField(blank=True, max_length=1, choices=GENDER)
    phone = models.CharField(blank=True, max_length=10)

    def get_populated_fields(self):
        """
        To collect form data
        :return:
        """
        fields = {}
        if self.firstname is not None:
            fields['firstname'] = self.firstname
        if self.lastname is not None:
            fields['lastname'] = self.lastname
        if self.sex is not None:
            fields['sex'] = self.sex
        if self.phone is not None:
            fields['phone'] = self.phone

        return fields

    def __str__(self):
        return self.firstname + " " + self.lastname


class Account(models.Model):
    ACCOUNT_ADMIN = 1
    ACCOUNT_MEMBER = 2
    ACCOUNT_CANDIDATE = 3
    ACCOUNT_AUX_ADMIN = 4
    ACCOUNT_TYPES = (
        (ACCOUNT_ADMIN, "Admin"),
        (ACCOUNT_MEMBER, "Member"),
        (ACCOUNT_CANDIDATE, "Candidate"),
        (ACCOUNT_AUX_ADMIN, "Aux SIG Admin")
    )
    SIG_CHOICES = (("--", "NONE"), ("CO", "Code"),
                 ("GD", "Gadget"),
                 ("GR", "Garage"),)
    #TODO: AUX SIGS

    @staticmethod
    def to_name(key):
        """
        Parses an integer value to a string representing an account role.
        :param key: The account role as a int
        :return: The integer representation of the account role
        """
        key = key.lower()
        for item in Account.ACCOUNT_TYPES:
            if item[1].lower() == key:
                return item[0]
        return 0

    @staticmethod
    def to_sig(key):
        key = key.lower()
        for item in Account.SIG_CHOICES:
            if item[1].lower() == key:
                return item[0]
        return "None"

    role = models.IntegerField(default=0, choices=ACCOUNT_TYPES)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    SIG = models.CharField(null=True, max_length=2)

    def __str__(self):
        return self.profile.__str__()


class Status(models.Model):
    STATUS_TYPES = (
        ("RE", "Application Accepted"),
        ("WR", "Written Round"),
        ("TE", "Technical"),
        ("HR", "HR")
    )
    SIG_TYPES_MAIN = (("", "None"), ("CO", "Code"),
                      ("GD", "Gadget"),
                      ("GR", "Garage"),)
    SIG_TYPES_AUX = (("", "None"), ("SR", "Script"),
                     ("RO", "Robotics"),
                     ("CA", "Capital"),
                     ("ME", "Media"))
    SIG_TYPES = (
        ("CO", "Code"),
        ("GD", "Gadget"),
        ("GR", "Garage"),
        ("SR", "Script"),
        ("RO", "Robotics"),
        ("CA", "Capital"),
        ("ME", "Media")
    )

    @staticmethod
    def to_status(key):
        key = key.lower()
        for item in Status.STATUS_TYPES:
            if item[1].lower() == key:
                return item[0]
        return "None"

    @staticmethod
    def to_sig(key):
        key = key.lower()
        for item in Status.SIG_TYPES:
            if item[1].lower() == key:
                return item[0]
        return "None"

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    SIG = models.CharField(null=True, max_length=2)
    status = models.CharField(max_length=2, choices=STATUS_TYPES)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.SIG + ": " + self.user.__str__()
