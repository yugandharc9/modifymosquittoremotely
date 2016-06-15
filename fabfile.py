"""
Author - Yugandhar K. Chaudhari
Different ways to handle the exception are shown in function 
You may embed in every function.
"""
from fabric.api import * 
import ConfigParser
import os,time,requests
os.environ['DJANGO_SETTINGS_MODULE']='mq.settings'
import django
django.setup()
import DJANGOAPP.views
import DJANGOAPP.models
from django.contrib.auth.models import User
#User are previosly authenticated
app=Celery('fabfile',backend="rpc://",broker='amqp://USER:PASSWORD@ADDRESS:PORT/NAME')
#Job Queue Configuration 



@app.task(trail=True)
def createinstance(username,instancename,session,port_ssl,port_websocket,port_normal,maxcon,pempath,serverip,count):
 #For creating instance on remote server count is 0 for 1st try 
 try:
  if count<3:
   local('mkdir -p /home/ubuntu/srvc/%s/%s'% (username,instancename))
   local('touch  /home/ubuntu/srvc/%s/%s/%s.log /home/ubuntu/srvc/%s/%s/%s.acl /home/ubuntu/srvc/%s/%s/%s.pwd '%(username,instancename,instancename,username,instancename,instancename,username,instancename,instancename))
    #making copy of directories on local webserver  
   local('tmux send-keys -t %s "mkdir -p /home/ubuntu/srvc/%s/%s" ENTER'%(session,username,instancename))
    #makin copy on remote webservers
   local('tmux send-keys -t %s "touch /home/ubuntu/srvc/%s/%s/%s.acl /home/ubuntu/srvc/%s/%s/%s.pwd" ENTER'%(session,username,instancename,instancename,username,instancename,instancename))
    #create acl file pwd file
   local('tmux send-keys -t %s "python /home/ubuntu/scripts/configwriter.py %s %s %s %s %s %s" ENTER'%(session,username,instancename,port_ssl,port_websocket,maxcon,port_normal))
    #See scrpits/configwriter.py  it writes configuration to mosquitto.conf
   local('tmux send-keys -t %s "mosquitto -d -c /home/ubuntu/srvc/%s/%s/%s.conf " ENTER'%(session,username,instancename,instancename)) 
    #start mosquitto in detchaed mode on server note - You may store instance credentials here or in views.py
   local('tmux send-keys -t %s "python /home/ubuntu/scripts/instancestarter.py %s %s" ENTER'%(session,username,instancename)) 
    #Take care of restarting the instance when remote server reboots.
  else:
   print '#createinstance failed#'
   pass
   #log
 except Exception as e:
  print e
  count+=1
  #increment count  
  createinstance(username,instancename,session,port_ssl,port_websocket,port_normal,maxcon,pempath,serverip,count)
  #retry again
 
@app.task(trail=True)
def getpid(username,instancename,pempath,serverip,count):
 #get process id of created mosquitto instance
 try:
  if count<=2:
   local('scp -i %s ubuntu@%s:/home/ubuntu/srvc/%s/%s/%s.pid /home/ubuntu/srvc/%s/%s'%(pempath,serverip,username,instancename,instancename,username,instancename))
   #copy pid to local server
   fs=open('/home/ubuntu/srvc/%s/%s/%s.pid'%(username,instancename,instancename),'r')
   fsl=fs.readline()
   retval=fsl.replace('\n','') 
   usrobj=User.objects.all().get(username=username)
   instobj=DATABASE.models.instance.objects.all().get(serviceuser=usrobj,instance_name=instancename)
   #service user is user authenticated throgh web app 'instance' stores fields like its name,portno etc., 'instance_name' is name of mosquitto instance stored locally
   obj=DATABASE.models.pidfile.objects.create(instance_name=instobj,pid=retval)
   #'pidfile' is table in local datatbase for storing proccess id.instance_name is name of mosquitto instance stored locally 
   obj.save()
   #store pid as to related instance
   fs.close()
  else:
   print '#getpid failed#'
   pass
   #log
 except:
  count+=1
  #increment retry count
  getpid(username,instancename,pempath,serverip,count)

