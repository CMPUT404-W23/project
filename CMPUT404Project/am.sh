#! usr/bin/bash
python3 manage.py makemigrations socialDist
python3 manage.py migrate
python3 manage.py createsuperuser