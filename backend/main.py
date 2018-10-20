from flask import Flask, jsonify, request
import autocomplete

# Set up the model.
autocomplete.load()
app = Flask(__name__)

# Create a class for custom error messages (reference: http://flask.pocoo.org/docs/0.12/patterns/apierrors/).
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

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