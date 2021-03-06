from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
from twilio.rest import Client
import autocomplete
from gtts import gTTS
import os

# Set up the model.
autocomplete.load()
app = Flask(__name__)
CORS(app)

# The application
@app.route("/")
def index():
	return render_template("index.html")

# Create a class for custom error messages (reference: http://flask.pocoo.org/docs/0.12/patterns/apierrors/).
class InvalidUsage(Exception):
	status_code = 400

	# Initialize the InvalidUsage exception.
	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	# Convert the exception information into a dictionary.
	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

# Register the custom exception with the error handler (reference: http://flask.pocoo.org/docs/0.12/patterns/apierrors/).
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

# Converts English text to speech.
@app.route('/convert_text_to_speech', methods=['POST'])
def convert_text_to_speech():
	# Check to see if the required parameters are present.
	if 'text_to_convert' not in request.values.keys():
		raise InvalidUsage("No text included for conversion", status_code = 400)
		
	# Send the post request.
	tts = gTTS(text=request.values['text_to_convert'], lang='en')
	tts.save('converted_text.mp3')
	os.system('start converted_text.mp3')
	
	# Return the sound file.
	return send_file('converted_text.mp3', mimetype='audio/mpeg')

# Get suggestions for words that the user typed in.
@app.route('/get_suggestion', methods=['GET','POST'])
def get_suggestion():
	# Raise an exception if the required parameters are not specified.
	if "words" not in request.values.keys():
		raise InvalidUsage("No words were specified for prediction.", status_code = 400)
	
	# Predict the next word.
	text = request.values['words']
	prediction = [];
	if len(text.split(" ")) > 1:
		prediction = autocomplete.split_predict(text, 10)
	else:
		prediction = autocomplete.predict_currword(text, 10)
		
	return jsonify(prediction)
	
# Adds text message support to allow Don to send text messages.
@app.route('/send_text', methods=['GET', 'POST'])
def send_text():
	# Raise an exception if the required parameters are not specified.
	if "text" not in request.values.keys():
		raise InvalidUsage("The text message was not found in the request.", status_code = 400)
	if "to" not in request.values.keys():
		raise InvalidUsage("The to-number was not found in the request", status_code = 400)
	
	# Extract the required information from the request body.
	text = request.values['text']
	to_number = request.values['to']
	
	# Set up the account credentials - in a production project, this would be placed in a "secrets" file.
	account_sid = "ACbbd2cff98bcbbad08f76b03701a0f2d9"
	auth_token = "7d786ff14c6b4572a6e8e78f8ad6aee5"
	
	# Send the text message.
	client = Client(account_sid, auth_token)
	message = client.messages.create(
		from_="+12267992139",
		to=to_number,
		body=text)

	return jsonify({"to":to_number, "message":message.body, "error code":message.error_code})
	