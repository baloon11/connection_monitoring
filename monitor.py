# coding: utf-8
import socket
import os
import datetime


REMOTE_SERVER = "www.google.com"

curr_dir=os.path.dirname(__file__)
out_file=os.path.join(curr_dir,'out')
connection_status_file=os.path.join(curr_dir,'connection_status')

def working_with_file(file_name='',write='',key=''):
    curr_file=open(file_name,key)
    curr_file.write(write)
    curr_file.close()

try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    socket.create_connection((host, 80), 2)
    working_with_file(file_name=connection_status_file,
                      write='connection=True',
                      key='w')
except:
    connection_status=[connection_line.strip() for connection_line in open(connection_status_file,'r')][0]
    if connection_status=='connection=True':
        curr_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #getting 100 last lines from /var/log/syslog and filtered by NetworkManager and eth0
        raw_syslog=[raw_line for raw_line in open('/var/log/syslog','r')][-100:]
        syslog=[line for line in raw_syslog if 'NetworkManager' in line or 'eth0'in line]
        working_with_file(file_name=out_file,
                          write='script found disconnection in %s\n%s\n'%(curr_time,"-----"*10),
                          key='a')
        for out_line in syslog:
            working_with_file(file_name=out_file,
                              write=out_line+'\n',
                              key='a')
        working_with_file(file_name=out_file,
                          write="-----"*20+'\n',
                          key='a')
        working_with_file(file_name=connection_status_file,
                          write='connection=False',
                          key='w')
    print 'done!'