import json
from room import *

#this class basically makes and then stores all existing rooms
class World:
    rooms = []

    def __init__(self, name):
        self.worldName = name

    def create_world(self):
        with open(self.worldName + ".json", "r") as f:
            world = json.load(f)
        with open(self.worldName + " enemies.json", "r") as f:
            enemies = json.load(f)
        for roomdict in world:
            #takes the values only from the dictionaries, since the rest is for readability in the json file
            room = list(roomdict.values())
            itemlist = []
            enemylist = []
            #turns the item and itemtype from the json into objects of the class Item
            for i in range(len(room[2])):
                newItem = Item(room[2][i], room[3][i])
                itemlist.append(newItem)
            for i in range(len(room[4])):
                for enemydict in enemies:
                    enemy = list(enemydict.values())
                    if enemy[0] == room[4][i]:
                        if '+' in enemy[3]:
                            dice = enemy[3].split('+')
                            plusnr = dice[1]
                            dice = dice[0].split('d')
                        else:
                            dice = enemy[3]
                            plusnr = 0
                            dice = dice.split('d')
                        newEnemy = Enemy(enemy[0], enemy[1], enemy[2], dice[0], dice[1], plusnr, enemy[4], enemy[5])
                        enemylist.append(newEnemy)
            self.add_room(room[0], room[1], itemlist, enemylist)

    def add_room(self, name, exits, items, enemies):
        newRoom = Room(name, exits, items, enemies)
        self.rooms.append(newRoom)

    def first_room(self):
        return self.rooms[0]
