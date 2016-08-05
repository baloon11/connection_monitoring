import socket
import os
import datetime
import time

REMOTE_SERVER = "www.google.com"

curr_dir=os.path.dirname(__file__)
out_file=os.path.join(curr_dir,'out')
connection_status_file=os.path.join(curr_dir,'connection_status')
try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    status_file=open(connection_status_file,'w')
    status_file.write('connection=True')
    status_file.close()

except:
    connection_status=[connection_line.strip() for connection_line in open(connection_status_file,'r')][0]
    if connection_status=='connection=True':
        curr_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(60)
        #getting 100 last lines (filtered by NetworkManager)
        raw_syslog=[raw_line for raw_line in open('/var/log/syslog','r')][-100:]
        syslog=[line for line in raw_syslog if 'NetworkManager' in line or 'eth0'in line]
        out=open(out_file,'a')
        out.write('script found disconnection in '+curr_time+'\n'+"-----"*10+'\n')
        out.close()

        for out_line in syslog:
            out=open(out_file,'a')
            out.write(out_line+'\n')
            out.close()

        out=open(out_file,'a')
        out.write("-----"*20+'\n')
        out.close()
        status_file=open(connection_status_file,'w')
        status_file.write('connection=False')
        status_file.close()
    print 'done!'