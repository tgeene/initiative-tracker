from os import listdir
from os.path import isfile, join

from random import randrange

print('\nINITIATIVE TRACKER')
print('-----')

files = [f for f in listdir('encounters') if isfile(join('encounters', f))]

print('\nAvailable Encounters')
key = 0
while key < len(files):
    file_name = files[key].replace(".csv", "").replace("-", " ")
    print(f'{key}: {file_name}')
    key = key + 1

encounter = int(input('Which encounter would you like to run? '))

creatures = {}
efile = open('encounters/' + files[encounter], 'r')
next(efile)
for line in efile:
    mob = line.rstrip().split(",")

    initiative = randrange(1, 20) + int(mob[2])
    if int(mob[2]) < 10:
        mob[2] = '0' + mob[2]
    key = float(str(initiative) + '.' + mob[2] + str(randrange(10,99)))

    creatures[key] = mob[0] + ' (lvl ' + mob[1] + ')'
efile.close()

print("\n-----\n")

pfile = open('players.csv', 'r')
next(pfile)
for line in pfile:
    player = line.rstrip().split(",")

    initiative = input(f'Player {player[0]} Initiative: ')
    if int(player[1]) < 10:
        player[1] = '0' + player[1]
    key = float(str(initiative) + '.' + player[1] + str(randrange(10,99)))

    creatures[key] = player[0]
pfile.close()

init_order = sorted(creatures, reverse=True)
current_index = 0

print("\n-----")
print("\nAvailable commands: [next|insert|hold|remove|exit]")

hold_list = []
action = 'start'
while action != 'exit':
    current_key = init_order[current_index]
    print(f"\nCurrent: {creatures[current_key]}")

    action = input('Command: ')

    if action == 'next':
        current_index = current_index + 1

        if current_index == len(init_order):
            current_index = 0

        current_key = init_order[current_index]
    elif action == 'hold' or action == 'remove':
        if action == 'hold':
            creature = {
                'name': creatures[current_key],
                'key': current_key
            }
            hold_list.append(creature)

        init_order.pop(current_index)
    elif action == 'insert':
        if len(hold_list) > 0:
            print('\nCreatures available for insert:')

            key = 0
            for creature in hold_list:
                print(f'{key}: {creature["name"]}')
                key = key + 1
			
			index = -1
			while index < 0:
				insert = input('Which creature would you like to insert? ')
				if re.search(r'\d', insert):
					index = int(insert)
					
					if 0 <= index < len(hold_list):
						init_order.insert(current_index, hold_list[index]['key'])
						hold_list.pop(index)
					else:
						print("Invalid Creature")
				else:
					print("Selection is not a Number.")
        else:
            print('\nNo creatures available for insert.')
    else:
	    print("Invalid Command")
