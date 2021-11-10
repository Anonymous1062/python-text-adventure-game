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
