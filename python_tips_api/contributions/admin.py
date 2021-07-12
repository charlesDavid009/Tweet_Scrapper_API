from django.contrib import admin
from .models import *

# Register your models here.

admin.sites.register(Tips)
admin.sites.register(TweetsPythonTips)
admin.sites.register(TipsLikes) #i could move this into a tabular inline with tips but lets leave it like this for now