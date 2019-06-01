from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    datePublished = models.DateField(auto_now_add=True)

    def __str__(self):
        # return "{} published on {} ".format(self.title, self.datePublished)
        return f"{self.title} published on {self.datePublished}"

