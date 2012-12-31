#!/usr/bin/env python

# this script should be run as a startup script
# gnome-desktop-item-edit --create-new ~/.config/autostart/
# Name: ssTriger, Command: /path_to_the_file/ssTriger.py
from gobject import MainLoop
from dbus import SessionBus
from dbus.mainloop.glib import DBusGMainLoop
import datetime
import MySQLdb as mdb
import logging
import os

logging.basicConfig(filename='/tmp/working_time.log',level="INFO",
        format='%(levelname)s %(asctime)s %(message)s')
logging.info("starting...")

class SSTrigger:
    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        self.mem='ActiveChanged'
        self.dest='org.gnome.ScreenSaver'
        self.bus=SessionBus()
        self.loop=MainLoop()
        self.bus.add_signal_receiver(self.catch,self.mem,self.dest)

    def catch(self,ssOn):
        conn = mdb.connect('localhost', 'root','mysql_password', 'working_time');
        cursor = conn.cursor()
        now = datetime.datetime.now()

        if ssOn == 1: #Screensaver turned on
            sql = "UPDATE working_time SET end='%s' WHERE date='%s' AND end='0:0'"\
                    %(now.strftime("%H:%M"),now.strftime("%Y-%m-%d"))
            #logging.info(" sql=%s "%sql)
            logging.info("end=%s" % str(now.strftime("%H:%M")))
            res = cursor.execute(sql)
            if conn.affected_rows() != 1:
                cursor.execute("SELECT * from working_time")
                if cursor.rowcount != 1: # ignore error if it is a very first record in database
                    logging.error("ERROR!!! It should be only one (the last) record with end=0:0")

        else: #Screensaver turned off
            sql = "INSERT INTO working_time (date, start, end) VALUES('%s','%s','%s')"\
                    %(now.strftime("%Y-%m-%d"),now.strftime("%H:%M"),"0:0")
            #logging.info(" sql=%s "%sql)
            res=cursor.execute(sql)
            logging.info("start=%s "%now.strftime("%H:%M"))
            os.system("xmessage -nearmouse 'If you were out then start: log_working_time.py break'")

        conn.commit()	
        cursor.close()
        conn.close()
        
SSTrigger().loop.run()


