def check_string(text):
    if text.startswith('The'):
        return'Fount it!'
    else:
        return'Nope.'

str1 = 'The'
str2 = 'Thumps up'
str3 = 'Theatre can be boring'

print(check_string(str1))
print(check_string(str2))
print(check_string(str3))