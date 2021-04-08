from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    game = models.ForeignKey('game.Game', on_delete=models.CASCADE, null=True)

