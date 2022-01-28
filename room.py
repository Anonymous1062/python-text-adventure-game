from item import *
from enemy import *

#this class has all the details about 1 specific room, and allows you to modify it if needed
class Room:
    def __init__(self, roomName, addExits, addItems, addEnemies, boss, checkpoint):
        self.name = roomName
        self.exits = addExits
        self.items = addItems
        self.enemies = addEnemies
        self.boss = boss
        if checkpoint == "yes":
            self.checkpoint = True
        else:
            self.checkpoint = False

    def describe(self):
        print("You are in " + self.name)
        print("From this room, you can go to: " + ', '.join(self.exits))
        itemNames = []
        #because items are objects of the class Item, you have to make a list with just the names for join
        for currentItem in self.items:
            itemNames.append(currentItem.name)
        print("These items are in this room: " + ', '.join(itemNames))
        print("\n")
