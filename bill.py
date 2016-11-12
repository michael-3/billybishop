from flask import Flask
app = Flask(__name__)

@app.route('/')
def main_app():
	return 'Billy Bishop Chatbot'
