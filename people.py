from app import (app, db)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database with proper tables"""
    db.create_all()
    db.session.commit()
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print("Initialized the database")


if __name__ == '__main__':
    app.run()
