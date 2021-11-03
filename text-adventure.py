import random, os, json

#to roll a dice to see if you hit, how much damage you do, or other things. 2d20 + 5 is a = 2, b = 20, c = 5
#I wouldn't use a global function, but this is just much more efficient considering I use it in multiple functions
def roll(a, b, c):
    rolls = c
    for i in range(a):
        diceroll = random.randint(0, b)
        rolls += diceroll
    return int(rolls)

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
            #checks if 3 items with itemtype 'victory' are in inventory
            if self.player.check_victory() == 3:
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
                        #so you'll move to a room, instead of a string with the same name as the room
                        moveTo = self.world.rooms[i]
                        changed = True
                os.system("cls")
                if changed == True:
                    self.player.goto_room(moveTo)
                    if len(self.player.currentRoom.enemies) != 0:
                        self.combat()
                else:
                    print("Room not found\n")
            elif playerInput == "pick up":
                itemChoice = input("Which item do you pick up? ").lower()
                os.system("cls")
                self.player.pick_up(itemChoice)
            elif playerInput == "inventory":
                inv = self.player.check_inventory()
                os.system("cls")
                print("Your inventory: " + ', '.join(inv) + "\n")
            elif playerInput == "equip":
                itemChoice = input("Which item do you want to equip? ").lower()
                os.system("cls")
                self.player.equip_item(itemChoice)
            else:
                os.system("cls")
                print("This is no valid action\n")

    def combat(self):
        print("Combat has been initiated.")
        enemycount = len(self.player.currentRoom.enemies)
        for i in range(enemycount):
            print("Enemy " + str(i + 1) + ": " + self.player.currentRoom.enemies[i].name)
        selectedEnemy = int(input("Give the number of the enemy you want to attack: "))
        if selectedEnemy <= enemycount:
            playerhit, playerdmg = self.player.attack()
            enemystatus = self.player.currentRoom.enemies[selectedEnemy - 1].defend(playerhit, playerdmg)
            print(enemystatus)
            if enemystatus:
                self.player.currentRoom.enemies.pop(selectedEnemy - 1)
        for i in range(enemycount):
            print("Enemy " + str(i + 1) + " attacks...")
            enemydamage = self.player.currentRoom.enemies[i].attack(self.player.armourclass)
            if enemydamage > 0:
                self.player.currentHP -= enemydamage
                print("You currently have " + str(self.player.currentHP) + "/" + str(self.player.maxHP) + " HP")

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
                        newEnemy = Enemy(enemy[0], enemy[1], enemy[2], enemy[3], enemy[4], enemy[5], enemy[6], enemy[7])
                        enemylist.append(newEnemy)
            self.add_room(room[0], room[1], itemlist, enemylist)

    def add_room(self, name, exits, items, enemies):
        newRoom = Room(name, exits, items, enemies)
        self.rooms.append(newRoom)

    def first_room(self):
        return self.rooms[0]

#this class has all the details about 1 specific room, and allows you to modify it if needed
class Room:
    def __init__(self, roomName, addExits, addItems, addEnemies):
        self.name = roomName
        self.exits = addExits
        self.items = addItems
        self.enemies = addEnemies

    def describe(self):
        print("You are in " + self.name)
        print("From this room, you can go to: " + ', '.join(self.exits))
        itemNames = []
        #because items are objects of the class Item, you have to make a list with just the names for join
        for i in range(len(self.items)):
            currentItem = self.items[i]
            itemNames.append(currentItem.name)
        print("These items are in this room: " + ', '.join(itemNames))
        print("\n")

#this class knows everything about the player character, and can modify it all as well
class Player:
    inventory = []
    hitbonus = "strength"
    diecount = 1
    diesize = 1

    def __init__(self, name, hp = 10, ac = 10):
        self.playername = name
        self.armourclass = ac
        self.maxHP = hp
        self.currentHP = hp

    def attack(self):
        balancingdivider = 1 #if too easy, to decrease dmg
        if self.hitbonus == "strength":
            tohit = roll(1, 20, (self.strength / balancingdivider) + 2)
            damage = roll(self.diecount, self.diesize, (self.strength / balancingdivider))
        elif self.hitbonus == "dexterity":
            tohit = roll(1, 20, (self.dexterity / balancingdivider) + 2)
            damage = roll(self.diecount, self.diesize, (self.dexterity / balancingdivider))
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
                elif self.inventory[i - 1].itemtype == "weapon" :
                    self.diesize = self.inventory[i - 1].hitdie
                    self.diecount = self.inventory[i - 1].diecount


class Stats:
    level = 1
    exp = 0
    neededexp = 300
    strength = 0
    dexterity = 0
    constitution = 0
    intelligence = 0
    wisdom = 0
    charisma = 0

    def level_up(self, choice):
        if exp => neededexp:
            if choice == "strength":
                self.strength += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            elif choice == "dexterity":
                self.dexterity += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            elif choice == "constitution":
                self.constitution += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            elif choice == "intelligence":
                self.intelligence += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            elif choice == "wisdom":
                self.wisdom += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            elif choice == "charisma":
                self.charisma += 1
                self.level += 1
                self.neededexp = self.neededexp * 3
            else:
                print("Impossible to level " + choice + " due to it not existing.")
        else:
            print("Impossible to level " + choice + " due to not having enough exp.")


class Enemy:
    death = False

    def __init__(self, enemyname, armourclass, tohit, diecount, hitdie, extradmg, hitpoints, rewards):
        self.name = enemyname
        self.ac = armourclass
        self.hitbonus = tohit
        self.diecount = diecount
        self.diesize = hitdie
        self.damagebonus = extradmg
        if isinstance(hitpoints, str):
            if '+' in hitpoints:
                dice = hitpoints.split('+')
                plusnr = numbers[1]
            else:
                dice = hitpoints
                plusnr = 0
            dice = dice.split('d')
            self.hp = roll(int(dice[0]), int(dice[1]), int(plusnr))
        else:
            self.hp = hitpoints
        self.rewards = rewards

    def attack(self, playerac):
        tohitroll = roll(1, 20, self.hitbonus)
        damageroll = 0
        if tohitroll > playerac:
            damageroll = roll(self.diecount, self.diesize, self.damagebonus)
            print("Hit! You got " + str(damageroll) + " damage!")
        return damageroll

    def defend(self, playertohit, playerdamage):
        if playertohit > self.ac:
            self.hp - playerdamage
            print(self.hp)
            print("Hit! You did " + str(playerdamage) + " damage!")
            if self.hp <= 0:
                self.death = True
                print("This enemy is now dead")
        return self.death


#very simple class which stores information about an item
class Item:
    def __init__(self, iname, itype):
        self.name = iname
        if iname[:2] == "ac":
            self.itemtype = "armour"
            self.armourclass = int(iname[2:])
        elif iname[:3] == "wpn":
            self.itemtype = "weapon"
            dice = itype.split('d')
            self.diecount = int(dice[0])
            self.hitdie = int(dice[1])
        elif iname[:3] = "key":
            self.itemname = "key"
            self.location = iname[3:]
        else:
            self.itemtype = itype

#wn = input("Which world do I load in? ").lower()
wn = "dsr"
#pn = input("Name your player: ")
pn = "John Darksoul"
os.system("cls")
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
