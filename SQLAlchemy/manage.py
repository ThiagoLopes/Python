import os

import click

from model import Base
from sqlalchemy import create_engine

MODEL = 'models.db'


def create_db():
    click.echo('Creating database...')
    engine = create_engine('sqlite:///' + MODEL)
    Base.metadata.create_all(engine)
    click.echo('Done')


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    """ Create database """
    if os.path.exists(MODEL):
        click.echo('Database exists')
    else:
        create_db()


@cli.command()
def dropdb():
    """ Drop database """
    try:
        os.remove(MODEL)
        click.echo('Droped')
    except OSError:
        click.echo('Database dont exist')
