Description
================

Log working hours (ie screen is locked/unlocked) and fill a total working time to the web form using selenium.

How it works?
================

Whenever screen is locked/unlocked [ssTriger](http://blog.troyastle.com/2011/06/run-scripts-when-gnome-screensaver.html) script is triggered.
It happens only for screen lock (for example shortcut Ctrl+Alt+L) but not in case of login, logout, restart... 
ssTriger writes the current time in mysql database. 
`log_working_time.py` at the end of a day (crontab) is used to summarize all working time and to fill web form.
When user come back from the break, he/she should run `log_working_time.py break` to mark pause as break in work.

Install
================
You can download with

    git clone 

Here are instructions for installing on Ubuntu 12.10

    sudo apt-get install default-jre python-mysqldb python-pip mysql-server
    # set the password="password"
    
Set up database and table

    mysql -uroot -ppassword -e "CREATE DATABASE working_time"
    mysql -uroot -ppassword working_time -e "CREATE TABLE working_time ( start time NOT NULL, end time NOT NULL, itWasABrake tinyint(1) NOT NULL DEFAULT 0, ID int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID));"
    
Set up and start Selenium

    sudo pip install -U selenium # --proxy="user:password@server:port"
    wget http://selenium.googlecode.com/files/selenium-server-standalone-2.28.0.jar 

Create two startup scripts

    gnome-desktop-item-edit --create-new ~/.config/autostart/
    
for first set Name: **java** and second Name: **ssTriger**

Create (shortcuts)[http://askubuntu.com/questions/64222/how-can-i-create-launchers-on-my-desktop] 

    gnome-desktop-item-edit --create-new ~/Desktop
    
Set up unlocking password: `All Settings->Brightness and Lock->"Require my password when waking from suspend"`. 

Settings
================
There are three places in `log_working_time.py` that need to be adjusted
* password for mysql
* target field and password for webform
* whether total working time should be reduced with minimum lunch break (30 min)

