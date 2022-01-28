import random

#to roll a dice to see if you hit, how much damage you do, or other things. 2d20 + 5 is a = 2, b = 20, c = 5
#I wouldn't use a global function, but this is just much more efficient considering I use it in multiple functions
def roll(a, b, c):
    #ik zet het allemaal nog een keer om in ints, ook al had het dat al moeten zijn, omdat het alsnog een error gaf
    a = int(a)
    b = int(b)
    c = int(c)
    print(str(a) + "d" + str(b) + " + " + str(c))
    rolls = c
    for i in range(a):
        diceroll = random.randint(1, b)
        rolls += diceroll
        print("rolls: " + str(rolls))
    return int(rolls)

def split_dice(diceString):
    if '+' in diceString:
        dice = diceString.split('+')
        plusnr = dice[1]
        dice = dice[0].split('d')
    else:
        dice = diceString
        plusnr = 0
        dice = dice.split('d')
    return dice, plusnr
