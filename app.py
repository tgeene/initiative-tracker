from tracker import game_tracker

print("\nINITIATIVE TRACKER")
print("-----")

game_tracker.pick_encounter()

print("\n-----\n")

game_tracker.player_initiative()
game_tracker.set_order()

action = ''
while action != 'exit':
    print(f"\nCurrent: {game_tracker.get_current()}")

    action = input("Command: ")
    game_tracker.handle_actions(action)