import requests
import time

# Server URL and configuration
server = "https://api.artifactsmmo.com"
token =''  # Your token (keep this secret)  # Your character name
url_base = f"{server}/my/"
character_colors = {"Jman5213":"\033[96m","JmanBob":"\033[91m","JmanTree":"\033[34m"}

locations = {
    "bank1":(4,1),
    "bank2":(7,13),
    "copper":(2,0),
    "ash_tree1":(6,1),
    "ash_tree2":(-1,0),
    "sunflower": (2, 2),
    "salmon1":(-3,-4),
    "salmon2":(-2,-4),
    "woodcutting":(-2,-3),
    "cooking":(1,1),
    "weaponcrafting":(2,1),
    "gearcrafting":(3,1),
    "jewelrycrafting":(1,3),
    "alchemy":(2,3),
    "mining":(1,5)
}

def action(to_do, character, data=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    actions = {
        "move": url_base + character + "/action/move",  # data {'x':[], 'y':[]}
        "fight": url_base + character + "/action/fight",
        "rest": url_base + character + "/action/rest",
        "gather": url_base + character + "/action/gathering",
        "unequip": url_base + character + "/action/unequip",  # data {"slot":"[slot-name]"}
        "craft": url_base + character + "/action/crafting",  # data {"code":"[item-name"], "quantity":[num]}
        "equip": url_base + character + "/action/equip",  # data {"code":"[item_name]", "slot":"[slot_name]"}
        "deposit": url_base + character + "/action/bank/deposit", # data {"code":"[item_name]", "quantity":[num]}
    }

    try:
        response = requests.post(actions[to_do], headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        json_data = response.json()["data"]
        print("|"+character_colors[character]+character.rjust(9," "),
              "\033[00m"+"|\033[92m","action: \033[00m"+json_data["cooldown"]["reason"].ljust(10," ")+"| cooldown:",
              str(json_data["cooldown"]["total_seconds"]).rjust(2,"0").rjust(4," "),"|")
        return json_data["cooldown"]["remaining_seconds"]
    except requests.exceptions.RequestException as error:
        print(error)


def get_location(character):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url_base+f"characters/{character}", headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        json_data = response.json()["data"]
        print("|"+character_colors[character]+character.rjust(9," "),
              "\033[00m"+"|\033[92m","action:\033[00m",
              str(str(json_data["x"])+", "+str(json_data["y"])).ljust(10," ")+"| cooldown:",
              "none".rjust(2,"0"),"|")
        return json_data["x"], json_data["y"]
    except requests.exceptions.RequestException as error:
        print(error)


def comp_locations(loc1, loc2):
    return all(x == y for x, y in zip(loc1, loc2))


def get_inventory(character):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url_base+f"characters/{character}", headers=headers)
        response.raise_for_status()
        json_data = response.json()["data"]
        print("|" + character_colors[character] + character.rjust(9, " "),
              "\033[00m" + "|\033[92m",
              "action:\033[00m",
              "get inv.".ljust(10, " ") + "| cooldown:",
              "none".rjust(2, "0"), "|")
        inventory = {}
        total_items = 0
        for item in json_data["inventory"]:
            inventory[item["code"]] = item["quantity"]
            total_items += item["quantity"]

        return inventory, total_items, json_data["inventory_max_items"]
    except requests.exceptions.RequestException as error:
        print(error)


def deposit(character, stuff, amount):
    if not comp_locations(get_location(character), (4,1)):
        time.sleep(action("move", character=character, data={"x": 4, "y": 1}))
    time.sleep(action("deposit", character=character, data={"code": stuff, "quantity": amount}))


def bad_exception(character):
    if not comp_locations(get_location(character), (0, 1)):
        time.sleep(action("move", character=character, data={"x": 0, "y": 1}))
    inv = get_inventory(character)
    if inv[1] == inv[2]:
        for key, value in inv.items():
            deposit(character, key, value)


def simple_fight(character):
    while True:
        try:
            time.sleep(action("fight", character=character))
            time.sleep(action("rest", character=character))
        except:
            bad_exception(character)
            time.sleep(40)
