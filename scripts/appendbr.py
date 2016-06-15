import sys

#1:username
#2.instacename
#3.url
#4.port
#5.username 
#6.password
#7.topic name
#8.direction
#9.QoS
#10.local prefix 
#11.remote prefix

def configwriter(argv):
 f=open('/home/ubuntu/srvc/%s/%s/%s.conf'%(sys.argv[1],sys.argv[2],sys.argv[2]),'a')
 f.write("connection bridge-%s\n"%(sys.argv[2]))
 f.write("bridge_cafile /home/ubuntu/certs/ca.crt\n")
 f.write("bridge_certfile /home/ubuntu/certs/__primemq_com_ee.crt\n")
 f.write("bridge_keyfile /home/ubuntu/certs/primemq.com.key\n")
 f.write("bridge_insecure false\n")
 f.write("bridge_tls_version tlsv1.2\n")
 f.write("address %s:%s\n"%(sys.argv[3],sys.argv[4]))
 f.write("cleansession false\n")
 f.write("clientid bridge-from-%s\n"%(sys.argv[2]))
 f.write("start_type automatic\n")
 f.write("username %s\n"%(sys.argv[5]))
 f.write("password %s\n"%(sys.argv[6]))
 f.write("try_private true\n")
 f.write("topic %s %s %s %s %s\n"%(sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10],sys.argv[11]))
 f.close()
"""
def abc(argv):
 print sys.argv[1]
 print sys.argv[2]
"""
if __name__=='__main__':
 configwriter(sys.argv)
