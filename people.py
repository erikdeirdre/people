""" Main Flask App """
from os.path import (join, exists, abspath, dirname)
from glob import glob
from sqlalchemy.exc import IntegrityError
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
import click
from app import (APP, DB)


@APP.cli.command('initdb')
def initdb_command():
    """Initializes the database with proper tables"""
    DB.create_all()
    DB.session.commit()
    print(APP.config['SQLALCHEMY_DATABASE_URI'])
    print("Initialized the database")


@APP.cli.command('seed')
@click.argument('directory', default='seed')
@click.argument('demo', default=False)
def seed_command(directory, demo):
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
            load_fixtures(DB, fixtures)
        except IntegrityError as err:
            print('It appears, {}, was already processed'.format(
                fixture_file))
            return False
        print("Processed fixture file: {}".format(fixture_file))

    print("Loading Demo Data")
    if demo:
        for fixture_file in glob(join(base_dir, directory, 'demo', '*.json')):
            fixtures = JSONLoader().load(fixture_file)
            try:
                load_fixtures(DB, fixtures)
            except IntegrityError as err:
                print('It appears, {}, was already processed'.format(
                    fixture_file))
                return False
            print("Processed fixture file: {}".format(fixture_file))

    return True


if __name__ == '__main__':
    APP.run()
