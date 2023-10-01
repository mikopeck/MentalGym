def decode_if_needed(s):
    try:
        decoded_s = s.encode('latin1').decode('unicode_escape')
        if s != decoded_s:
            return decoded_s
        else:
            return s
    except:
        return s  # Return original string if decoding fails