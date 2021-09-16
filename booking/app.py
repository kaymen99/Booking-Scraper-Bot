
from flask import Flask, render_template, request
import os, random
from scraper import scrape

app = Flask(__name__)
random.seed(0)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		currency = request.form['currency']
		city = request.form['location']
		start = request.form['start']
		end = request.form['end']
		adultes = int(request.form['adultes'])
		rooms = int(request.form['rooms'])
		print(currency, city, start, end, adultes, rooms)
		scrape(currency, city, start, end, adultes, rooms)
		return render_template('index.html')
	else:
		return render_template('index.html')	


if __name__ == '__main__':
	app.run(debug=True)
