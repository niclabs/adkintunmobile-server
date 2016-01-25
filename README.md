Adkintun Mobile Server
======================

Adkintun Mobile server.

Current requirements
--------------------

* Flask
* Flask-Script
* VirtualEnv
* Postgresql
* SQLAlchemy.
* Flask-SQLAlchemy.
* Flask-Migrate.
* Flask-RESTful.
* Flask-Admin.

To run
------
Clone project:

```
$ git clone git@git.niclabs.cl:adkmobile/server.git
```

Install pip, VirtualEnv, postgres and others:

```
$ sudo apt-get install python3-dev
$ sudo apt-get install python-pip
$ pip install virtualenv
$ sudo apt-get install postgresql
```

Create and activate virtual enviroment:

```
$ virtualenv -p [python 3 interpreter] venv  
$ . venv/bin/activate
```

Install requirements (in the virtual enviroment):

```
$ pip install -r requirements.txt
```

Database config
---------------
In postgres:

```
$ sudo -u postgres psql
# CREATE ROLE batman WITH PASSWORD 'cocacolaamediollenar';
# ALTER ROLE batman WITH LOGIN SUPERUSER;
# CREATE DATABASE adkintun WITH OWNER batman;
```

If you wish to run the tests:

```
# CREATE DATABASE test_adkintun WITH OWNER batman;
```

Then initiate and migrate the database:

```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

Run server
----------
To run the server:

```
$ python manage.py runserver
```

To run the tests:

```
$ python manage.py test
```
