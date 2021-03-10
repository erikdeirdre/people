""" Routes Module """
from flask_graphql import GraphQLView
from app import (APP, DB)
from .schema import SCHEMA


@APP.route('/')
def hello_world():
    """ Print hello world as poor excuse of a health check """
    print('hello world')
    return 'Hello World!'


APP.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=True, # for having the GraphiQL interface
        get_context=lambda: {'session': DB.session}
    )
)