@app.task(trail=True)
def replacepid(username,instancename,pempath,serverip,count):
 #replace pid in case of instnace restart or server migration
 try:
  if count<=2:
   local('scp -i %s ubuntu@%s:/home/ubuntu/srvc/%s/%s/%s.pid /home/ubuntu/srvc/%s/%s'%(pempath,serverip,username,instancename,instancename,username,instancename))
   #copy from remote server to local file
   fs=open('/home/ubuntu/srvc/%s/%s/%s.pid'%(username,instancename,instancename),'r')
   fsl=fs.readline()
   #read from file
   readval=fsl.replace('\n','') 
   usrobj=User.objects.all().get(username=username)
   instobj=DATABASE.models.instance.objects.all().get(serviceuser=usrobj,instance_name=instnancename)
   obx=DATABASE.models.pidfile.objects.get(instance_name=instobj)
   obx.pid=readval
   obx.save()
   #replace new pid
   fs.close()

  else:
   print '#replacepid failed#'
   pass
   #log
 except:
  count+=1
  replacepid(username,instancename,pempath,serverip,count)

@app.task(trail=True)
def writeusertoinstance(username,instancename,session,uname,pwd,pempath,serverip,count):
 #write new user to instance 
 try:
  if count<=2:
   local('tmux send-keys -t %s "mosquitto_passwd -b /home/ubuntu/srvc/%s/%s/%s.pwd \'%s\' \'%s\'" ENTER' % (session,username,instancename,instancename,uname,pwd))
   #need mosquitto_passwd on remote server note- install mosquitto from source 
  else:
   print '#write user is failed#'
   pass
 except :
  count+=1
  with settings(warn_only=True):
   #check if tmux session is running 
   #Can be used in each job 
   res=local('tmux has-session -t %s'%session)
   if(res!=0):
    local('tmux new -s %s -d '%session)
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip) )
   else:
    local('tmux kill-session -t %s'% session)
    local('tmux new -s %s -d'% session) 
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
   #One way to handle the tmux session exception
  writeusertoinstance(username,i,session,uname,pwd,pempath,serverip,count) 

@app.task(trail=True)
def removeuserfrominstance(username,instancename,session,uname,pempath,serverip,count):
 #removing user from instance
 try:
  if count<=2:
   local('tmux send-keys -t %s "mosquitto_passwd -D /home/ubuntu/srvc/%s/%s/%s.pwd %s" ENTER' % (session,username,instancename,instancename,uname)) 
  else:
   print '#removeuser failed#'
   pass
   
 except :
  count+=1
  with settings(warn_only=True):
   res=local('tmux has-session -t %s'%session)
   if(res!=0):
    local('tmux new -s %s -d '%session)
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip) )
   else:
    local('tmux kill-session -t %s'% session)
    local('tmux new -s %s -d'% session) 
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
  removeuserfrominstance(username,instancename,session,uname,pempath,serverip,count) 

@app.task(trail=True)
def writetoacl(username,instancename,pempath,serverip,count):
 try:
  if count<=2:
   local("scp -i %s /home/ubuntu/srvc/%s/%s/%s.acl ubuntu@%s:~/srvc/%s/%s"%(pempath,username,instancename,instancename,serverip,username,instancename))
   #note-before copying create the acl file on the local server
  else:
   print "#writetoacl failed#"
 except:
  count+=1
  writetoacl(username,instancename,pempath,serverip,count)

