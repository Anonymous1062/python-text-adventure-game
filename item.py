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
