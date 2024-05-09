def sanitize_string(input_string):
    return input_string.replace('\x00', '')
