from django import forms
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rate = models.FloatField()
    image = models.ImageField(upload_to='games/')

    def __str__(self):
        return f"{self.name} ({self.id})"

class Comment(models.Model): 
    game = models.ForeignKey(Game, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=65, default="anonymous")
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Comment on {self.game.name} by {self.username}"
    
