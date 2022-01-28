import json
from room import *
from global_functions import *

#this class basically makes and then stores all existing rooms
class World:
    rooms = []

    def __init__(self, name):
        self.worldName = name

    def create_world(self):
        with open(self.worldName + ".json", "r") as f:
            world = json.load(f)
        for roomdict in world:
            #takes the values only from the dictionaries, since the rest is for readability in the json file
            room = list(roomdict.values())
            itemlist = []
            enemylist = []
            newBoss = False
            #turns the item and itemtype from the json into objects of the class Item
            for i in range(len(room[2])):
                newItem = Item(room[2][i], room[3][i])
                itemlist.append(newItem)
            for i in range(len(room[4])):
                enemylist.append(self.read_enemies(room[4], i))
            if room[5] != "":
                newBoss = self.read_boss(room[5])
            self.add_room(room[0], room[1], itemlist, enemylist, newBoss, room[6])

    #takes the correct enemies from the file to put into the room
    def read_enemies(self, thisRoom, i):
        with open(self.worldName + " enemies.json", "r") as f:
            enemies = json.load(f)
        for enemydict in enemies:
            enemy = list(enemydict.values())
            if enemy[0] == thisRoom[i]:
                dice, plusnr = split_dice(enemy[3])
                newEnemy = Enemy(enemy[0], enemy[1], enemy[2], dice[0], dice[1], plusnr, enemy[4], enemy[5])
                return newEnemy

    #takes the correct boss from the file to put into the room
    def read_boss(self, bossName):
        with open(self.worldName + " bosses.json", "r") as f:
            bosses = json.load(f)
        for bossdict in bosses:
            boss = list(bossdict.values())
            if boss[0] == bossName:
                diecounts = []
                hitdice = []
                damagebonuses = []
                newBoss = Boss(boss[0], boss[1], boss[2], boss[3], boss[4], boss[5], boss[6], boss[7], boss[8], boss[9])
                return newBoss

    def add_room(self, name, exits, items, enemies, boss, checkpoint):
        newRoom = Room(name, exits, items, enemies, boss, checkpoint)
        self.rooms.append(newRoom)

    def first_room(self):
        return self.rooms[0]
