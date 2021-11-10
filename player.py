from global_functions import *
from item import *
from room import *
from stats import *

#this class knows everything about the player character, and can modify it all as well
class Player:
    inventory = []
    hitbonus = "strength"
    diecount = 1
    diesize = 1
    playerstats = Stats()

    def __init__(self, name, hp = 10, ac = 10):
        self.playername = name
        self.armourclass = ac
        self.maxHP = hp
        self.currentHP = hp

    def attack(self):
        balancingdivider = 1 #if too easy, to decrease dmg
        if self.hitbonus == "strength":
            tohit = roll(1, 20, ((self.playerstats.strength / balancingdivider) + 2))
            damage = roll(self.diecount, self.diesize, (self.playerstats.strength / balancingdivider))
        elif self.hitbonus == "dexterity":
            tohit = roll(1, 20, ((self.playerstats.dexterity / balancingdivider) + 2))
            damage = roll(self.diecount, self.diesize, (self.playerstats.dexterity / balancingdivider))
        return tohit, damage

    def get_hit(self, damage):
        self.currentHP -= damage
        if self.currentHP < 0:
            return "game over"

    def goto_room(self, room):
        if room.name in self.currentRoom.exits:
            self.currentRoom = room
        else:
            print("Room not available from here\n")

    def set_current_room(self, room):
        self.currentRoom = room

    def get_current_room(self):
        return self.currentRoom

    def pick_up(self, item):
        found = False
        for i in range(len(self.currentRoom.items)): #loop through items in the room
            if item == self.currentRoom.items[i - 1].name.lower(): #if item asked to pick up is in the room
                self.inventory.append(self.currentRoom.items[i - 1]) #add item to inventory
                self.currentRoom.items.pop(i - 1) #remove item from room
                found = True
        if found == False:
            print("Item not found in this room\n")

    def check_inventory(self):
        inv = []
        #puts the names of the items in the inventory in inv, to make it easier to print
        for i in range(len(self.inventory)):
            inv.append(self.inventory[i].name)
        return inv

    def check_victory(self):
        winitems = 0
        #loops through the inventory to see if you have enough type 'victory' items
        for i in range(len(self.inventory)):
            if self.inventory[i].itemtype == "victory":
                winitems += 1
        return winitems

    def equip_item(self, item):
        for i in range(len(self.inventory)):
            if item == self.inventory[i - 1].name.lower(): #check if you have the item in your inventory
                if self.inventory[i - 1].itemtype == "armour":
                    self.armourclass = self.inventory[i - 1].armourclass
                elif self.inventory[i - 1].itemtype == "weapon":
                    self.diesize = self.inventory[i - 1].hitdie
                    self.diecount = self.inventory[i - 1].diecount
