import random
from global_functions import *

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
