# coding: utf-8
import socket
import os
import time
import datetime
from peewee import *
import sqlite3 as lite


def create_db():
    con = lite.connect('connection_status.db')
    con.close()


db = SqliteDatabase('connection_status.db')
class Status(Model):
    connection = BooleanField(default=True)

    class Meta:
        database = db


def create_tables():
    db.connect()
    db.create_tables([Status], safe=True)
    db.close()

def create_first_row():
    db.connect()
    Status.create()#first row
    db.close()

def connection_status(connection=True):
    db.connect()
    status = Status.get(Status.id == 1)
    status.connection=connection
    status.save()
    db.close()

REMOTE_SERVER = "www.google.com"

curr_dir=os.path.dirname(__file__)
out_file=os.path.join(curr_dir,'out')
connection_status_file=os.path.join(curr_dir,'connection_status')

def working_with_file(file_name='',write='',key=''):
    curr_file=open(file_name,key)
    curr_file.write(write)
    curr_file.close()

def main():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, 80), 2)
        connection_status(connection=True)
    except Exception, e:
        print e
        #connection==True in DB 
        #but now the server lost network connection
        if Status.get(Status.id == 1).connection:
            time.sleep(60)
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
            connection_status(connection=False)
    print 'done!'

if __name__=='__main__':
    if not os.path.exists('connection_status.db'):
        create_db()
        create_tables()
        create_first_row()
        main()
    else:
        main()