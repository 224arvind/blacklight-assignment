from django.db import models

# Create your models here.
class UserInfo(models.Model):
  uid = models.TextField()
  name = models.CharField(max_length=200)
  score = models.IntegerField()
  country = models.CharField(max_length=2)
  timestamp = models.DateTimeField()