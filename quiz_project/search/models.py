from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    iframe = models.TextField()

    def __str__(self):
        return self.title