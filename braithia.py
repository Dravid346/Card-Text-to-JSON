import helpers

# The code for reading card for my card game "Braithia". When written in text, the cards are formatted like so:
# [NAME]
# [TYPE], [REGION]
# Lv[LEVEL], [POWER]p or [SPELL SUBTYPE]
#
# [RULES TEXT 1]
#
# [RULES TEXT 2]
#
# "[FLAVOR TEXT 1]"
# "[FLAVOR TEXT 2]"
#
# Between each card is at least 2 empty lines, and comments can be made by starting a line with #. The code has some
# leniency in certain places, but for the most part requires that the input file be formatted exactly like this. See
# braithia_input.txt for an example. In object form, the cards have all of the properties, even nonexistent ones
# like cards that lack flavor text or monster cards lacking a spellSubType. Nonexistent properties are left at their
# default values.


class braithiaCard:
    def __init__(self):
        self.name = None
        self.type = None
        self.region = None
        self.level = None
        self.power = None
        self.spellSubType = None
        self.rulesText = []
        self.flavorText = None


def braithiaRead(inFile):
    cardList = []
    endOfFile = False
    helpers.skip(inFile)  # Get to start of first card
    while not endOfFile:
        print("Braithia starting loop")
        card = braithiaCard()

        card.name = helpers.readUntil(inFile, helpers.NEWLINE, True)
        print(f"Got card name: {card.name}")

        card.type = helpers.readUntil(inFile, helpers.COMMA, False)
        print(f"Got type: {card.type}")

        helpers.readUntil(inFile, helpers.ALPHA, False)  # Get past the comma+space
        card.region = helpers.readUntil(inFile, helpers.NEWLINE, True)
        print(f"Got region: {card.region}")

        helpers.readUntil(inFile, helpers.NUM, False)  # Skip past the "Lv"
        card.level = int(helpers.readUntil(inFile, helpers.COMMA))
        print(f"Got level: {card.level}")

        # Next part is either a monster card's power or a spell card's subtype)
        match card.type.lower():
            case "monster":
                helpers.readUntil(inFile, helpers.NUM, False)  # Get past the comma+space
                card.power = int(helpers.readUntil(inFile, helpers.ALPHA+helpers.NEWLINE, False))
                print(f"Found monster, got power: {card.power}")
            case "spell":
                helpers.readUntil(inFile, helpers.ALPHA, False)  # Get past the comma+space
                card.spellSubType = helpers.readUntil(inFile, helpers.NEWLINE, False)
                print(f"Found spell, got subtype: {card.spellSubType}")
            case _:
                print(f'Unrecognized card type: "{card.type}"')

        # The number of rules text lines and flavor text lines are variable-length, in different ways
        # Either way, need to go down two lines
        inFile.readline()
        inFile.readline()

        card.rulesText = helpers.getRulesText(inFile)
        print(f"Got rules text: {card.rulesText}")
        card.flavorText = helpers.getFlavorText(inFile)
        print(f"Got flavor text: {card.flavorText}")

        cardList.append(card.__dict__)
        print(f"Final card: {card}")

        # Go to start of next card, or end if no next card
        if helpers.skip(inFile) == 0:
            endOfFile = True

    return cardList
