from controller import *

wn = input("Which world do I load in? ").lower()
#wn = "dsr" #test world to skip this
pn = input("Name your player: ")
#pn = "John Darksoul" #test name to skip this
os.system("cls")
game = Controller(wn, pn)
game.play_game()



'''
#to roll a dice to see if you hit, how much damage you do, or other things. 2d20 + 5 is a = 2, b = 20, c = 5
#I wouldn't use a global function, but this is just much more efficient considering I use it in multiple functions
def roll(a, b, c):
    print(str(a) + "d" + str(b) + " + " + str(c))
    rolls = c
    for i in range(a):
        diceroll = random.randint(1, b)
        rolls += diceroll
        print("rolls: " + str(rolls))
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
                        death = self.combat()
                        if death:
                            break
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
        combatrewards = []
        print("Combat has been initiated.")
        enemycount = len(self.player.currentRoom.enemies)
        while enemycount > 0:
            for i in range(enemycount):
                print("Enemy " + str(i + 1) + ": " + self.player.currentRoom.enemies[i].name)
            selectedEnemy = int(input("Give the number of the enemy you want to attack: "))
            if selectedEnemy <= enemycount:
                playerhit, playerdmg = self.player.attack()
                enemystatus = self.player.currentRoom.enemies[selectedEnemy - 1].defend(playerhit, playerdmg)
                if enemystatus:
                    combatrewards += self.player.currentRoom.enemies[selectedEnemy - 1].rewards
                    self.player.currentRoom.enemies.pop(selectedEnemy - 1)
                    enemycount -= 1
            for i in range(enemycount):
                print("Enemy " + str(i + 1) + " attacks...")
                enemydamage = self.player.currentRoom.enemies[i].attack(self.player.armourclass)
                if enemydamage > 0:
                    self.player.currentHP -= enemydamage
                    print("You currently have " + str(self.player.currentHP) + "/" + str(self.player.maxHP) + " HP")
                    if self.player.currentHP <= 0:
                        print("YOU DIED")
                        return True
        for i in range(len(combatrewards)):
            if combatrewards[i][:2] == "xp":
                self.player.playerstats.exp += int(combatrewards[i][2:])

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

class Stats:
    level = 1
    exp = 0
    neededexp = 300
    strength = 8
    dexterity = 8
    constitution = 8
    intelligence = 8
    wisdom = 8
    charisma = 8

    def create_character(self):
        print("Racial options: Elf, Dwarf, Human")
        race = input("Which race would you like to be?").lower()
        if race == "elf":
            self.dexterity += 2
            self.wisdom += 2
            self.intelligence += 1
        elif race == "dwarf":
            self.constitution += 2
            self.strength += 2
            self.wisdom += 1
        elif race == "human":
            self.strength += 1
            self.dexterity += 1
            self.constitution += 1
            self.intelligence += 1
            self.wisdom += 1
        while True:
            print("Divide 27 points among the 6 stats: ")
            str = int(input("Strength: "))
            dex = int(input("Dexterity: "))
            con = int(input("Constitution: "))
            intel = int(input("Intelligence: "))
            wis = int(input("Wisdom: "))
            cha = int(input("Charisma: "))
            if (str + dex + con + intel + wis + cha) != 27:
                print("Total does not equal 27")
            else:
                self.strength += str
                self.dexterity += dex
                self.constitution += con
                self.intelligence += intel
                self.wisdom += wis
                self.charisma += cha
                break

    def level_up(self, choice):
        if exp >= neededexp:
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
            self.hp -= playerdamage
            print("Hit! You did " + str(playerdamage) + " damage!")
            if self.hp <= 0:
                self.death = True
                print("This enemy is now dead")
        return self.death

class Boss(Enemy):
    def __init__(self, enemyname, armourclass, tohit, diecount, hitdie, extradmg, hitpoints, rewards, dialogue, attacknames):
        Enemy.__init__(self, enemyname, armourclass, tohit, diecount, hitdie, extradmg, hitpoints, rewards)
        self.dialogue = dialogue
        self.attacknames = attacknames

    def start_fight(self):
        print("The door closes behind you, temporarily blocking the way out. Only your own power can save you now...")
        for i in range(len(self.dialogue)):
            print(self.dialogue[i])

    def attack(self, playerac):
        attackcount = len(self.attacknames)
        selected_attack = random.randint(0, (attackcount - 1))
        print(self.name + " attacks with " + self.attacknames[selected_attack])
        tohitroll = roll(1, 20, self.hitbonus[selected_attack])
        damageroll = 0
        if tohitroll > playerac:
            damageroll = roll(self.diecount[selected_attack], self.diesize[selected_attack], self.damagebonus[selected_attack])
            print("Hit! You got " + str(damageroll) + " damage!")
        return damageroll

#very simple class which stores information about an item
class Item:
    def __init__(self, iname, itype):
        self.name = iname
        if itype[:2] == "ac":
            self.itemtype = "armour"
            self.armourclass = int(itype[2:])
        elif itype[:3] == "wpn":
            self.itemtype = "weapon"
            weapondice = itype[3:]
            dice = weapondice.split('d')
            self.diecount = int(dice[0])
            self.hitdie = int(dice[1])
        elif itype[:3] == "key":
            self.itemname = "key"
            self.location = itype[3:]
        else:
            self.itemtype = itype
'''
