import pytest
from datetime import date
from board.models import Task, Sprint


@pytest.mark.django_db
def test_sprint_without_name():
    date_ = date.today()
    sprint = Sprint(description='simple project django', end=date_)

    assert str(sprint) == 'Sprint ending in {}'.format(date_)


def test_sprint_with_name():
    date_ = date.today()
    sprint = Sprint(
        name='Django Project', description='simple project django', end=date_)

    assert str(sprint) == 'Django Project'
