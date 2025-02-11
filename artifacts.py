import threading
from basic_functions import *


def ash_tree(character):
    if not comp_locations(get_location(character), (-1,0)):
        time.sleep(action("move", character=character, data={"x":-1, "y":0}))
    while True:
        try:
            for i in range(100-get_inventory(character)[1]):
                time.sleep(action("gather", character=character))
                time.sleep(action("move", character=character, data={"x":-1,"y":0}))
            deposit(character=character, stuff="ash_wood", amount=100)
            time.sleep(action("move", character=character, data={"x":-1,"y":0}))
        except:
            bad_exception(character)
            time.sleep(40)


def level_up_weapon_crafting(character):
    if not comp_locations(get_location(character), (2,0)):
        time.sleep(action("move", character=character, data={"x":2,"y":0}))

    while True:
        for i in range(48):
            try:
                time.sleep(action("gather", character=character))
            except:
                bad_exception(character)
                time.sleep(40)
        time.sleep(action("move", character=character, data={"x":1,"y":5}))
        time.sleep(action("craft", character=character, data={"code":"copper","quantity": 6}))
        time.sleep(action("move", character=character, data={"x":2,"y":1}))
        time.sleep(action("craft", character=character, data={"code":"copper_dagger","quantity": 1}))
        deposit(character=character, stuff="copper_dagger", amount=1)
        time.sleep(action("move", character=character, data={"x":2,"y":0}))




if __name__ == "__main__":
    Jman5213 = threading.Thread(target=level_up_weapon_crafting, args=("Jman5213",))
    JmanBob = threading.Thread(target=ash_tree,args=("JmanBob",))
    JmanTree = threading.Thread(target=simple_fight,args=("JmanTree",))

    JmanBob.start()
    Jman5213.start()
    JmanTree.start()