def personalCodeValid(code):
    if "-" in code:
        splitted_code = code.split('-')
        if (len(splitted_code[0]) == 6 and all(char.isdigit() for char in splitted_code[0])):
            if (len(splitted_code[1]) == 5 and all(char.isdigit() for char in splitted_code[1])):
                return True
    return False

def profileNumberCheck(text, profiles_count):
    splitted_text = text.split(' ')
    if len(splitted_text) == 2 and splitted_text[0] == "Профиль":
        if len(splitted_text[1]) == 1 and splitted_text[1].isdigit():
            if int(splitted_text[1]) <= profiles_count:
                return True
    return False