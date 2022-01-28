import os

class Stats:
    level = 1
    exp = 0
    neededexp = 300
    strength = 10
    dexterity = 10
    constitution = 10

    #unused stats, which also makes character creation unbalanced for now, so they're not used outside of this class.
    intelligence = 10
    wisdom = 10
    charisma = 10

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
        while (str + dex + con + intel + wis + cha) != 27:
            print("Divide 27 points among the 6 stats: ")
            str = int(input("Strength: "))
            dex = int(input("Dexterity: "))
            con = int(input("Constitution: "))
            intel = int(input("Intelligence: "))
            wis = int(input("Wisdom: "))
            cha = int(input("Charisma: "))
            if (str + dex + con + intel + wis + cha) != 27:
                os.system("cls")
                print("Total does not equal 27")
        self.strength += str
        self.dexterity += dex
        self.constitution += con
        self.intelligence += intel
        self.wisdom += wis
        self.charisma += cha

    def level_up(self):
        if self.exp >= self.neededexp:
            choice = input("Level up!\n Choose your stat to level up: ").lower()
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
