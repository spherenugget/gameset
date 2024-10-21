from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rate = models.FloatField()
    image = models.ImageField(upload_to='games/')

    def __str__(self):
        return f"{self.name} ({self.id})"