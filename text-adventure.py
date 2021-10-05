import random, os, json
#this class is used to control the menu and player inputs
class Controller:

    def __init__(self, worldname, playername):
        self.world = World(worldname)
        self.player = Player(playername)

    def play_game(self):
        self.world.create_world() #reads from file
        firstRoom = self.world.first_room()
        self.player.set_current_room(firstRoom)
        while True:
            if self.player.check_victory() == 3: #checks if 3 items with itemtype 'victory' are in inventory
                print("Well done " + self.player.playername + ", you have beaten the game.")
                break
            self.player.currentRoom.describe()
            print("Possible actions: move, pick up, inventory, equip")
            playerInput = input("What do you do? ").lower()
            if playerInput == "move":
                moveLoc = input("Which room do you move to? ")
                changed = False
                for i in range(len(self.world.rooms)):
                    if moveLoc == self.world.rooms[i].name:
                        moveTo = self.world.rooms[i] #so you'll move to a room, instead of a string with the same name as the room
                        changed = True
                if changed == True:
                    self.player.goto_room(moveTo)
                else:
                    print("Room not found")
            elif playerInput == "pick up":
                itemChoice = input("Which item do you pick up? ").lower()
                self.player.pick_up(itemChoice)
            elif playerInput == "inventory":
                inv = self.player.check_inventory()
                print("Your inventory: " + ', '.join(inv))
            elif playerInput == "equip":
                itemChoice = input("Which item do you want to equip? ").lower()
                self.player.equip_item(itemChoice)
            else:
                print("This is no valid action")
       
#this class basically makes and then stores all existing rooms
class World:
    rooms = []

    def __init__(self, name):
        self.worldName = name

    def create_world(self):
        with open(self.worldName + ".json", "r") as f:
            world = json.load(f)
        for dict in world:
            room = list(dict.values()) #takes the values only from the dictionaries, since the rest is for readability in the json file
            itemlist = []
            for i in range(len(room[2])): #turns the item and itemtype from the json into objects of the class Item
                newItem = Item(room[2][i], room[3][i])
                itemlist.append(newItem)
            self.add_room(room[0], room[1], itemlist)

    def add_room(self, name, exits, items):
        newRoom = Room(name, exits, items)
        self.rooms.append(newRoom)

    def first_room(self):
        return self.rooms[0]

#this class has all the details about 1 specific room, and allows you to modify it if needed
class Room:
    def __init__(self, roomName, addExits = [], addItems = []):
        self.name = roomName
        self.exits = addExits
        self.items = addItems

    def add_exit(self, room):
        self.exits.append(room)

    def add_item(self, itemname, itemtype):
        newItem = Item(itemname, itemtype)
        self.items.append(newItem)

    def describe(self):
        print("You are in " + self.name)
        print("From this room, you can go to: " + ', '.join(self.exits))
        itemNames = []
        for i in range(len(self.items)): #because items are objects of the class Item, you have to make a list with just the names for join
            currentItem = self.items[i]
            itemNames.append(currentItem.name)
        print("These items are in this room: " + ', '.join(itemNames))
        print("\n")

#this class knows everything about the player character, and can modify it all as well
class Player:
    inventory = []
    level = 1
    strength = 10
    dexterity = 10
    constitution = 10
    intelligence = 10
    faith = 10
    currency = 0

    def __init__(self, name, hp = 10, ac = 10):
        self.playername = name
        self.armourclass = ac
        self.maxHP = hp
        self.currentHP = hp
    
    
    def goto_room(self, room):
        if room.name in self.currentRoom.exits:
            self.currentRoom = room
        else:
            print("Room not available from here")

    def set_current_room(self, room):
        self.currentRoom = room

    def get_current_room(self):
        return self.currentRoom

    def pick_up(self, item):
        for i in range(len(self.currentRoom.items)): #loop through items in the room
            if item == self.currentRoom.items[i - 1].name.lower(): #if item asked to pick up is in the room
                self.inventory.append(self.currentRoom.items[i - 1]) #add item to inventory
                self.currentRoom.items.pop(i - 1) #remove item from room
                
    def check_inventory(self):
        inv = []
        for i in range(len(self.inventory)): #puts the names of the items in the inventory in inv, to make it easier to print
            inv.append(self.inventory[i].name)
        return inv

    def check_victory(self):
        winitems = 0
        for i in range(len(self.inventory)): #loops through the inventory to see if you have enough type 'victory' items
            if self.inventory[i].itemtype == "victory":
                winitems += 1
        return winitems

    def equip_item(self, item):
        for i in range(len(self.inventory)):
            if item == self.inventory[i - 1].name.lower(): #check if you have the item in your inventory
                if self.inventory[i - 1].itemtype[:2] == "ac": #check if it's armour
                    print(self.inventory[i - 1].itemtype[2:4])
                    self.armourclass = self.inventory[i - 1].itemtype[2:4] #change armourclass to the one specified
                    print(self.armourclass)
    
    def level_up(self, added):
        if added == "strength":
            self.strength += 1
            self.level += 1
            self.currency -= 1
        elif added == "dexterity":
            self.dexterity += 1
            self.level += 1
            self.currency -= 1
        elif added == "constitution":
            self.constitution += 1
            self.level += 1
            self.currency -= 1
        elif added == "intelligence":
            self.intelligence += 1
            self.level += 1
            self.currency -= 1
        elif added == "faith":
            self.faith += 1
            self.level += 1
            self.currency -= 1
        else:
            print("Stat to level up not found")
    


#very simple class which stores information about an item
class Item:
    def __init__(self, iname, itype):
        self.name = iname
        self.itemtype = itype

wn = input("Which world do I load in? ").lower()
pn = input("Name your player: ")
game = Controller(wn, pn)
game.play_game()


'''
with open(self.worldName + " rooms.txt") as f:
    file = f.read().split('\n')

for content in file:
    if not content == '':
        roomName, newexits = content.split("=")
        #print(roomName)
        newExit = newexits.split(',')
        #print(newExit)
        newRoom = Room(roomName)
        newRoom.exits = [] #for some reason it retains the exits from the last iteration of the for loop without this
        #print(newRoom)
        #print(newRoom.name)
        #print(newRoom.exits)
        for i in range(len(newExit)):
            newRoom.add_exit(newExit[i - 1])
            #print(newExit[i - 1])
        #print(newRoom.exits)
        self.rooms.append(newRoom)
f.close()

with open(self.worldName + " items.txt") as f:
    file = f.read().split('\n')

for content in file:
    if not content == '':
        room, newItems = content.split("=")
        itemList = newItems.split(',')
        for i in range(len(itemList)):
            newItemname, newItemtype = itemList[i].split('/')
            print(newItemname + " " + newItemtype)
            newItem = Item(newItemname, newItemtype)
            for currentRoom in self.rooms:
                if room == currentRoom.name:
                    print(currentRoom.name)
                    #print(newItem)
                    currentRoom.items.append(newItem)
                    print(currentRoom.items)
                    #print(i.items[i].name)
f.close()
'''