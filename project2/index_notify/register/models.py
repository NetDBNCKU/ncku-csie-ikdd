from django.db import models

# Create your models here.

class Member(models.Model):
    email = models.EmailField()
    what = models.CharField(max_length=256)
    lower = models.FloatField()
    upper = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
