# ModifyMosquittoRemotely
ModifyMosquittoRemotely is how to modify mosquitto configurations on remote servers distributedly through python web appliation.

Prerequisites:<br>
Python 2.7<br>
Django 1.9<br>
Fabric 2.5<br>
Celery 3.1<br>
Mosquitto 1.4.7<br>

Steps:
1.Setup pyton environment<br> 
  `pip install virtualenv`
2.Create virtualenv
 `virtualenv NAME`
 `cd NAME`
  `source bin/activate`
2.Install Django,Celery,Fabric,Tmux
`pip install django Celery fabric`
`apt-get install tmux`
3.Download mosquitto <a href="http://mosquitto.org/files/source/mosquitto-1.4.9.tar.gz">source</a> on remote webserver<br>
 `tar -xvf mosquitto-1.4.9.tar.gz`
 `cd mosquitto-1.4.9`
 `make`
 `make install`
4.Create Django Project<br>
  `django-admin.py startproject PROJECTNAME`
5.Configure database<br>
5.Create Models<br>
6.Setup Celery <a href="http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html">See<br>
7.Create views.
8.Start App.
