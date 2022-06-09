import random

class Runa:

    runaPosition = [" ", " перевернутая"]

    #класс руна, name - название, description - описание значений, position - 0 - прямое положение, 1 перевернутое
    def __init__ (self, name, description, descriptionInverted, position, pointer, ascii):
        self.name = name
        self.description = description
        self.descriptionInverted = descriptionInverted
        self.position = random.randint(0, 1)
        if name == 'Gifu' or name == 'Hagalaz' or name == 'Nautiz' or name == 'Isa' or name == 'Jera' or name == 'Eihwaz' or name == 'Siegel' or name == 'Ingwaz' or name == 'Dagaz' or name == 'Wyrd':
            self.position = 0
        self.pointer = pointer
        self.ascii = ascii

    def __str__(self):
        if self.position==0:
            return "%s %s %s %s" % (self.name, self.ascii, self.description, "прямое положение")
        if self.position==1:
            return "%s %s %s %s" % (self.name, self.ascii, self.descriptionInverted, "перевернутое положение")
