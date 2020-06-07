from random import randrange

from os import listdir
from os.path import isfile, join

class GameTracker:
    current_index = 0
    current_key = ''

    creatures = {}

    init_order = []
    hold_list = []

    def __init__(self):
        pass

    def pick_encounter(self):
        files = [f for f in listdir("encounters") if isfile(join("encounters", f))]

        print("\nAvailable Encounters")
        key = 0
        while key < len(files):
            file_name = files[key].replace(".csv", "").replace("-", " ")
            print(f"{key}: {file_name}")
            key = key + 1

        encounter = int(input("Which encounter would you like to run? "))

        efile = open("encounters/" + files[encounter], 'r')
        next(efile)
        for line in efile:
            mob = line.rstrip().split(",")

            initiative = randrange(1, 20) + int(mob[2])
            if int(mob[2]) < 10:
                mob[2] = '0' + mob[2]
            key = float(str(initiative) + '.' + mob[2] + str(randrange(10, 99)))

            self.creatures[key] = mob[0] + " (cr " + mob[1] + ")"
        efile.close()

    def player_initiative(self):
        pfile = open("players.csv", 'r')
        next(pfile)
        for line in pfile:
            player = line.rstrip().split(",")

            initiative = input(f"Player {player[0]} Initiative: ")
            if int(player[1]) < 10:
                player[1] = '0' + player[1]
            key = float(str(initiative) + '.' + player[1] + str(randrange(10, 99)))

            self.creatures[key] = player[0]
        pfile.close()

    def set_order(self):
        self.init_order = sorted(self.creatures, reverse=True)
        self._set_current_key()

        print("\n-----")
        print("\nAvailable commands: [next|insert|hold|remove|add|exit]")

    def get_current(self):
        return self.creatures[self.current_key]

    def handle_actions(self, action):
        method = getattr(self, "_"+action, (lambda: 'Invalid'))
        method()

    def _next(self):
        self.current_index += 1

        self._check_for_new_round()
        self._set_current_key()

    def _remove(self):
        self.init_order.pop(self.current_index)

        self._check_for_new_round()
        self._set_current_key()

    def _hold(self):
        creature = {
            'name': self.creatures[self.current_key],
            'key': self.current_key
        }
        self.hold_list.append(creature)

        self._remove()

    def _insert(self):
        if len(self.hold_list) > 0:
            print("\nCreatures available for insert:")

            key = 0
            for creature in self.hold_list:
                print(f"{key}: {creature['name']}")
                key = key + 1

                index = -1

                while index < 0:
                    insert = input("Which creature would you like to insert? ")
                    if insert.isdigit():
                        index = int(insert)

                        if index in self.hold_list:
                            self.init_order.insert(self.current_index, self.hold_list[index]['key'])
                            self.hold_list.pop(index)

                            self._set_current_key()
                        else:
                            print("Invalid Creature")
                    else:
                        print("Selection is not a Number.")

        else:
            print("\nNo creatures available for insert.")

    def _add(self):
        creature = input("New creatures name: ")

        c_type = ''
        while c_type != 'y' and c_type != 'n':
            c_type = input("Is this creature a player? (y/n)  ")

            if c_type == 'n':
                cr_level = input("What is the creatures CR? ")

                creature += " ("+cr_level+")"

        new_key = randrange(111, 999)
        self.creatures[new_key] = creature
        self.init_order.insert(self.current_index, new_key)

        self._set_current_key()

    def _exit(self):
        print("Good Bye!")

    def _check_for_new_round(self):
        if self.current_index == len(self.init_order):
            self.current_index = 0
            print("\nNew Round\n")

    def _set_current_key(self):
        self.current_key = self.init_order[self.current_index]

game_tracker = GameTracker()