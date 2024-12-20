from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import secrets
# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_games')
    gridsize = models.IntegerField(default=3)
    alignement = models.IntegerField(default=3)
    gameover = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    full = models.BooleanField(default=False)
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='joined_games')
    current_player = models.CharField(max_length=100, null=True, blank=True)
    access_code = models.CharField(default="a", max_length=8, unique=True,blank=True)
    board = models.JSONField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loser', null=True, blank=True)
    is_ff = models.BooleanField(default=False)
    exist_winner = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.access_code == "a":
            self.access_code = secrets.token_urlsafe(6).upper()     # Générer un code d'accès aléatoire
        super().save(*args, **kwargs)
        self.board = [[None for _ in range(self.gridsize)] for _ in range(self.gridsize)]

    def get_next_player(self):
        if self.current_player == self.author:
            return User.objects.exclude(id=self.author.id).first()
        else:
            return self.author

    def get_board(self):
        return self.board
