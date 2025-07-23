age = {'Hans': 24, 'Prag': 23, 'Bunyod': 18}
print(age)
print(age['Hans'])
new_age = {'Prag':30}
age.update(new_age)
print(age['Prag'])
del age['Bunyod']
print(age)