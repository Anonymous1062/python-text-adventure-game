import os

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
