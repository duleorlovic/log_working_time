#!/usr/bin/env python
from selenium import selenium
import unittest, time, re
import MySQLdb as mdb
import os
import logging
import datetime
import sys

logging.basicConfig(filename='/tmp/working_time.log',level="INFO",format='%(levelname)s %(asctime)s %(message)s')

# this script should run from crontab
# crontab: 0 22 * * 1-5 /path_to_the/log_working_time.py > /dev/null
# selenuim should be started, preferably as a startup script
# gnome-desktop-item-edit --create-new ~/.config/autostart/
# Name: Selenium, Command: java -jar /path_to_the/selenium-server-standalone-2.20.0.jar

class LogWorkingTime(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.conn = mdb.connect('localhost', 'root','mysql_password', 'working_time')
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        self.cursor.close()
        self.conn.close()
    
    def test_ignore_last_record(self):
        self.test_add(True)

    def test_add(self,ignore_last_record=False):
        now = datetime.datetime.now()
        sql = "SELECT start, end, itWasABrake FROM working_time \
                WHERE date='%s' ORDER BY ID "%now.strftime("%Y-%m-%d")
        #logging.info(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) < 2:
           self.assertTrue(False,'Less than two records in database. Please lock your screen CTRL+ALT+L')

        if results[-1][1] == datetime.timedelta() and not ignore_last_record:
            self.assertTrue(False,'"end" field of the last record in working_time table is 0:0\n\
            log_working_time.py should be started when screen is locked!\n\
            if you only want to test then start with an argument ignore_last_record\n\
            "log_working_time.py ignore_last_record"\n\
            afterwards you should clear the inserted value from the web and log file')

        day_start = results[0][0] # start of the first working time period
        if ignore_last_record:
            # do not take end time of the last record which is probably '0:0', use before the last
            day_end = results[-2][1]
        else:
            day_end = results[-1][1] # end time of the last working time period

        logging.info("total time without breaks = %s" % (day_end-day_start))
        
        previous_end = results[0][1]
        total_break = datetime.timedelta(0)
        
        for current_start, current_end, itWasABrake in results[1:]:
           if itWasABrake :
           	total_break += current_start - previous_end
           	logging.info("break at %s in duration %s" % (current_start,current_start-previous_end))
           else:
              if current_start-previous_end > datetime.timedelta(minutes=10):  
                  # alert if long pause is not market as break
                  logging.debug("alert! Pause at %s in duration %s but itWasABrake==False"% (previous_end, current_start-previous_end))
           previous_end = current_end

        if total_break < datetime.timedelta(minutes=30) :
           pass
           #logging.info("total break %s is less then minimum value 30min" %total_break)
           #total_break = datetime.timedelta(minutes=30)
        
        logging.info("total_break = %s" % total_break)
        
        working_hours = day_end - day_start - total_break
	self.selenium_write(working_hours)

    def selenium_write(self, working_hours):        
        sel = selenium("localhost", 4444, "*chrome", "http://wtis/")
        sel.start()
        sel.open("/")
        sel.type("username", "web_user")
        sel.type("password", "web_password")
        sel.click("login")
        sel.wait_for_page_to_load("30000")
        time.sleep(3)
        sel.select("class=gwt-ListBox","text of the option value")
        time.sleep(1)
        sel.type("css=input.gwt-TextBox", "%.2f"%(working_hours.seconds/3600.))
        sel.click("css=button.gwt-Button")
        sel.stop()
        logging.info("-----> writed %.2f (%s)" % (working_hours.seconds/3600.,working_hours))

    def test_summarize(self):
        now = datetime.datetime.now()
        self.cursor.execute("SELECT start, end, itWasABrake FROM working_time \
                WHERE date='"+now.strftime("%Y-%m-%d")+"' ORDER BY ID")
        results = self.cursor.fetchall()
        if len(results) < 2:
           os.system("xmessage -nearmouse 'There should be at least two records. Please lock your screen.'")
           sys.exit()
        today_start = results[0][0]
        previous_end = results[0][1]
        print today_start, "-",previous_end
        pause = datetime.timedelta(0)
        for current_start,current_end,itWasABrake in results[1:]:
            print current_start, "-",current_end, 
            if itWasABrake :
                pause += current_start-previous_end
                print "break %s" % (current_start-previous_end)
            else:
                print
            previous_end = current_end

        working_time = now - today_start - pause

        print "today start ", today_start
        print "total break ", pause
        print "current time ", now.strftime("%H:%M")
        print "total time so far ", working_time.strftime("%H:%M")
        os.system("xmessage -nearmouse 'total working time so far %s '" % working_time)

    def test_break(self):
        self.cursor.execute("SELECT start, end FROM working_time \
		WHERE end>=CURDATE() ORDER BY ID DESC LIMIT 2")
        results = self.cursor.fetchall()
        if len(results) != 2:
            logging.debug("it_was_a_brake.py -> there should at least two records")
            os.system("xmessage -nearmouse 'Please lock your screen and then make a break'")
        else:
            self.cursor.execute("UPDATE working_time SET itWasABrake=TRUE ORDER BY ID DESC LIMIT 1")
            logging.info("itWasABrake=TRUE")
            os.system("xmessage -nearmouse 'Break duration %smin'" % (results[0][0] - results[1][1]))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    if len(sys.argv)==1:
        suite.addTest(LogWorkingTime('test_add'))
    else:
        if sys.argv[1]=='summarize':
            suite.addTest(LogWorkingTime('test_summarize'))
        elif sys.argv[1]=='break':
            suite.addTest(LogWorkingTime('test_break'))
        elif sys.argv[1]=='ignore_last_record':
            suite.addTest(LogWorkingTime('test_ignore_last_record'))
        else:
            print "log_working_time.py {summarize|break|ignore_last_record}"
            sys.exit()
    unittest.TextTestRunner().run(suite)

