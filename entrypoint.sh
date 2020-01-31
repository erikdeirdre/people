#!/usr/bin/env sh

echo "Run db upgrade and initialize db"
 flask db upgrade && flask initdb && flask run --host=0.0.0.0
