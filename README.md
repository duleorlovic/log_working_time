Description
================

Log working hours (ie when screen is unlocked) and fill a total working time to the web form using [selenium](http://seleniumhq.org/).

How it works?
================

Whenever screen is locked or unlocked [ssTriger.py](http://blog.troyastle.com/2011/06/run-scripts-when-gnome-screensaver.html) script is triggered.
It happens only for screen lock (for example keyboard shortcut: Ctrl+Alt+L) but not in case of login, logout, restart. 
`ssTriger.py` writes the current time in mysql database. At the end of a day (using crontab) `log_working_time.py` is used to summarize all working time and to fill web form.
When users come back from the break, they should run `log_working_time.py break` to mark previous pause as break in work time.

Install
================
You can download with

    git clone https://github.com/duleorlovic/log_working_time.git

On Ubuntu 12.10 you should have these packages (for mysql password use *password* or whatever you want)

    sudo apt-get install default-jre python-mysqldb python-pip mysql-server
    # set the password="password"
    
Set up database and table

    mysql -uroot -ppassword -e "CREATE DATABASE working_time"
    mysql -uroot -ppassword working_time -e "CREATE TABLE working_time ( date date NOT NULL, start time NOT NULL, end time NOT NULL, itWasABrake tinyint(1) NOT NULL DEFAULT 0, ID int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID));"
    
Download [Selenium](http://pypi.python.org/pypi/selenium)

    sudo pip install -U selenium # --proxy="user:password@server:port"
    wget http://selenium.googlecode.com/files/selenium-server-standalone-2.28.0.jar 

Create two [startup scripts on Ubuntu](http://askubuntu.com/questions/64222/how-can-i-create-launchers-on-my-desktop),
one for selenium and one for ssTriger

    sudo apt-get install --no-install-recommends gnome-panel
    mkdir ~/.config/autostart
    gnome-desktop-item-edit --create-new ~/.config/autostart/
    # Name: **selenium** and Command: `java -jar /path_to_the_file/selenium-server-standalone-2.28.0.jar`
    gnome-desktop-item-edit --create-new ~/.config/autostart/
    # Name: **ssTriger** and Command: `/path_to_the_file/ssTriger.py`

Create Desktop shortcut to use when we want to mark previous pause as break in worktime:

    gnome-desktop-item-edit --create-new ~/Desktop
    # Name: **break**, Command: `/path_to_the_file/log_working_time.py break`

You can set up unlocking password: `All Settings->Brightness and Lock->"Require my password when waking from suspend"`. 

There are three places in `log_working_time.py` that need to be adjusted
* password for mysql
[log_working_time.py#L21](https://github.com/duleorlovic/log_working_time/blob/master/log_working_time.py#L21) and
[ssTriger.py#L28](https://github.com/duleorlovic/log_working_time/blob/master/ssTriger.py#L28)
* user and password for web form [log_working_time.py#L85](https://github.com/duleorlovic/log_working_time/blob/master/log_working_time.py#L85)
* target option value [log_working_time.py#L90](https://github.com/duleorlovic/log_working_time/blob/master/log_working_time.py#L90)
* whether total working time should be reduced with minimum lunch break (30 min) [log_working_time.py#L73](https://github.com/duleorlovic/log_working_time/blob/master/log_working_time.py#L73)

