# import the Flask class from the flask modules
from flask import Flask, render_template, request, send_from_directory
import json
import sqlite3
import datetime, time
 

db = "./static/myTempTime.db"
tempData = "./static/tempData.txt"



# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return app.send_static_file('tempData.txt') 

@app.route('/welcome')
def welcome():
    return render_template('about.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

#JSON filewriter BROKEN
#def fileWrite():
#	with open(db, 'w') as f: f.write(getTemps(json_str = True)


#Chart data input	
def getTemps(json_str = False):
	conn = sqlite3.connect(DB)
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	rows = db.execute('''SELECT * from data''').fetchall()
	conn.commit()
	conn.close()
	if json_str:
		return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON
	return rows
	

