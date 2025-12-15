import string


def check_string(charlist):
    for char in charlist:
        if char not in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) + ['ą', 'ę', 'ó', 'ś', 'ł', 'ż', 'ź', 'ć', 'ń'] + ['Ą', 'Ę', 'Ó', 'Ś', 'Ł', 'Ż', 'Ź', 'Ć', 'Ń'] + ['.', '{', '}', ',', '?', '!', '/', ' ', '_', '-', '=', '+', "\n", ":"]:
            return False
    return True


def check_sid(charlist):
    for char in charlist:
        if char not in list(string.ascii_lowercase) + ['_']:
            return False
    return True


def replace_unicode(charlist):
    text = charlist.replace("ł", "\\u0142")
    text = text.replace("ę", "\\u0119")
    text = text.replace("ó", "\\u00f3")
    text = text.replace("ą", "\\u0105")
    text = text.replace("ś", "\\u015b")
    text = text.replace("ż", "\\u017c")
    text = text.replace("ź", "\\u017a")
    text = text.replace("ć", "\\u0107")
    text = text.replace("ń", "\\u0144")
    text = text.replace("\n", "\\n")
    
    text = text.replace("Ę", "\\u0118")
    text = text.replace("Ó", "\\u00d3")
    text = text.replace("Ą", "\\u0104")
    text = text.replace("Ś", "\\u015a")
    text = text.replace("Ż", "\\u017b")
    text = text.replace("Ź", "\\u0179")
    text = text.replace("Ć", "\\u0106")
    text = text.replace("Ń", "\\u0143")
    
    text = text.replace("Ł", "\\u0141")
    
    return text
