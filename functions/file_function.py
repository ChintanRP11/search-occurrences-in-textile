# fucntion which called during the api call
import os
from functions.sentence_functions import compare_res, create_sentences, line_wise_search


def make_sentences_data(search_text):
    search_string = search_text.lower()
    try:
        text_file = "king-i-150.txt"
        
        occurrences = create_sentences(text_file, search_string)
        testing = False
        # validating the result
        if(testing == True):
            org_res = line_wise_search(text_file, search_string)
            print(org_res)
            is_same = compare_res(occurrences, org_res)
            print("Correct answer: ", is_same)
        
        return occurrences
    except Exception as e:
        raise FileNotFoundError(f"Source file not found")
