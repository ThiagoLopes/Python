from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint, Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField(source='get_links')
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, obj):
        request = self.context.get('request')
        username = obj.get_username()
        return {
            'self':
            reverse(
                'user-detail',
                kwargs={User.USERNAME_FIELD: username},
                request=request),
            'tasks':
            '{}?assigned={}'.format(
                reverse('task-list', request=request), username)
        }


class TaskSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField(source='get_links')
    status_display = serializers.SerializerMethodField(
        source='get_status_display')
    assigned = serializers.SlugRelatedField(
        queryset=User.objects.order_by(User.USERNAME_FIELD),
        slug_field=User.USERNAME_FIELD,
        required=False)

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'order',
                  'assigned', 'started', 'due', 'completed', 'links',
                  'status_display')

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse(
                'task-detail', kwargs={'pk': obj.pk}, request=request)
        }

    def validate_sprint(self, value):
        if value:
            if value.end < date.today():
                msg = _('Cannot add task to a past sprint')
                raise serializers.ValidationError(msg)

        if self.instance:
            if (self.instance.status ==
                    Task.STATUS_DONE) and (self.instance.sprint != value):
                msg = _('Cannot change sprint in done tasks')
                raise serializers.ValidationError(msg)

        return value

    def validate(self, attrs):
        sprint = attrs.get('sprint')
        status = attrs.get('status')

        if not sprint and status != Task.STATUS_TODO:
            msg = _('Backloag tasks must have "Not Started" status')
            raise serializers.ValidationError(msg)
        return attrs


class SprintSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField(source='get_links')

    class Meta:
        model = Sprint
        fields = (
            'id',
            'name',
            'description',
            'end',
            'links',
        )

    def get_links(self, obj):
        request = self.context.get('request')

        return {
            'self':
            reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
            'tasks':
            reverse('task-list', request=request) +
            '?sprint={}'.format(obj.pk)
        }

    def validate_end(self, value):
        if value < date.today():
            msg = _('End date cannot be in the past.')
            raise serializers.ValidationError(msg)
        return value
