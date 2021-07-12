from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwner
from django.conf import settings
from django.db.models import Q

from . models import *
from . serializers import *
import tweepy
import twitter
import os

class GetTipsList(generics.ListAPIView):
    """
    GET ALL TIPS MADE BY USERS ON THE SITE
    ARGS:
            ONLY ADMINS CAN GET TO SEE THESE TIPS
    """

    serializer_class = TipsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Tips.objects.all()
        return qs


class PostTipsView(generics.CreateAPIView):
    """
    CREATES TIPS AND SAVE USERS TIPS TO DATABASE
    AFTER FORM VALIDATION IS TRUE:

    ARGS:
            ANYONE CAN CONTRIBUTE TIPS TO THE SITE
    """
    serializer_class = CreateTipSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        return Tips.objects.all()

    def perform_create(self, serializer):
        users = self.request.user
        serializer.save(user=users)


class PostTipsView(generics.RetriveUpdateDestroyAPIView):
    """
    UPDATES USER'S TIPS AND SAVE USER'S TIPS TO DATABASE
    AFTER FORM VALIDATION IS TRUE:

    ARGS:
            ONLY OWNER OF TISP CAN UPDATE A TIP
    """
    lookup                  = 'pk'
    serializer_class        = CreateTipSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Tips.objects.all()

class GetTweetLists(generics.ListAPIView):
    """
    GETS ALL TWEETS POSTS ON TWITTER

    ARGS:
            GETS TWEETS FROM TWITTER ASSCOIATED TO DAILY TIPS PYTHON
    """
    serializer_class = TweetSerializer

    def get_queryset(self):
        """
        Gets ALL TWEETS SAVED IN DATABASE FROM TWITTER API
        """
        qs = Tweets.Objects.all()
        return qs


class BlogActionView(generics.CreateAPIView):
    """
    THIS VIEW CREATES THE LIKE OBJECT BY TAKING
    THE ID OF THE OBJECT AND THEN ADDING THE ACTION
    USER WISHES TO COMPLAIN ABOUT

    ARGS:
            ID OF TIPS
            ACTION PERFORMED BY USER
    """

    queryset = Tips.objects.all()
    serializer_class = ActionTipsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs): #- Returns a serializer instance.
        serializer = ActionTipsSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id')
            action = data.get('action')
            queryset = self.get_queryset()
            qs = queryset.filter(id = blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.likes.add(self.request.user)
                serializer = BlogSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)
            elif action == "unlike":
                    obj.likes.remove(request.user)
                    serializer = BlogSerializer(obj)
                    return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
