from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tips(models.Model):
    """
    FORM FIELD FOR USER TO INPUT THEIR PYTHON TIPS 
    """
    user = models.ForeignKey(self, null=True, blank=True, on_delete=models.SET_NULL)
    tips = models.CharField(blank = False, null =False, max_length = 140)
    twitter_id = models.CharField(blank = False, null = False, max_length = 120)
    email = models.EmailField(blank= False, null = False)
    created_at = models.DateTimeField(auto_add_now = True)

    class Meta:
        ordering = ['-id']

    @property
    def owner(self):
        return self.username
