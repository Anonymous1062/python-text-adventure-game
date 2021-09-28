import random, os, json

class Controller:

    def __init__(self, worldname, playername):
        self.world = World(worldname)
        self.player = Player(playername)

    def play_game(self):
        self.world.create_world()
        firstRoom = self.world.first_room()
        self.player.set_current_room(firstRoom)
        while True:
#            inventorySize = len(self.player.inventory)
#            if self.player.inventory[inventorySize - 1].itemtype == "victory":
#                print("Well done " + self.player.playername + ", you have achieved a victory.")
#                break
#            else:
            if self.player.check_victory() == 3:
                print("Well done " + self.player.playername + ", you have beaten the game.")
                break
            self.player.currentRoom.describe()
            print("Possible actions: move, pick up, inventory")
            playerInput = input("What do you do? ").lower()
            if playerInput == "move":
                moveLoc = input("Which room do you move to? ")
                changed = False
                for i in range(len(self.world.rooms)):
                    if moveLoc == self.world.rooms[i].name:
                        moveTo = self.world.rooms[i]
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
            else:
                print("This is no valid action")
       

class World:
    rooms = []

    def __init__(self, name):
        self.worldName = name

    def create_world(self):
        with open(self.worldName + ".json", "r") as f:
            world = json.load(f)
        for dict in world:
            room = list(dict.values())
            itemlist = []
            for i in range(len(room[2])):
                newItem = Item(room[2][i], room[3][i])
                itemlist.append(newItem)
            self.add_room(room[0], room[1], itemlist)

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
    
    def add_room(self, name, exits, items):
        newRoom = Room(name, exits, items)
        self.rooms.append(newRoom)

    def first_room(self):
        return self.rooms[0]

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
        for i in range(len(self.items)):
            currentItem = self.items[i]
            itemNames.append(currentItem.name)
        print("These items are in this room: " + ', '.join(itemNames))
        print("\n")

class Player:
    inventory = []

    def __init__(self, name):
        self.playername = name 
    
    def goto_room(self, name):
        if name.name in self.currentRoom.exits:
            self.currentRoom = name
        else:
            print("Room not available from here")

    def set_current_room(self, room):
        self.currentRoom = room

    def get_current_room(self):
        return self.currentRoom

    def pick_up(self, item):
        for i in range(len(self.currentRoom.items)):
            if item == self.currentRoom.items[i - 1].name.lower():
                self.inventory.append(self.currentRoom.items[i - 1])
                self.currentRoom.items.pop(i - 1)
                
        #if item in self.currentRoom.items:
        #    self.currentRoom.items.remove(item)
        #    self.inventory.append(item)
        #else:
        #    print("Item not found in this room")
    
    def check_inventory(self):
        inv = []
        for i in range(len(self.inventory)):
            inv.append(self.inventory[i].name)
        return inv

    def check_victory(self):
        winitems = 0
        for i in range(len(self.inventory)):
            if self.inventory[i].itemtype == "victory":
                winitems += 1
        print(str(winitems) + " aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        return winitems

class Item:
    def __init__(self, iname, itype):
        self.name = iname
        self.itemtype = itype

wn = input("Which world do I load in? ").lower()
pn = input("Name your player: ")
game = Controller(wn, pn)
game.play_game()