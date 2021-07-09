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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Tips_likes', blank=True, through='TipsLikes')

    class Meta:
        ordering = ['-id']

    @property
    def owner(self):
        return self.username


class BlogLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED AND ADDS LIKES FUNCTIONALITY
    TO EACH TIP OBJECT

    ARGS:
            GETS TIPS ID AND THEN ADDS IT TO LIKE TABLE
    """
    tip = models.ForeignKey(Tips, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
