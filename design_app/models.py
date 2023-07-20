# Create your models here.
from django.db import models

from django.contrib.auth.models import User
    
class UserDesign(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    design = models.TextField()

    def __str__(self):
        return f"{self.user}, {self.design}"