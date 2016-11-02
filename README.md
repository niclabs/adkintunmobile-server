Adkintun Mobile Server [![Build Status](https://travis-ci.org/niclabs/AdkintunMobile-Server.svg?branch=master)](https://travis-ci.org/niclabs/AdkintunMobile-Server)
======================

Adkintun Mobile server.

What is new?
-------
* 1.1.2 (30.9.2016)
    * Fixed antennas geolocalization bugs
    * Changed apscheduler for uwsgi mules
    * Changed trigger pages for commands
    * minor fixes

* 1.1.1 (7.9.2016)
    * Created method to geolocalized antennas, and update them to the database
    * Added job to the schedduler for antennas geolocalization
    * Refactor code

* 1.1 beta (2.9.2016)
    * Bug fixes and refactor code.
    * New api methods for antennas
    * New api method for terms and condition
    * Added antenna signal mean reports generation and api
    * Added antenna network report generation and api
    * Added application rankings generation and api
    * New way to add events and their context

* 1.0.2 beta (02.8.2016)
    * Bug fixes and refactor code.
    * Limit size log file.

* 1.0.1 beta (28.7.2016)
    * Bug fixes.
    * Add carriers dynamically, with tests.
    
* 1.0 beta (20.7.2016)
    * First release AdkintunMobile Server.


Current requirements
--------------------

* Flask
* Flask-Script
* sqlalchemy
* flask-sqlalchemy
* flask-migrate
* flask-restful
* psycopg2
* flask_admin
* flask-login
* flask-httpauth
* requests
* uwsgi

For more info visit the project [Wiki](https://github.com/niclabs/AdkintunMobile-Server/wiki)
