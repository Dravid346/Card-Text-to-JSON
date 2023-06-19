import helpers

# The code for reading card for my card game "Braithia". When written in text, the cards are formatted like so:
# [NAME]
# [MANA COST]
# [TYPE 1] [TYPE 2] - [SUBTYPE 1] [SUBTYPE 2] (if no subtypes, remove the "-")
#
# [RULES TEXT 1] (activated abilities' mana costs must be wrapped in square brackets or parentheses to be differentiated
# from power/toughness)
#
# [RULES TEXT 2]
#
# "[FLAVOR TEXT 1]"
# "[FLAVOR TEXT 2]"
#
# [POWER]/[TOUGHNESS]
#
# Between each card is at least 2 empty lines, and comments can be made between cards
# by starting a line with #. The code has some leniency in certain places, but for the most part requires that the
# input file be formatted exactly like this. See magic_input.txt for an example. In object form, the cards have all of
# the properties in magicCard, even nonexistent ones like cards that lack flavor text or sorcery cards lacking
# power and toughness. Nonexistent properties are left at their default values.


class magicCard:
    def __init__(self):
        self.name = ""
        self.cost = ""
        self.types = []
        self.subtypes = []
        self.rulesText = []
        self.flavorText = None
        self.power = None
        self.toughness = None


def magicRead(inFile):
    cardList = []
    endOfFile = False
    helpers.skip(inFile)  # Get to start of first card
    while not endOfFile:
        print("Magic starting loop")
        card = magicCard()

        card.name = helpers.readUntil(inFile, helpers.NEWLINE, True)
        print(f"Got card name: {card.name}")

        card.cost = helpers.readUntil(inFile, helpers.NEWLINE, True)
        print(f"Got card cost: {card.cost}")

        exitChar = "lol"
        while exitChar not in "-\n" and exitChar != "":
            card.types.append(helpers.readUntil(inFile, helpers.SPACE+helpers.NEWLINE, True))

            # We skip the space/newline after each type, so we can end by finding either the dash that signals
            # subtypes, or the blank line between types and rules text
            exitChar = helpers.peek(inFile)

        if exitChar == '-':
            inFile.read(2)  # Get past the '- ' to reach first subtype
            # We skip the space/newline after each type, so if we find the blank line between types and rules text, end
            while helpers.peek(inFile) != '\n':
                card.subtypes.append(helpers.readUntil(inFile, helpers.SPACE+helpers.NEWLINE, True))

        # The number of rules text lines and flavor text lines are variable-length, in different ways
        # There's two blank lines between types and rules, and we exit the typeline by skipping over the \n,
        # so go down one more line
        inFile.readline()

        card.rulesText = helpers.getRulesText(inFile)
        print(f"Got rules text: {card.rulesText}")
        card.flavorText = helpers.getFlavorText(inFile)
        print(f"Got flavor text: {card.flavorText}")

        # getFlavorText ends one line below

        if helpers.peek(inFile) in helpers.NUM:
            card.power = helpers.readUntil(inFile, ['/'], True)
            card.toughness = helpers.readUntil(inFile, helpers.NEWLINE, True)

        cardList.append(card.__dict__)
        print(f"Final card: {card}")

        # Go to start of next card, or end if no next card
        if helpers.skip(inFile) == 0:
            endOfFile = True

    return cardList
