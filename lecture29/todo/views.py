# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

from .serializers import TodoSerializer
from .models import Todo

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    permission_classes = [IsAuthenticated]
    # authentication_classes = []
