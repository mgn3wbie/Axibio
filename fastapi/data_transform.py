import json

def _camel_to_snake(s):
    '''turn a CamelCase string into a snake_case one'''
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def process_octave_response_into_dict_list(json_data):
    '''turns an octave response into a list of dicts'''
    dict_list = []
    data = json_data["body"]
    i = 0
    while i < len(data):
        dict_list.append(data[i])
        i += 1
    return dict_list

def turn_camel_to_snake_case_for_dicts(dict_list):
    '''iterates over the dict_list and turns their keys into snake_case'''
    new_dict_list = []
    for dict in dict_list:
        temp_dict = {}
        for key, value in dict.items():
            temp_dict[_camel_to_snake(key)] = dict[key]
        new_dict_list.append(temp_dict)
    return new_dict_list
