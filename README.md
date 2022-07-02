# Objective
Following 7-hours-long Django tutorial :)

YouTube tag: `PtQiiknWUcI`

# Setting up

Set up a project and run its server:

```bash
mkdir django-7-hours
cd django-7-hours/
pip3.9 install virtualenv
virtualenv env
source env/bin/activate
pip install django
django-admin
django-admin startproject studybud
python manage.py runserver
```
Re-activate and run server again:

```bash
deactivate
cd /home/m3/repos/django-7-hours
source env/bin/activate
cd studybud/
python manage.py runserver
```
Don't move the `env` directory on Linux. The `python` commands would throw errors.

Create a new component or app for the project:

```bash
python manage.py startapp base
```
# Run SQL commands

Prepare database:

```bash
python manage.py migrate
```
