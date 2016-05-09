#!/bin/bash

#it needs to change the actual directory to the DB directory
cd /home/phelipe/project

#runs the script to move the sensor and get the temperature
python controller.py

#creates a JSON file with the information on the DB
python convertdb.py

#uploads the created file to the address www2.newpaltz.edu/~fernandp5/buoy/buoy.txt
scp -i ~/.ssh/id_rsa /var/www/html/buoy/buoy.txt fernandp5@www2.newpaltz.edu:/home/fernandp5/public_html/buoy/buoy.txt
