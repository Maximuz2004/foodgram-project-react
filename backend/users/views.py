
from django.shortcuts import render
from djoser.views import UserViewSet

from .models import Subscription, User

class CustumUserViewSet(UserViewSet):
