import json
import sys
import time

def clear():
    print('\n' * 49)

class Character:
    def __init__(self, name, health, inventory, level):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.level = level

save = open("./data/save.json")
levels = open("./data/levels.json")
deaths = open("./data/deaths.json")
items = open("./data/items.json")
chests = open("./data/chests.json")
save_data = {}
levels_data = {}
deaths_data = {}
items_data = {}
chests_data = {}

try:
    save_data = json.load(save)
except:
    print("⚠    SAVE DATA CORRUPTED    ⚠️")

try:
    levels_data = json.load(levels)
    deaths_data =  json.load(deaths)
except:
    print("⚠    LEVEL DATA CORRUPTED    ⚠️")
    time.sleep(5)
    sys.exit("⚠    LEVEL DATA CORRUPTED    ⚠️")
try:
    items_data = json.load(items)
    chests_data = json.load(chests)
except:
    print("⚠    ITEM DATA CORRUPTED    ⚠️")
    time.sleep(5)
    sys.exit("⚠    ITEM DATA CORRUPTED    ⚠️")

def save_game(character):
    character_data = {
        "name": character.name,
        "health": character.health,
        "inventory": character.inventory,
        "level": character.level
    }

    json_data = json.dumps(character_data, indent=4)
    
    with open("./data/save.json", "w") as f:
        f.write(json_data)

def erase_save():
    with open("./data/save.json", "w") as f:
        f.write("{}")
        
def get_item(character, item):
    character.inventory.append(item)


def main(died, character=""):
    if save_data == {}:
        print("No save found, creating new......\n\n")
        character = Character(input("Enter character name > "), 20, [], "game-level-start")
    elif died:
        pass
    else:
        level = levels_data[save_data["level"]]
        
        choice = input(f"Recover save? Level: {level['name']} | Health: {save_data['health']} | Name: {save_data['name']} > ").lower()
        if choice == "yes":      
            character = Character(save_data["name"], save_data["health"], save_data["inventory"], save_data["level"])
        elif choice == "no":
             character = Character(input("Enter character name > "), 20, ["0/10"], "game-level-start")
        else:
            sys.exit("invalid choice bruh")
    
    save_game(character)

    if died == False:
        print("\n----- Weclome to this text RPG")
        print("----- Your goal is to get all 10 spaceship parts")
        print("----- On each level you will get your available ways to go")
        print("----- To select one, type in your choice and press enter\n")

    load_level(character, False)

def assemble(character):
    if "wrench" in character.inventory:
        clear()
        print("----- Starting spaceship assembly")
        time.sleep(2)
        clear()
        print("----- Used 10/10 spaceship parts")
        time.sleep(1)
        print("----- Used wrench")
        time.sleep(2)
        clear()
        print("----- Your spaceship is ready")
        print("----- Thank you for playing")
        time.sleep(2)
        sys.exit("---- Exited")
    else:
        print("----- A wrench is needed to assemble spaceship")

def load_level(character, restart):
    save_game(character)

    if "10/10" in character.inventory:
        assemble(character)
    level(levels_data[character.level], character, restart)

def level(level, character, restart):
    if restart:
        pass
    else:
        print("")
        for message in level["messages"]:
            print(message)
        print("")

    level_name = level["name"]
    destinations = level["destinations"]
    items = level["items"]
    exits = level["exits"]
    chests = level["chests"]

    if restart:
        pass
    else:
        for chest in chests:
            choice = input(f"Open chest? > ")
            if choice == "yes":
                print("----- Chest contained: \n")
                for item in chests_data[chest]["items"]:
                    print(f"----- {item}")
                    get_item(character, item)
                print("")
            elif choice == "no":
                pass
        for item in items:
            if items_data[item]["demage"].endswith("/10"):
                print(f"You just found {items_data[item]['name']}!")
                print("It has been added to your inventory \n")
                character.inventory[0] = items_data[item]["demage"]
            elif int(items_data[item]["demage"]) == 0:
                print(f"You found a {items_data[item]['name']}, will this be useful later?")
                choice = input(f"Pick up item? Name: {items_data[item]['name']} > ")
                if choice == "yes":
                    get_item(character, item)
                elif choice == "no":
                    pass
            elif int(items_data[item]["demage"]) < 0:
                healing = 0 - int(items_data[item]['demage'])
                choice = input(f"Consume {items_data[item]['name']}? +{healing} health > ")
                if choice == "yes":
                    if character.health >= 20:
                       print("You are at full health, cannot consume!")
                    elif character.health + healing >= 20:
                        character.health = 20
                    else:
                        character.health += healing
                elif choice == "no":
                    pass
            else:
                choice = input(f"Pick up item? Name: {items_data[item]['name']} - Demage: {items_data[item]['demage']} > ")
                if choice == "yes":
                    get_item(character, item)
                elif choice == "no":
                    pass

        print(f"Avaible ways to go are:  {exits}")

    choice = input(f"Level: {level_name} | Health: {character.health} | Name: {character.name} > ")
    
    if choice in exits:
        for ext in exits:
            if choice == ext:
                if destinations[ext].startswith("game-death"):
                    clear()
                    death(destinations[ext], character)
                else:
                    clear()
                    character.level = destinations[ext]
                    load_level(character, False)
                    
    else:
        clear()
        print(f"{choice} is not a valid way")
        load_level(character, True)

def death(data, character):
    #erase_save()
    print(deaths_data[data])
    print("Going back to last level in 5...")
    time.sleep(5)
    main(True, character)

main(False)
