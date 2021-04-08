""" Main Flask App """
from os.path import (join, exists, abspath, dirname)
from glob import glob
import click
from sqlalchemy.exc import IntegrityError
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
from app import (APP, DB)


@APP.cli.command('initdb')
def initdb_command():
    """Initializes the database with proper tables"""
    print(APP.config['SQLALCHEMY_DATABASE_URI'])
    DB.create_all()
#    DB.session.commit()
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
    print(APP.config['SQLALCHEMY_DATABASE_URI'])

    for fixture_file in glob(join(base_dir, directory, '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        try:
            load_fixtures(DB, fixtures)
        except IntegrityError as err:
            # rollback required, so subsequent files may be processed
            DB.session.rollback()
            print('It appears, {}, was already processed'.format(
                fixture_file))
        print("Processed fixture file: {}".format(fixture_file))

    if demo:
        print("Loading Demo Data")
        for fixture_file in glob(join(base_dir, directory, 'demo', '*.json')):
            fixtures = JSONLoader().load(fixture_file)
            try:
                load_fixtures(DB, fixtures)
            except IntegrityError as err:
                # rollback required, so subsequent files may be processed
                DB.session.rollback()
                print('It appears, {}, was already processed'.format(
                      fixture_file))
            print("Processed fixture file: {}".format(fixture_file))

    return True


if __name__ == '__main__':
    APP.run()
