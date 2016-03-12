import requests
import math

class Runescaper:

    def __init__(self, name):
        self.name = name
        self.skills = [ Skill(x, 1, 0) for x in skill_list ]
        self.xp_table = [0]
        points = 0
        for level in range(1,99):
            diff = int(level + 300 * math.pow(2, float(level)/7) )
            points += diff
            self.xp_table.append(points/4)
        self.RS3 = self.get_RS3_stats()

    def get_RS3_stats(self):
        underscored_name = self.name.replace(" ", "_")
        r = requests.get('http://hiscore.runescape.com/index_lite.ws?player='+underscored_name)
        ranks_list = []
        rs3player = (r.status_code != 404)
        if(rs3player):
            ranks_list = r.text.split("\n")
            ranks_list = ranks_list[1:len(skill_list)+1]
            ranks_list = [stats.split(",") for stats in ranks_list]
            ranks_list = [[int(stat) for stat in stats] for stats in ranks_list]
            for val, stats in enumerate(ranks_list, start=0):
                if(stats[2] == -1):
                    stats[2] = 0
                self.change_skill_exp(skill_list[val], stats[2])
        return rs3player

    def get_level_exp(self, level):
        return self.xp_table[level-1]

    def add_skill_dict(self, dictionary, level_mode=True):
        if(level_mode): 
            for skill, level in dictionary.items():
                self.change_skill_exp(skill, (self.get_level_exp(level)/2), True)
        else:
            for skill, exp in dictionary.items():
                self.change_skill_exp(skill, exp/2, True)

    def __str__(self):
        long_string =      "===========Stats for "+self.name+"===========\n\n"
        if(self.RS3):
            long_string += "You have an RS3 account. Your exp was added.\n\n"
        else:
            long_string += "You don't have an RS3 account. \n\n"
        for skill in self.skills:
            long_string += skill.name.title()+": "+str(skill.exp)+" Experience (Level "+str(skill.level)+")\n\n"
        long_string += "Your total level will be "+str(self.total_level())+"."
        return long_string
        
    def change_skill_exp(self, skill, exp, addition=False):
        a_skill = list(filter(lambda x: x.name == skill, self.skills))
        if(a_skill):
            a_skill[0].change_exp(exp, addition)

    def total_level(self):
        total_level = 0
        for skill in self.skills:
            total_level += skill.level
        return total_level

class Skill:

    def __init__(self, name, level, exp):
        self.name = name
        self.level = level
        self.exp = int(exp)
        self.xp_table = [0]
        points = 0
        for level in range(1,99):
            diff = int(level + 300 * math.pow(2, float(level)/7) )
            points += diff
            self.xp_table.append(points/4)

    def __str__(self):
        return self.name+" Level "+str(self.level)+ " XP: "+str(self.exp)

    def change_exp(self, exp, addition=False):
        self.exp = (self.exp + exp if addition else exp)
        self.level = self.calculate_level()

    def calculate_level(self):
        level = 0
        for x in (self.xp_table):
            level = level + 1
            if(self.exp <= x):
                level = level - 1
                break
        return level

skill_list = [
    "attack",
    "defence",
    "strength",
    "constitution",
    "ranged",
    "prayer",
    "magic",
    "cooking",
    "woodcutting",
    "fletching",
    "fishing",
    "firemaking",
    "crafting",
    "smithing",
    "mining",
    "herblore",
    "agility",
    "thieving",
    "slayer",
    "farming",
    "runecrafting",
    "hunter",
    "construction",
    "summoning",
    "dungeoneering",
    "divination",
]
    
