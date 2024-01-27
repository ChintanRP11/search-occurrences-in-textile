# fucntion which called during the api call
import os
from functions.sentence_functions import create_sentences
from functions.sentence_functions import compare_res, line_wise_search


# Function which is called during the API call. 
# It specify the textfile name. Handles the case for missing text_file.
def make_sentences_data(search_text):
    """
    Find occurrences of a search string in a text file.

    Args: search_text (str): The search string to look for in the text file.

    Returns:
        list: A list of occurrences of the search string, each represented as a dictionary
              containing line number, start index, end index, and the whole sentence containing the match.
    Raises:
        FileNotFoundError: If the source file is not found.
    """
    search_string = search_text.lower()
    try:
        text_file = "king-i-150.txt"
        
        occurrences = create_sentences(text_file, search_string)
        
        # Verification of results (Produces 99% correct results)
        testing = False
        if(testing == True):
            org_res = line_wise_search(text_file, search_string)
            print(org_res)
            is_same = compare_res(occurrences, org_res)
            print("Correct answer: ", is_same)
        
        return occurrences
    except Exception as e:
        raise FileNotFoundError(f"Source file not found")
