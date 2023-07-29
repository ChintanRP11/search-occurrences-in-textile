import json
from flask import Blueprint, app, jsonify, request
from functions.file_function import make_sentences_data

search_routes_bp = Blueprint('search_routes', __name__)

# routes for app
@search_routes_bp.route('/search', methods=['GET'])
def search_occurrences():
    query_text = request.args.get('query_text') 
    
    if query_text is None:
        error_response = {
            "Error": "Missing 'query_text' parameter in the request."
        }
        return jsonify(error_response), 400
    
    if query_text == "":
        error_response = {
            "Error": "'query_text' parameter cannot be empty."
        }
        return jsonify(error_response), 400

    try:
        text_occurrences = make_sentences_data(query_text)

        response = {
            "query_text": query_text,
            "number_of_occurrences": len(text_occurrences),
            "occurrences": text_occurrences
        }

        return json.dumps(response, indent=2), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        # Handling missing file and other unexpected exceptions
        error_response = str(e)
        print("Error: ", error_response)
        return jsonify({"Error in server: ": error_response}), 500

