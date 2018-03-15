from datetime import date, timedelta

from board.models import Task, Sprint

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def client(django_user_model):
    """ create user to token and DRF client """
    user = django_user_model.objects.create_user(
        username='tester', password='secret')
    token = Token.generate_key(user)
    client = APIClient()
    client.force_authenticate(user=user, token=token)
    return client


@pytest.fixture
def sprint(client):
    _date = date.today()
    url = reverse('sprint-list')

    client.post(
        url, {
            'name': 'Django test',
            'description': 'Create a test',
            'end': _date
        },
        format='json')


@pytest.fixture
def task(django_user_model, client, sprint):
    user = django_user_model.objects.get(username='tester')
    sprint = 1  # pk
    url = reverse('task-list')
    msg = {
        'name': 'Create Test',
        'description': 'Test for views in project',
        'sprint': sprint,
        'status': Task.STATUS_TODO,
        'order': 0,
        'assigned': user,
        'started': date.today(),
        'due': date.today(),
        'completed': date.today()
    }

    client.post(url, msg)


def test_list_sprint(client):
    url = reverse('sprint-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_create_sprint(client):
    _date = date.today()
    url = reverse('sprint-list')
    response = client.post(
        url, {
            'name': 'Django test',
            'description': 'Create a test',
            'end': _date
        },
        format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_create_sprint_in_past(client):
    _date = date.today() - timedelta(days=1)
    url = reverse('sprint-list')
    response = client.post(
        url, {
            'name': 'Django test',
            'description': 'Create a test',
            'end': _date
        },
        format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('end') == ['End date cannot be in the past.']


def test_create_sprint_unique_end(client):
    _date = date.today()
    url = reverse('sprint-list')
    msg = {'name': 'Django test', 'description': 'Create a test', 'end': _date}
    client.post(url, msg, format='json')
    response = client.post(url, msg, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get('end') == [
        'sprint with this end already exists.'
    ]


def test_hateoas_in_sprint(client):
    test_create_sprint(client)
    url = reverse('sprint-list')
    response = client.get(url)

    json = response.json()[0]

    assert 'self' in json.get('links')
    assert json['links']['self'].endswith('sprints/1/') is True


def test_get_task_list(client):
    url = reverse('task-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_list_task(client):
    url = reverse('task-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_create_task(django_user_model, client, sprint):
    user = django_user_model.objects.get(username='tester')
    sprint = 1  # pk
    url = reverse('task-list')
    msg = {
        'name': 'Create Test',
        'description': 'Test for views in project',
        'sprint': sprint,
        'status': Task.STATUS_TODO,
        'order': 0,
        'assigned': user,
        'started': date.today(),
        'due': date.today(),
        'completed': date.today()
    }
    response = client.post(url, msg)

    assert response.status_code == status.HTTP_201_CREATED


def test_task_is_json(client, task):
    url = reverse('task-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert isinstance(response.json(), dict)


def test_hateoas_in_task_detail(client, task):
    url = reverse('task-detail', kwargs={'pk': 1})
    response = client.get(url)

    json = response.json()

    assert json['links']['self'].endswith('/tasks/1/')


def test_hateoas_in_task_list(client, task):
    url = reverse('task-list')
    response = client.get(url)

    json = response.json()[0]

    assert json['links']['self'].endswith('/tasks/1/')


def test_task_status_display_is_humanized(client, task):
    url = reverse('task-detail', kwargs={'pk': 1})
    response = client.get(url)

    json = response.json()

    assert isinstance(json['status_display'], str)


def test_task_assigned_is_username(client, task, django_user_model):
    url = reverse('task-detail', kwargs={'pk': 1})
    response = client.get(url)

    json = response.json()

    assert json['assigned'] == 'tester'


@pytest.mark.django_db
def test_task_in_past(django_user_model, client):
    past = date.today() - timedelta(days=1)
    Sprint.objects.create(name='teste!', end=past)

    user = django_user_model.objects.get(username='tester')
    sprint = 1  # pk
    url = reverse('task-list')
    msg = {
        'name': 'Create Test',
        'description': 'Test for views in project',
        'sprint': sprint,
        'status': Task.STATUS_TODO,
        'order': 0,
        'assigned': user,
        'started': date.today(),
        'due': date.today(),
        'completed': date.today()
    }

    response = client.post(url, msg)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.json()['sprint'][0], str)
