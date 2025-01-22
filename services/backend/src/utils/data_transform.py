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

# todo : make it recursive ? 
def turn_camel_to_snake_case_for_dicts(dict_list):
    '''iterates over the dict_list and turns their first level keys into snake_case'''
    new_dict_list = []
    for dict in dict_list:
        temp_dict = {}
        for key, value in dict.items():
            temp_dict[_camel_to_snake(key)] = dict[key]
        new_dict_list.append(temp_dict)
    return new_dict_list

def flatten_dict_depth(nested_dict: dict) -> dict:
    '''flattens a dict with nested dicts to have all values at same level. Will remove keys for dict values'''
    new_dict = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            new_dict.update(flatten_dict_depth(value))
        else:
            new_dict.update({key: value})
    return new_dict

def turn_energy_events_query_results_into_json(results):
    '''turns query results into json'''
    events = [row[0] for row in results]
    json_events = [
        {
            "id": event.id,
            "name": event.name,
            "seq": event.seq,
            "ts": event.ts.isoformat(),
            "temp": event.temp,
            "bat_ws": event.bat_ws,
            "reg_ws": event.reg_ws,
            "volts": event.volts,
            "period": event.period,
        }
        for event in events
    ]
    return json_events

def turn_logs_into_energy_events(energy_event_logs):
    '''takes the result of a query and turns it into a list of dict represented events'''
    events = []
    for id, event_data in energy_event_logs:

        result = flatten_dict_depth(event_data)
        result.update({"id": id, "name": "energy_inc"})
        events.append(result)
    events = turn_camel_to_snake_case_for_dicts(events)
    return events