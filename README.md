Description
================

Log working hours (ie screen is locked/unlocked) and fill a total working time to the web form using selenium.

INSTALL
================
Here are instructions for installing on Ubuntu 12.10

    sudo apt-get install default-jre python-mysqldb python-pip mysql-server
    # set the password="password"
    
Set up database and table

    mysql -uroot -ppassword -e "CREATE DATABASE working_time"
    mysql -uroot -ppassword working_time -e "CREATE TABLE working_time ( start time NOT NULL, end time NOT NULL, itWasABrake tinyint(1) NOT NULL DEFAULT 0, ID int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID));"
    
Set up and start Selenium

    sudo pip install -U selenium # --proxy="user:password@server:port"
    wget http://selenium.googlecode.com/files/selenium-server-standalone-2.28.0.jar 
    java -jar selenium-server-standalone.jar

Create shortcuts http://askubuntu.com/questions/64222/how-can-i-create-launchers-on-my-desktop

    gnome-desktop-item-edit --create-new ~/Desktop
    



