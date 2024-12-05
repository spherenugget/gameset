from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.FloatField()
    image = models.ImageField(upload_to='games/')
    like_count = models.PositiveIntegerField(default=0)  # Field for like counts
    review_count = models.PositiveIntegerField(default=0)  # Field for review counts

    def __str__(self):
        return self.name

class Comment(models.Model):
    game = models.ForeignKey(Game, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)  # Field for the name of the user
    content = models.TextField()  # Field for the comment content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created

    def __str__(self):
        return f'Comment by {self.user_name} on {self.game.name}'