@app.task(trail=True)
def appendbridge(username,instancename,session,url,port,uname,pwd,topic,direction,qos,lp,rp,pid,pempath,serverip,count):
 #append bridge to running instance
 try:
  if count<=2:
   local('tmux send-keys -t %s "python /home/ubuntu/scripts/appendbr.py \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\' \'%s\'" ENTER'%(session,username,instancename,url,port,uname,pwd,topic,direction,qos,lp,rp))
   #See scripts/appendbr.py
   local('tmux send-keys -t %s "kill -KILL %s" ENTER'%(session,pid))
   local('tmux send-keys -t %s "mosquitto -c /home/ubuntu/srvc/%s/%s/%s.conf -d" ENTER'%(session,username,instancename,instancename))
   replacepid(username,instancename,pempath,serverip,count)
  else:
   print '#appendbridge failed#' 
   pass
 except :
  count=+1
  with settings(warn_only=True):
   res=local('tmux has-session -t %s'%session)
   if(res!=0):
    local('tmux new -s %s -d '%session)
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip) )
   else:
    local('tmux kill-session -t %s'% session)
    local('tmux new -s %s -d'% session) 
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
  appendbridge(username,instancename,session,url,port,uname,pwd,topic,direction,qos,lp,rp,pid,pempath,serverip,count)

@app.task(trail=True)
def deletebridge(username,instancename,session,pid,pempath,serverip,count):
 #delete runnging bridge and restart the instance
 try:
  if count<=2:
   local('tmux send-keys -t %s "python /home/ubuntu/scripts/deletebr.py \'%s\' \'%s\'" ENTER'%(session,username,instancename))
   # See scripts/deletebr.py
   local('tmux send-keys -t %s "kill -KILL %s" ENTER'%(session,pid))
   #Send reload signal
   local('tmux send-keys -t %s "mosquitto -c /home/ubuntu/srvc/%s/%s/%s.conf -d" ENTER'%(session,username,instancename,instancename))
   replacepid(username,instancename,pempath,serverip,count)
   #get pid of new instance
  else:
   print "#deletebridge failed#"
   pass
 except :
  count=+1
  with settings(warn_only=True):
   res=local('tmux has-session -t %s'%session)
   if res!=0:
    local('tmux new -s %s -d '%session)
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip) )
   else:
    local('tmux kill-session -t %s'% session)
    local('tmux new -s %s -d'% session) 
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
  deletebridge(username,i,session,pid,pempath,serverip,count)

@app.task(trail=True)
def reloadconfig(session,pid,pempath,serverip,count):
 #send reload signal to running instance 
 try:
  if count<=2:
   local('tmux send-keys -t %s "kill -HUP %s" ENTER '%(session,pid))
   #send reload
  else:
   print '#reloadconfig failed#'
   pass
 except:
  count=+1
  with settings(warn_only=True):
   res=local('tmux has-session -t %s'%session)
   if res!=0:
    local('tmux new -s %s -d '%session)
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip) )
   else:
    local('tmux kill-session -t %s'% session)
    local('tmux new -s %s -d'% session) 
    local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
   reloadconfig(session,pid,pempath,serverip,count)

def getlog(username,instancename,pemfile,serverip,count):
 #get log on local server
 try:
  if count<=2:
   local('scp -i %s ubuntu@%s:/home/ubuntu/srvc/%s/%s/%s.log /home/ubuntu/srvc/%s/%s'%(pemfile,serverip,username,instancename,instancename,username,instancename))
  else:
   print '#getlog unjob failed#'
   pass
 except:
  count+=1
  getlog(username,instancename,pemfile,serverip,count)
  

@app.task(trail=True)
def createsession(session,serverip,pempath,count):
 #create a tmux session
 try:
  if count<=2:
   local('tmux new -s %s -d'% session)
   local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
  else:
   print "#create session failed#"
   pass
 except:
  with settings(warn_only=True):
   ret1=local('tmux has-session -t %s'%(session))
  print str(ret1.return_code)+ 'this is ret'
  if ret1.return_code==int(0):
   local('tmux kill-session -t %s'%(session))
   local('tmux new -s %s -d'% session)
   local('tmux send-keys -t %s "ssh -i %s ubuntu@%s" ENTER'%(session,pempath,serverip))
  else:
   print 'runnig else'
   count+=1 
   createsession(session,serverip,pempath,count)
   
@app.task(trail=True)
def deletesession(session_name,count):
#Deleting a tmux session locally
 try:
  if count<=2:
   local('tmux kill-session -t %s'%session_name)
  else:
   print '#delete session failed#'
 except:
  count+=1
  deletesession(session_name,count)  


