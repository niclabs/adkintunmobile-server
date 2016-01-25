Adkintun Mobile Server
======================

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

Install pip, VirtualEnv, postgres, mongo and others:

```
$ sudo apt-get install python3-dev
$ sudo apt-get install python-pip
$ pip install virtualenv
$ sudo apt-get install postgresql
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
$ sudo apt-get update  
$ sudo apt-get install -y mongodb-org
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

Run server
=======
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

Finally run the server:

```
$ python manage.py runserver
```
