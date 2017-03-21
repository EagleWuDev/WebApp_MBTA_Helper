"""
Simple "Hello, World" application using Flask
"""
from mbta_helper import find_stop_near
from flask import Flask, render_template, request
app = Flask(__name__)

app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		placeName = str(request.form["place"])
		typeTrans = str(request.form["transType"])
		ret = find_stop_near(placeName, typeTrans)
		print(ret)
		return render_template('index.html', stops = ret, placeName = placeName)
	else:
		return render_template('index.html')


if __name__ == '__main__':
    app.run()
