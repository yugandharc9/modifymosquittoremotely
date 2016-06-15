# ModifyMosquittoRemotely
ModifyMosquittoRemotely is how to modify mosquitto configurations on remote servers distributedly through python web appliation.

Prerequisites:<br>
Python 2.7<br>
Django 1.9<br>
Fabric 2.5<br>
Celery 3.1<br>
Mosquitto 1.4.7<br>

Steps:
<h2>On Local Webserver</h2>
1.Setup python environment<br> 
  `pip install virtualenv`<br>
  
2.Create virtualenv<br>
 `virtualenv NAME`<br>
 `cd NAME`<br>
  `source bin/activate`<br>

3.Install Django,Celery,Fabric,Tmux<br>
`pip install django Celery fabric`<br>
`apt-get install tmux`<br>

4.Create Django Project<br>
  `django-admin.py startproject PROJECTNAME`<br>

5.Start Django app<br>
`python manage.py startapp APPNAME`<br>
<br>
6.Configure database<br>
<br>
7.Create Models<br>
<br>
8.Setup Celery <a href="http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html">See</a><br>
<br>
9.Create views.<br>
<br>
10.Start App.<br>

<h2>On remote server where mosquitto is hosted.</h2>
<br>
1.Download mosquitto <a href="http://mosquitto.org/files/source/mosquitto-1.4.9.tar.gz">source</a> on remote webserver<br>
 `tar -xvf mosquitto-1.4.9.tar.gz`<br>
 `cd mosquitto-1.4.9`<br>
 `make`<br>
 `make install`<br>
 <br>
 2.Install tmux <br>
`apt-get install tmux`<br>
 <br>
 3.Place scripts in home directory<br>
