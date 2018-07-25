from __future__ import unicode_literals
from django.db import models
import re, bcrypt

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9._]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class PlayerManager(models.Manager):
    def reg_validation(self, postData):
        errors = {}
        #Username validation
        if len(postData['username']) < 3:
            errors['username_length'] = "Username must be at least 3 characters long!"
<<<<<<< HEAD
        elif not USERNAME_REGEX.match(postData['username']):
=======
        elif not EMAIL_REGEX.match(postData['username']):
>>>>>>> e38e878aa438c6e081e462b4dc5ea00b1e8a9fe7
            errors['username_format'] = "Username can only contain letters, numbers, underscores and dots!"
        else:
            players = Player.objects.all()
            for player in players:
                if player.username == postData['username']:
                    errors['username_repeat'] = "This email address has already been taken!"
                    break
        #Email validation
        if len(postData['email']) < 1:
            errors['email_length'] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email format!"
        else:
            players = Player.objects.all()
            for player in players:
                if player.email == postData['email']:
                    errors['email_repeat'] = "This email address has already been taken!"
                    break
        #Password validation
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be at least 8 characters long!"
        elif postData['password'] != postData['repeat_password']:
            errors['repeat_password'] = "Password and repeat password do not match!"
        return errors

    def login_validation(self, postData):
        errors = {}
        players = Player.objects.all()
        email_exists = False
        for player in players:
            if player.email == postData['email']:
                email_exists = True
                if not bcrypt.checkpw(postData['password'].encode(), player.pass_hs.encode()):
                    errors['incorrect_pw'] = "Incorrect password!"
                break
        if not email_exists:
            errors['no_email'] = "This email address doesn't exist!"
        return errors


class Game(models.Model):
    p1_health = models.IntegerField()
    p2_health = models.IntegerField()
    p1_frz = models.BooleanField()
    p2_frz = models.BooleanField()
    p1_brn = models.BooleanField()
    p2_brn = models.BooleanField()
    p1_pos = models.BooleanField()
    p2_pos = models.BooleanField()
    battleground = models.IntegerField()

class Player(models.Model):
    email = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    pass_hs = models.CharField(max_length = 255)
    level = models.IntegerField()
    role = models.IntegerField()
    friends = models.ManyToManyField("self")
<<<<<<< HEAD
    games = models.ManyToManyField(Game, related_name = "players")
=======
    game = models.ForeignKey(Game, related_name = "players")
>>>>>>> e38e878aa438c6e081e462b4dc5ea00b1e8a9fe7
    objects = PlayerManager()


