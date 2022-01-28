import os
from world import *
from player import *

#this class is used to control the menu and player inputs
class Controller:

    def __init__(self, worldname, playername):
        self.world = World(worldname)
        self.player = Player(playername)

    def play_game(self):
        self.world.create_world() #reads from file
        firstRoom = self.world.first_room()
        self.player.set_current_room(firstRoom)
        #checks if 3 items with itemtype 'victory' are in inventory
        while self.player.check_victory() != 3:
            self.player.playerstats.level_up()
            self.player.currentRoom.describe()
            print("Possible actions: move, pick up, inventory, equip")
            playerInput = input("What do you do? ").lower()
            if playerInput == "move":
                if self.movePlayer():
                    break
            elif playerInput == "pick up":
                self.take_item()
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
            if self.player.currentRoom.checkpoint:
                self.player.currentHP = self.player.maxHP

        if self.player.check_victory() == 3:
            print("Well done " + self.player.playername + ", you have beaten the game.")

    def movePlayer(self):
        moveLoc = input("Which room do you move to? ")
        changed = False
        for room in self.world.rooms:
            if moveLoc == room.name:
                #so you'll move to a room, instead of a string with the same name as the room
                moveTo = room
                self.player.goto_room(moveTo)
                os.system("cls")
                if self.player.currentRoom.boss != False:
                    death = self.combat(True)
                    if death:
                        return True
                    for finalWords in self.player.currentRoom.boss.deathlines:
                        print(self.player.currentRoom.boss.name + ": " + finalWords)
                    self.player.currentRoom.boss = False
                elif len(self.player.currentRoom.enemies) != 0:
                    death = self.combat(False)
                    if death:
                        return True
                changed = True
        if changed == False:
            print("Room not found\n")

    def take_item(self):
        itemChoice = input("Which item do you pick up? ").lower()
        os.system("cls")
        self.player.pick_up(itemChoice)
        if self.player.inventory[-1].itemtype == "key": #newest item
            for room in self.world.rooms:
                if room.name == self.player.inventory[-1].entrance:
                    room.exits.append(self.player.inventory[-1].exit)
                elif room.name == self.player.inventory[-1].exit:
                    room.exits.append(self.player.inventory[-1].entrance)


    def combat(self, activeBoss):
        combatrewards = []
        print("Combat has been initiated.")
        if activeBoss:
            self.player.currentRoom.boss.start_fight()
            #so there's no new function needed for bosses
            self.player.currentRoom.enemies.append(self.player.currentRoom.boss)
        enemycount = len(self.player.currentRoom.enemies)
        while enemycount > 0:
            for i in range(enemycount):
                print("Enemy " + str(i + 1) + ": " + self.player.currentRoom.enemies[i].name)
            selectedEnemy = int(input("Give the number of the enemy you want to attack: "))
            if selectedEnemy <= enemycount:
                playerhit, playerdmg = self.player.attack()
                #will return True if the enemy is dead
                enemystatus = self.player.currentRoom.enemies[selectedEnemy - 1].defend(playerhit, playerdmg)
                if enemystatus:
                    combatrewards += self.player.currentRoom.enemies[selectedEnemy - 1].rewards
                    self.player.currentRoom.enemies.pop(selectedEnemy - 1)
                    enemycount -= 1
            else:
                continue
            if self.enemy_attack(enemycount):
                return True
        for reward in combatrewards:
            #no other rewards implemented, but leaving the possibility open
            if reward[:2] == "xp":
                self.player.playerstats.exp += int(reward[2:])

    def enemy_attack(self, enemycount):
        for i in range(enemycount):
            print("Enemy " + str(i + 1) + " attacks...")
            enemydamage = self.player.currentRoom.enemies[i].attack(self.player.armourclass)
            if enemydamage > 0:
                self.player.currentHP -= enemydamage
                print("You currently have " + str(self.player.currentHP) + "/" + str(self.player.maxHP) + " HP")
                if self.player.currentHP <= 0:
                    print("YOU DIED")
                    return True
