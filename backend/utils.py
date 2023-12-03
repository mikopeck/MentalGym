import re

emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF\U0001FC00-\U0001FCFF\U0001FD00-\U0001FDFF\U0001FE00-\U0001FEFF\U0001FF00-\U0001FFFF]+", flags=re.UNICODE)

def decode_if_needed(s):
    # try:
    #     decoded_s = s.encode('latin1').decode('unicode_escape')
    #     if s != decoded_s:
    #         return decoded_s
    #     else:
    #         return s
    # except:
    #     return s
    return s
    
def extract_single_emoji(text):
    print(f"String: {text}")
    emojis = emoji_pattern.findall(text)
    print(f"Emojis: {emojis}")
    if emojis[0] == "\",":
        return None
    return emojis[0] if emojis else None

def remove_emojis(text):
    return emoji_pattern.sub(r'', text)

def remove_emojis_except_first(text):
    first_char = text[0] if text else ''
    if emoji_pattern.fullmatch(first_char):
        return first_char + emoji_pattern.sub(r'', text[1:])
    else:
        return emoji_pattern.sub(r'', text)