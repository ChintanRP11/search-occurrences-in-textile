import json
from flask import Blueprint, app, jsonify, request
from functions.file_function import make_sentences_data

# This creates a new Flask Blueprint called search_routes_bp with the name search_routes. 
search_routes_bp = Blueprint('search_routes', __name__)

# Handler for HTTP GET requests to the /search endpoint
@search_routes_bp.route('/search', methods=['GET'])
def search_occurrences():
    query_text = request.args.get('query_text') 
    
    # if query parameter is not available
    if query_text is None:
        error_response = {
            "Error": "Missing 'query_text' parameter in the request."
        }
        return jsonify(error_response), 400
    
    if query_text == "":    # if query parameter is empty
        error_response = {
            "Error": "'query_text' parameter cannot be empty."
        }
        return jsonify(error_response), 400

    try: # if query parameter is one or more characters
        text_occurrences = make_sentences_data(query_text)

        response = {
            "query_text": query_text,
            "number_of_occurrences": len(text_occurrences),
            "occurrences": text_occurrences
        }

        return json.dumps(response, indent=2), 200, {'Content-Type': 'application/json'}
    
    except Exception as e: # Handling other unexpected exceptions
        error_response = str(e)
        return jsonify({"Error in server: ": error_response}), 500

