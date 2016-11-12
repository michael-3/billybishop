from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def chat():
    return render_template("chat.html")

@app.route('/', methods=['POST'])
def send_msg():
	text = request.form['text']
	return text

if __name__ == '__main__':
    app.run()
