import random

name = input('What is your name?\n')

adjectives = ('Smart', 'Dumb', 'Short', 'Tall', 'Fat', 'Skinny')
animals = ('Pig', 'Capybara', 'Tiger', 'Deer', 'Hot dog', 'Bat')

random_adjective = random.choice(adjectives)
random_animal = random.choice(animals)

codename = f'{random_adjective} {random_animal}'

lucky_number = random.randint(1, 99)

print(f'{name}, your code name is: {codename}')
print(f'Your lucky number is: {lucky_number}')