from __future__ import unicode_literals
from django.db import models
import re
import md5
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
BIRTHDAY_REGEX = re.compile(r"(^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$)")
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add = True)

class Quote(models.Model):
    content = models.CharField(max_length=1000)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    
class Registration(object):
    def __init__(self):
        self.is_valid = True
        self.id = ""
        self.message = []
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.birthday = ""
        self.pw_1 = ""
        self.pw_2 = ""
        self.pw_hash = ""

    def validate(self):
        if User.objects.filter(email=self.email.lower()).exists():
            self.is_valid = False
            self.message.append("Email already exists!")
        if len(self.first_name) < 1:
            self.message.append("First Name must not be empty!")
            self.is_valid = False
        if len(self.last_name) < 1:
            self.message.append("Last Name must not be empty!")
            self.is_valid = False
        if len(self.email) < 1 or not EMAIL_REGEX.match(self.email):
            self.message.append("Email not valid!")
            self.is_valid = False
        if len(self.pw_1) < 8 or len(self.pw_2) < 8:
            self.message.append("Password fields must be longer than 8 characters!")
            self.is_valid = False
        if self.pw_1 != self.pw_2:
            self.message.append("Passwords do not match!")
            self.is_valid = False
        if not BIRTHDAY_REGEX.match(self.birthday):
            self.message.append("Birthday format not correct!")
            self.is_valid = False
        if not self.first_name.isalpha() or not self.last_name.isalpha():
            self.message.append("Name Field must be letters!")
            self.is_valid = False
        if self.is_valid:
            self.pw_hash = bcrypt.hashpw(self.pw_1, bcrypt.gensalt())

    def create_user(self):
        if self.is_valid:
            self.id = User.objects.create(first_name=self.first_name,
             last_name=self.last_name,email=self.email, birthday=self.birthday,
             password=self.pw_hash)
            self.id = self.id.id

class Login(object):
    def __init__(self):
        self.email = ""
        self.pw = ""
        self.validate = True
        self.message = []
        self.id = ""
        self.user = ""
    def validation(self):
        if not User.objects.filter(email=self.email).exists():
            self.validate = False
            self.message.append("Email doesn't exist, please try again.")
        if self.validate:
            self.user = User.objects.filter(email=self.email)
            if not bcrypt.hashpw(self.pw, self.user[0].password.encode()) == self.user[0].password.encode():
                self.validate = False
                self.message.append("Password does not match, please try again.")
        if self.validate:
            self.id = self.user[0].id
