# people

Module to manage people in a system.

It uses a base person class along with specialized people.

## Initial Setup

-   Create a virtualenv
-   Run `pip install -r requirements.txt`
-   Set environment variables:
        `FLASK_APP=people.py`
        `SQLALCHEMY_URI=<your database connection string>`
        `SQLALCHEMY_DATABASE_URI=SQLALCHEMY_URI`
        `USPS_USERID="<USPS User Id>"`
-   Set `GRAPHIQL=true`, if you wish to use the 'GraphiQL' interface.

### Flask Options

Two additional, `flask` commands exist for prepping the database.

-   `initdb` creates the table schema for the application. Shouldn't be needed. `flask db upgrade` should be used instead.

-   `seed` populates the database with data found in the directory specified. `DEMO` loads demo data. It's not intended to do updates, only initial data load.
    Usage: `flask seed {load files directory} (defaults to 'seed') {demo switch} (defaults to 'false')`.

### Running Graphql

You should be able to access the `graphql` console via `http://127.0.0.1:5000/graphql`


## Troubleshooting

If the system reports

```bash
Usage: flask [OPTIONS] COMMAND [ARGS]...
Try "flask --help" for help.

Error: No such command "command".
```

when executing some commands then confirm you set `FLASK_APP=people.py`.

## Database Changes

# Database

This section manages the database. It's primary focus is SqlAlchmey models used by other scripts. Additionally, it houses the migration scripts used for managing the database schema. 

**NOTE:** The database is geared for Postgresql. It hasn't been tested with other database server types.


`models.py` describes the tables using SqlAlchemy.

`migrations` directory holds the migrations scripts.

`alembic.ini` configures the migration process. There's a copy of this file in `../migrations_config` if you need to redo the migrations process.

`functions` directory contains Postgres function code.

`views` directory contains Postgres view code.

## Database Migrations

`flask db`, 'Alembic under the covers', is used for database migrations; making changes to tables.

Alembic is configured to generate migration files from changes to `models.py`. Manual modifications can be accomplished by manually changing the generated files.

### Migration Steps

3. Set `SQLALCHEMY_DATABASE_URI` to point to the proper database.

4. Run `flask db migrate -m "<some comment>"` to generate a new 'version' file within the 'versions' directory.

5. Check the `migrations` directory for a file matching your comment. Confirm the file has the expected changes. If not, you'll need to modify it so it aligns with the model changes you made earlier. 

6. Run `flask db upgrade` to apply all version files.

**Important Note:** Migration must occur prior to 'seeding the database.

Run `flask db upgrade` followed by `flask seed`.


### Issues and Solutions

This section is dedicated to the problems and subsequent solutions encountered while working on the code.

**Problem**

```bash
(.env)% alembic revision --autogenerate -m "Create New Table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
ERROR [alembic.util.messaging] Target database is not up to date.
  FAILED: Target database is not up to date.
```

**Solution**

The migration script can't connect to a database. Make sure the environment variable, `SQLALCHEMY_URI` is set to the proper database.

**Problem**

The command `alembic revision <command>` results in ...

```bash
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "migrations/env.py", line 11, in <module>
    from database import models
ModuleNotFoundError: No module named 'database'
```

**Solution**

`PYTHONPATH` isn't set correctly. Set it to point to the root of the workspace.

**Problem**

Running `alembic` command results in ` FAILED: No config file 'alembic.ini' found, or file has no '[alembic]' section`

**Solution**

Change to the `app` directory and rerun the command.

**Problem**

The command `alembic revision --autogenerate -m "some comment"` returns

```bash
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/configparser.py", line 1197, in set
    self._validate_value_types(option=option, value=value)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/configparser.py", line 1182, in _validate_value_types
    raise TypeError("option values must be strings")
TypeError: option values must be strings
```

**Solution**

Make sure the environment variable, `SQLALCHEMY_URI` is set to the proper database.

**Problem**

Executing `alembic upgrade head` results in an error. For example:

``` bash 
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sqlalchemy/util/compat.py", line 207, in raise_
    raise exception
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sqlalchemy/engine/base.py", line 1771, in _execute_context
    self.dialect.do_execute(
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/sqlalchemy/engine/default.py", line 717, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.InternalError: (psycopg2.errors.DependentObjectsStillExist) cannot drop view pg_stat_statements because extension pg_stat_statements requires it
HINT:  You can drop extension pg_stat_statements instead.
```

**Solution**

Troubleshoot as you would a Python program. In this is was a matter of removing a step in the migration script. That's why the migration output includes a line, `# ### commands auto generated by Alembic - please adjust! ###`
