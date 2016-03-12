import sys
from darkscape_transfer_skills import Runescaper, Skill
from darkscape_transfer_ui import Ui_DarkscapeTransferWindow
from PyQt5.QtCore import Qt, QRegExp, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class DarkscapeUI(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.ui = Ui_DarkscapeTransferWindow()
        self.ui.setupUi(self)    
        self.skill_ui = {
            "attack" : self.ui.attack_level,
            "strength" : self.ui.strength_level,
            "defence" : self.ui.defence_level,
            "ranged" : self.ui.range_level,
            "prayer" : self.ui.prayer_level,
            "magic" : self.ui.magic_level,
            "runecrafting" : self.ui.runecrafting_level,
            "construction" : self.ui.construction_level,
            "dungeoneering" : self.ui.dungeoneering_level,
            "constitution" : self.ui.constitution_level,
            "agility" : self.ui.agility_level,
            "herblore" : self.ui.herblore_level,
            "thieving" : self.ui.thieving_level,
            "crafting" : self.ui.crafting_level,
            "fletching" : self.ui.fletching_level,
            "slayer" : self.ui.slayer_level,
            "hunter" : self.ui.hunter_level,
            "divination" : self.ui.divination_level,
            "mining" : self.ui.mining_level,
            "smithing" : self.ui.smithing_level,
            "fishing" : self.ui.fishing_level,
            "cooking" : self.ui.cooking_level,
            "firemaking" : self.ui.firemaking_level,
            "woodcutting" : self.ui.woodcutting_level,
            "farming" : self.ui.farming_level,
            "summoning" : self.ui.summoning_level
        }
        self.init_validators()
        self.ui.action_about.triggered.connect(self.about_event)
        self.ui.action_exit.triggered.connect(QCoreApplication.instance().quit)
        self.ui.get_stats_button.clicked.connect(self.get_stats)
        self.ui.rs3_name.returnPressed.connect(self.get_stats)
        self.show()
    def init_validators(self):
        regex = QRegExp('^[1-9][0-9]$')
        self.skill_validator = QRegExpValidator(regex)
        for skill, ui_level in self.skill_ui.items():
            ui_level.setValidator(self.skill_validator)
        regex = QRegExp('[0-9a-zA-Z\s]+')
        self.name_validator = QRegExpValidator(regex)
        self.ui.rs3_name.setValidator(self.name_validator)

    def about_event(self):
        QMessageBox.about(
            self,
            "About",
            "Made by Brbwipe for the rsdarkscape subreddit"
        )

    def get_level(self, skill):
        this_skill = self.skill_dictionary[skill]
        return this_skill.text

    def get_stats(self):
        rs3_name = self.ui.rs3_name.text()
        runescaper = Runescaper(rs3_name)
        skills_dict = {}
        for skill, ui_level in self.skill_ui.items():
            skill_level = ui_level.text() if ui_level.text() else "1"
            skills_dict[skill] = int(skill_level)
        runescaper.add_skill_dict(skills_dict)
        QMessageBox.about(
            self,
            "Your Stats",
            str(runescaper)
        )
        
app = QApplication(sys.argv)
window = DarkscapeUI()
sys.exit(app.exec_())
