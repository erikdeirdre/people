from os.path import (join, exists, abspath, dirname)
from glob import glob
from sqlalchemy.exc import *
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
import click
from app import (app, db)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database with proper tables"""
    db.create_all()
    db.session.commit()
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print("Initialized the database")


@app.cli.command('seed')
@click.argument('dir', default='seed')
def seed_command(dir):
    """Load seed data"""
    if not exists(dir):
        print("Directory, {}, doesn't exist ... exiting".format(dir))
        return False

    base_dir = abspath(dirname(__file__))

    for fixture_file in glob(join(base_dir, dir, '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        try:
            load_fixtures(db, fixtures)
        except IntegrityError as err:
            print('It appears, {}, was already processed'.format(
                fixture_file))


if __name__ == '__main__':
    app.run()
