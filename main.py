"""
Målet med spillet mitt er å få alle 8 delene til romskipet.
For å gjøre dette må du gå gjennom alle stedene og finne alle delene.
Men noen steder er det farlig, så du må passe på at du ikke dør.
For å bevege deg rundt i spillet må du skrive inn veiene som står ved valgene.
"""

import json
import sys
import os
import time

def clear():
    print('\n' * 49)

devmode = False

class Character:
    def __init__(self, name, health, inventory, level):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.level = level

if not os.path.exists("./data/save.json"):
    with open("./data/save.json", "w"): pass

save_raw = open("./data/save.json")
levels_raw = open("./data/levels.json")
deaths_raw = open("./data/deaths.json")
items_raw = open("./data/items.json")
chests_raw = open("./data/chests.json")
save_data = {}
levels_data = {}
deaths_data = {}
items_data = {}
chests_data = {}

try:
    save_data = json.load(save_raw)
except json.decoder.JSONDecodeError:
    print("⚠️    SAVE DATA CORRUPTED    ⚠️")

try:
    levels_data = json.load(levels_raw)
    deaths_data = json.load(deaths_raw)
except json.decoder.JSONDecodeError:
    print("⚠️    LEVEL DATA CORRUPTED    ⚠️")
    time.sleep(5)
    sys.exit("⚠️    LEVEL DATA CORRUPTED    ⚠️")
try:
    items_data = json.load(items_raw)
    chests_data = json.load(chests_raw)
except json.decoder.JSONDecodeError:
    print("⚠️    ITEM DATA CORRUPTED    ⚠️")
    time.sleep(5)
    sys.exit("⚠️    ITEM DATA CORRUPTED    ⚠️")

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
    if devmode:
        print("----- \033[96m\033[1m[               Devmode is enabled              ]\033[0m")

    if save_data == {} or died:
        print("No save found, creating new......\n\n")
        character = Character(
            input("Enter character name > "), 20, ["0/8"], "game-level-start")
    else:
        level = levels_data[save_data["level"]]

        choice = input(
            f"Recover save? Level: {level['name']} | Health: {save_data['health']} | Name: {save_data['name']} > ").lower()
        if choice == "yes":
            character = Character(
                save_data["name"], save_data["health"], save_data["inventory"], save_data["level"])
        elif choice == "no":
            character = Character(input("Enter character name > "), 20, ["0/8"], "game-level-start")
        else:
            sys.exit("invalid choice bruh")

    #save_game(character)

    if died is False:
        print("\n----- Weclome to this text RPG")
        print("----- Your goal is to get all 8 spaceship parts")
        print("----- On each level you will get your available ways to go")
        print("----- To select one, type in your choice and press enter\n")
        print("----- Shortcuts: 0 = exit, 1 = restart, 2 = inventory")
        if devmode:
            print("----- Devmode Shortcuts: 3 = save game, 4 = erase save, 5 = instant win\n")

    load_level(character, False)


def assemble(character):
    if "wrench" in character.inventory:
        clear()
        print("----- Starting spaceship assembly")
        time.sleep(2)
        clear()
        print("----- Used 8/8 spaceship parts")
        time.sleep(1)
        print("----- Used wrench")
        time.sleep(2)
        clear()
        print("----- Your spaceship is ready")
        print("----- Thank you for playing")
        time.sleep(2)
        sys.exit("----- Exited")
    else:
        print("----- A wrench is needed to assemble spaceship")


def load_level(character, restart):
    if not devmode:
        save_game(character)

    if "8/8" in character.inventory:
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
            choice = input("Open chest? > ")
            if choice == "yes":
                print("----- Chest contained: \n")
                for item in chests_data[chest]["items"]:
                    print(f"----- {item}")
                    get_item(character, item)
                print("")
            elif choice == "no":
                pass
        for item in items:
            if items_data[item]["demage"].endswith("/8"):
                print(f"You just found {items_data[item]['name']}!")
                print("It has been added to your inventory \n")
                character.inventory[0] = items_data[item]["demage"]
            elif int(items_data[item]["demage"]) == 0:
                print(
                    f"You found a {items_data[item]['name']}, will this be useful later?")
                choice = input(
                    f"Pick up item? Name: {items_data[item]['name']} > ")
                if choice == "yes":
                    get_item(character, item)
                elif choice == "no":
                    pass
            elif int(items_data[item]["demage"]) < 0:
                healing = 0 - int(items_data[item]['demage'])
                choice = input(
                    f"Consume {items_data[item]['name']}? +{healing} health > ")
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
                choice = input(
                    f"Pick up item? Name: {items_data[item]['name']} - Demage: {items_data[item]['demage']} > ")
                if choice == "yes":
                    get_item(character, item)
                elif choice == "no":
                    pass

    print(f"Avaible ways to go are: {exits}")

    choice = input(f"Level: {level_name} | Health: {character.health} | Name: {character.name} > ")

    def choices():
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

    match choice:
        case "0":
            sys.exit("Exited")
        case "1":
            erase_save()
            main(False)
        case "2":
            clear()
            print(f"----- Spaceship Parts: {character.inventory[0]}")
            print(f"----- Inventory: {character.inventory[1:]}")
            load_level(character, True)
        case "3":
            if devmode:
                save_game(character)
                print("----- Saved game")
            load_level(character, True)
        case "4":
            if devmode:
                erase_save()
                print("----- Save erased")
            load_level(character, True)
        case "5":
            if devmode:
                character.inventory[0] = "8/8"
                character.inventory.append("wrench")
            load_level(character, True)
        case _:
            choices()


def death(data, character):
    print(deaths_data[data])
    print("Going back to last level in 5...")
    time.sleep(5)
    main(True, character)


main(False)