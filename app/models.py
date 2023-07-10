from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os import path


class UserBoards(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    board_id = models.IntegerField(unique=True)
    board_name = models.CharField(max_length=300)
    board_image = models.URLField(blank=True)

    def __str__(self):
        return self.board_name


class Boards(models.Model):
    board_id = models.ForeignKey(UserBoards, on_delete=models.CASCADE)
    slide_id = models.IntegerField(unique=True)
    slide_image = models.URLField(blank=True)
    prompt_content = models.TextField(blank=True)

    
    def __str__(self):
        return f"{self.__class__.__name__}: {str(self.slide_id)}"