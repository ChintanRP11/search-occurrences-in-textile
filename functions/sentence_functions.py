# function to find the end of sentence index, matches using pattern
# first argument is sentence (current line) and second argument is previous end of sentence value of current line
import os
import re


def find_eos_index(line, last_eos):
    """
    Find the end index for the sentence within the current line.

    Args:
        line (str): The current line.
        last_eos (int): The previous end of sentence value in current line.

    Returns:
        int: The index of the first occurrence of end of the sentence after last_eos, or -1 if not found.
    """
    patterns = [r'\.\"\s+[A-Za-z]', r'\.\s+[A-Za-z]', r'\.\s*\.', r'\.\n']
    end_ind_list = []
    for pattern in patterns:
        match = re.search(pattern, line[last_eos:])
        if match:
            if(pattern == r'\.\"\s+[A-Za-z]' or pattern == r'\.\s+[A-Za-z]'):
                end_ind_list.append(last_eos + match.end()-1)
            else:
                end_ind_list.append(last_eos + match.end())
    
    if len(end_ind_list) > 0:
        return min(end_ind_list)
    else:
        return -1

# look for search_string in sentence_data and create occurrences for the corresponding sentence
def find_occurrence_in_current_sentence(sentence_data, search_string):
    """
    Find occurrences of the search_string within the current sentence.

    Args:
        sentence_data (dict): The current sentence data, including the whole sentence and data of lines where it is divided.
        search_string (str): The search string to find in the sentence.

    Returns:
        list: A list of all occurrences of search string in sentence, each represented as a dictionary.
    """

    occurrences_in_sentence = []
    occ_in_sentence = {}
    current_sentence = sentence_data["sentence"].lower()    # converting to lowercase to remove case sensitivity
    
    # # check for all search_string in current_sentence
    # find first matching index, and loop for searching all following matches
    string_match = current_sentence.find(search_string)
    while(string_match != -1):
        match_index = string_match
        # line = [line_num, start, end, len] 
        # line[0] is line_number, line[1] is start_index for the sentence
        # line[2] is end_index of line for sentence
        # line[3] is length of current_line for sentence
        for line in sentence_data["lines"]: # scan through lines of sentence_data to find relevant line data
            
            # check for index if it lies in current-line of data
            if(match_index < line[2]-line[1]):
                occ_in_sentence["line"] = line[0]
                occ_in_sentence["start"] = match_index  + 1
                if(line[1] != 0): occ_in_sentence["start"] += line[1]    # if sentence does not start from 0 then match is after the start_index of sentence
                
                occ_in_sentence["end"] = occ_in_sentence["start"] + len(search_string)
                
                # # to handle search string divided into multi line
                # if(occ_in_sentence["end"] > line[3]+line[1]): 
                #     print(len(search_string), occ_in_sentence["start"], line[3])
                #     occ_in_sentence["end"] = len(search_string) + occ_in_sentence["start"] - line[3] - line[1] -1
                
                occ_in_sentence["in_sentence"] = sentence_data["sentence"].replace("\n", " ").strip()    # replacing \n and removing extra spaces
                occurrences_in_sentence.append(occ_in_sentence)  # add this occurence to occurrence
                occ_in_sentence = {}
                break
            else: # otherwise change/reduce the occst to look into next line
                if(line[1] == line[2]): match_index = 1 # if sentence start from end of previous line (\n)
                else: match_index -= line[3]    # otherwise update the match_index for next line
                
                if((line[2] - line[3]) != line[1]): match_index -= 1    # if sentence size does not match with data then reduce it
                
        string_match = current_sentence.find(search_string, string_match+1) # looking into letter part of the sentence
            
    return occurrences_in_sentence


# create structure for sentences array
# sentences = [...sentence]
# sentence_data = {
#     sentence: "whole statement including \n "
#     lines: [ ...[line number, start_index, end_index, length of line] ]
# }

# function to create all matching positions along with the sentence
def create_sentences(file_name, search_string):
    """
    Create sentence data for occurrences of the search_string in the given text file.

    Args:
        file_name (str): The name of the text file.
        search_string (str): The search string to find in the file.

    Returns:
        list: A list of all occurrences of search_string along with its whole sentence and corresponding line data, each represented as a dictionary.
    """
    text_file_path = os.path.join(os.path.dirname(__file__), '..', 'text_files', file_name)

    with open(text_file_path, "r") as file:
        line_number = 1
        sentence_data = {}
        current_sentence = ""
        lines = []

        line = file.readline()
        final_occurrences = []
        occurrences = []
        # reading file line by line until EOF
        while line:
            if(line == "\n"):   # if current line is blank and previous line does not ended before then it ends here add sentence_data into sentences
                lines.append([line_number, 0, 0, 0])
                sentence_data["sentence"] = current_sentence
                sentence_data["lines"] = lines
                
                # check for occurrences in recently created sentence
                occurrences = find_occurrence_in_current_sentence(sentence_data, search_string)
                if(len(occurrences) > 0): final_occurrences += occurrences
                
                # reseting sentence data
                sentence_data = {}
                lines = []
                current_sentence = ""
            
            else:
                eos_ind = find_eos_index(line, 0)   # find the end of sentence index
                
                # if line does not contain any end of sentence, add whole line into current_sentence and update lines array
                if eos_ind <= 0:    
                    current_sentence += line
                    lines.append([line_number, 0, len(line), len(line)])
                
                else:   # end of sentence found in line update the current_sentence, lines and sentence_data
                    sent_st = 0
                    # loop until all end of sentence found
                    while(eos_ind != -1):   # end of sentence found, complete the sentence and checking for search_string
                        
                        # if sentence start from middle of the line
                        if sent_st != 0: 
                            sent_st -= 1
                        
                        current_sentence += line[sent_st:eos_ind]
                        lines.append([line_number, sent_st, eos_ind, (eos_ind - sent_st)])
                        
                        # complete the sentence_data and check for occurrences
                        sentence_data["sentence"] = current_sentence 
                        sentence_data["lines"] = lines
                        occurrences = find_occurrence_in_current_sentence(sentence_data, search_string)
                        if(len(occurrences) > 0): final_occurrences += occurrences

                        # reseting the sentence_data, lines, current_sentence for next sentence
                        sentence_data = {}
                        lines = []
                        current_sentence = ""

                        sent_st = eos_ind   # maintaining start point for new sentences
                        eos_ind = find_eos_index(line, eos_ind) # find another end of sentence in current line
                        
                    # if no further end of sentence then add whole remaing line into current_sentence and update the lines array
                    if(line[sent_st:] != "\n"):
                        if(sent_st != len(line)): # if not end of the line
                            current_sentence = line[sent_st-1:]
                            lines.append([line_number, sent_st-1, len(line), len(line)-sent_st])

            # moving to next line
            line_number += 1    
            line = file.readline() 
        
        # case for last line in the file, complete sentence if any left 
        if(current_sentence != ""):
            sentence_data["sentence"] = current_sentence
            sentence_data["lines"] = lines
            occurrences = find_occurrence_in_current_sentence(sentence_data, search_string)
            if(len(occurrences) > 0): final_occurrences += occurrences
            
        return final_occurrences


# TESTING FUNCTIONS
# extra function for validation
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
