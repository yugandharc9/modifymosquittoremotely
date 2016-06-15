import sys
import re
#1:username
#2.instacename

def brwriter(argv):
 f=open('/home/ubuntu/srvc/%s/%s/%s.conf'%(sys.argv[1],sys.argv[2],sys.argv[2]),'r')
 a=f.read()
 f.close()
 ff=re.search(r'connection\s(.*\n)*',a)
 wr=a.replace(ff.group(),'')
 f=open('/home/ubuntu/srvc/%s/%s/%s.conf'%(sys.argv[1],sys.argv[2],sys.argv[2]),'w')
 f.write(wr)
 f.close()

if __name__=='__main__':
 brwriter(sys.argv)
