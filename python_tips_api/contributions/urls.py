from django.urls import path, include
from . import views

urlpatterns = [
    path('Tips/create', views.PostTipsView.as_view()),
    path('Tips/<int:pk>/', views.PostTipsView.as_view()),
    path('Tips/', views.GetTipsList.as_view()),
    path('Tweet/', views.GetTweetsList.as_view()),

    path('Blog/action', views.BlogActionView.as_view()),
]
