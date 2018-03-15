from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('sprints', views.SprintViewSet)
router.register('tasks', views.TaskViewSet)
router.register('users', views.UserViewSet)
