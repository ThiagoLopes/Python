from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, authentication, permissions, filters

from django.contrib.auth import get_user_model

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .forms import TaskFilter, SprintFilter

User = get_user_model()


class BaseViewSet:
    authentication_classes = (authentication.BasicAuthentication,
                              authentication.TokenAuthentication)

    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAuthenticatedOrReadOnly)

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginage_by = 100

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)


class SprintViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    filter_class = SprintFilter
    search_fields = ('name', )
    ordering_fields = (
        'end',
        'name',
    )


class TaskViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'order', 'started', 'due', 'completed')


class UserViewSet(BaseViewSet, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD)
