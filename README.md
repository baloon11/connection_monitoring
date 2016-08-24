#### This script solves the task of checking network connection.
If connection is lost -- it creates `out` file and writes info about lost connection in it.  
This info it gets from /var/log/syslog   
It gets 100 latest lines from this file and  
filtered it by words 'NetworkManager' and 'eth0'  
In this info easy to find the reason why connection is lost.  


##### Before Usage:
1. Create virtualenv
2. Install:  `pip install peewee`

##### Usage:
This script can be run manually:  
        
        python monitor.py  

or using cron job:  
  In crontab add this line:
  
     * * * * * /path/to/virtualenv/bin/python path_to_directoty/monitor.py

and the script will run every 1 minute.  
(Do not forget change the path)  

This script stores info about status of connection  
(the connection is exist or the connection is lost)  
in DB (sqlite - the single file) `connection_status.db`

When you run this script the first time it creates DB file, creates table `Status` in it.  
And in `Status` table in creates the single row with the field `connection` (default=True)  
It means that now connection is exists.  
Then the script will be  store the current connection status in this DB.  
It is necessary,for example, in the situation
if the connection is lost -- then the information will not be duplicated in the `out` file few times.  
