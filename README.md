# people

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9d16e13e80f3426caf399aa8bad8a846)](https://www.codacy.com/manual/erikdeirdre/people?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=erikdeirdre/people&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/9d16e13e80f3426caf399aa8bad8a846)](https://www.codacy.com/manual/erikdeirdre/people?utm_source=github.com&utm_medium=referral&utm_content=erikdeirdre/people&utm_campaign=Badge_Coverage)

Module to manage people in a system. 

It uses a base person class along with specialized people.

## Usage 

The following assumes you're using `sqlite` for your database.

### Running Locally

- create a virtualenv
- run ```pip install -r requirements.txt```
- if using Windows, run ```set FLASK_APP=people.py```, else ```export FLASK_APP=people.py```
- run ```flask run```

You should be able to access the `graphql` console via `http://127.0.0.1:5000`

### Running as a Docker container

If you plan on persisting data between runs then you need to create a Docker volume, and mount it within the container.

- create a Docker volume, `docker volume create {volume name}`. For example, `docker volume create sqlite_data`.
- build the container, `docker build -t {tag name} .`. For example: `docker build -t people:latest .`
- run the container, `docker run -d -v {source volume}:/{target name}  -e "CONFIG_SETTINGS=config.ProductionConfig" -e "DATABASE_DIR={database location}" {tag name}`. For example: `docker run -d -v sqlite_data:/data -e  -e "CONFIG_SETTINGS=config.ProductionConfig" "DATABASE_DIR=data" person`.
