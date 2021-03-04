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
@click.argument('demo', default=False)
def seed_command(dir, demo):
    """
    Populate database with seed data
        [DIR] - directory location of fixtures files, defaults to 'seed'
        [DEMO] - load demo data, defaults to 'false'
    """
    if not exists(directory):
        print("Directory, {}, doesn't exist ... exiting".format(directory))
        return False

    base_dir = abspath(dirname(__file__))

    print("Seeding Database")
    for fixture_file in glob(join(base_dir, directory, '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        try:
            load_fixtures(db, fixtures)
        except IntegrityError as err:
            print('It appears, {}, was already processed'.format(
                fixture_file))
        print("Processed fixture file: {}".format(fixture_file))

    print("Loading Demo Data")
    if demo:
        for fixture_file in glob(join(base_dir, directory, 'demo', '*.json')):
            fixtures = JSONLoader().load(fixture_file)
            try:
                load_fixtures(db, fixtures)
            except IntegrityError as err:
                print('It appears, {}, was already processed'.format(
                    fixture_file))
            print("Processed fixture file: {}".format(fixture_file))


if __name__ == '__main__':
    app.run()
