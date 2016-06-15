#!/usr/bin/python

#sys.argv[1]=uname
#sys.argv[2]=instancename
#sys.argv[3]=port_ssl
#sys.argv[4]=port_websocket
#sys.argv[5]=maxcon
#sys.argv[6]=port_normal

import sys

def configwriter(argv):
 f=open('/home/ubuntu/srvc/%s/%s/%s.conf'%(sys.argv[1],sys.argv[2],sys.argv[2]),'w')
 f.write('autosave_interval 2000\n')
 f.write('allow_anonymous false\n')
 f.write('persistence true\n')
 f.write('persistence_file %s.db\n'%sys.argv[2])
 f.write('persistence_location /home/ubuntu/srvc/%s/%s/\n'%(sys.argv[1],sys.argv[2]))
 f.write('connection_messages true\n')
 f.write('retained_persistence true\n')
 f.write('allow_duplicate_messages false\n')
 f.write('log_dest file /home/ubuntu/srvc/%s/%s/%s.log\n'%(sys.argv[1],sys.argv[2],sys.argv[2]))
 f.write('log_type warning\n')
 f.write('log_type notice\n')
 f.write('log_type information\n')
 f.write('log_type all\n')
 f.write('log_type debug\n')
 f.write('log_type websockets\n')
 f.write('log_timestamp true\n')
 f.write('max_connections %s\n'% sys.argv[5])
 f.write('acl_file /home/ubuntu/srvc/%s/%s/%s.acl\n'% (sys.argv[1],sys.argv[2],sys.argv[2]))
 f.write('password_file /home/ubuntu/srvc/%s/%s/%s.pwd\n'% (sys.argv[1],sys.argv[2],sys.argv[2]))
 f.write('pid_file /home/ubuntu/srvc/%s/%s/%s.pid\n'% (sys.argv[1],sys.argv[2],sys.argv[2]))
 f.write('user mosquitto\n') 
 f.write('port %s\n'% sys.argv[6])
 f.write('listener %s\n'% sys.argv[3])
 f.write('protocol mqtt\n')
 f.write('require_certificate false\n')
 f.write('cafile /home/ubuntu/certs/ca.crt\n')
 f.write('certfile /home/ubuntu/certs/__primemq_com_ee.crt\n')
 f.write('keyfile /home/ubuntu/certs/primemq.com.key\n')
 f.write('listener %s\n'% sys.argv[4])
 f.write('protocol websockets\n')
 f.write('cafile /home/ubuntu/certs/ca.crt\n')
 f.write('certfile /home/ubuntu/certs/__primemq_com_ee.crt\n')
 f.write('keyfile /home/ubuntu/certs/primemq.com.key\n')
 f.close()
"""
def abc(argv):
 print sys.argv[1]
 print sys.argv[2]
"""
if __name__=='__main__':
 configwriter(sys.argv)
