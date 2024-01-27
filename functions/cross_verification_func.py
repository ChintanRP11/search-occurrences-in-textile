import os
import re

# extra function for verification of results
def line_wise_search(file_name, search_text):
    """
    Creates result by searching line by line but it does not give the sentence for search_text
    """
    result = []
    search_text = search_text.lower()
    text_file_path = os.path.join(os.path.dirname(__file__), '..', 'text_files', file_name)

    with open(text_file_path, "r") as file:
        line = file.readline().lower()
        line_no = 1
        while(line):
            line = line.lower()
            st_ind = line.find(search_text)
            while(st_ind != -1):
                result.append([line_no, st_ind+1, st_ind+len(search_text)+1])
                st_ind = line.find(search_text, st_ind+1)
            
            line = file.readline()
            line_no += 1
    
    return result

# comparing occurrences and result from linewise search
def compare_res(occurrences, org_res):
    """
    It compares the result data from two functions (create_sentences, line_wise_search).
    IT only compares the line data(locatin of search_text)
    """
    res = False
    if(len(occurrences) == len(org_res)): res = True
    elif(len(occurrences) > len(org_res)): print("multiline result")

    for sen, org in zip(occurrences,org_res):
        if(sen["line"] == org[0] and sen["start"] == org[1] and sen["end"] == org[2]):
            continue
        else:
            print(sen, org)
            res = False
    
    return res
