import sys

def instancewriter(argv):
 f=open('/home/ubuntu/runonreboot.sh','a')
 f.write('mosquitto -c /home/ubuntu/srvc/%s/%s/%s.conf -d \n'%(sys.argv[1],sys.argv[2],sys.argv[2]))
 f.close()

if __name__=='__main__':
 instancewriter(sys.argv)
