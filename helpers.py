import string

ALPHA = list(string.ascii_letters)
NUM = list(string.digits)
NEWLINE = ["\n"]
COMMA = [","]
DASH = ["-"]
SPACE = [" "]
SYMBOL = ['[', ']', '(', ')', '*']


# Reads the file until it finds a matching character (or end of file), then returns everything read EXCEPT the match
# If skipOver is false, sets the cursor to just before the matching character. Otherwise sets it after
def readUntil(inFile, matches, skipOver=False):
    retStr = ""
    while True:
        position = inFile.tell()
        char = inFile.read(1)
        if char in matches:
            if not skipOver:
                inFile.seek(position, 0)  # We don't want to go past the ending char, so go back
            return retStr
        elif char == "":
            return retStr
        else:
            retStr += char  # Add each character that isn't the ending char


# Looks at the next character(s) and returns them without moving the cursor
def peek(inFile, length=1):
    position = inFile.tell()
    stuff = inFile.read(length)
    inFile.seek(position, 0)
    return stuff


# Skips over all comments to get to content. Returns 1 on success, 0 on end of file
def skip(inFile):
    while True:
        position = inFile.tell()
        char = inFile.read(1)
        match char:
            case '#':
                # Found a comment, skip to the next line
                inFile.readline()
            case '\n':
                # Just a blank line, do nothing
                pass
            case '':
                # Found end of file, return 0
                return 0
            case _:
                # Found valid text, go back to previous position so the caller can read it
                inFile.seek(position, 0)
                return 1


# Starts at where the first line of rules text should be. Returns and array of each rules text line.
# Ends with the cursor two lines down from the last rules text line
def getRulesText(inFile):
    rules = []
    while True:
        position = inFile.tell()
        line = readUntil(inFile, NEWLINE, False)

        if line != "" and line[0] in ALPHA + SYMBOL:
            # Found a line of rules text, add it and move down 2 lines for the next line
            rules.append(line)
            inFile.readline()
            inFile.readline()
        else:
            # No more rules text, go back and return all found lines
            inFile.seek(position, 0)
            return rules


# Very similar to getRulesText, but works with 1 line gaps instead of 2, returns a single
# string instead of an array, and returns None if no flavor text. Ends with cursor one line below last line
def getFlavorText(inFile):
    flavor = ''
    while True:
        position = inFile.tell()
        line = inFile.readline()

        if line != "" and line[0] == '"':
            # Found a line of flavor text, add it
            flavor += line
        else:
            # No more flavor text, return all found lines.
            if flavor == '':
                inFile.seek(position, 0)  # We want to end 2 lines below the last flavor line, usually we don't need to
                # seek back. But if there are no flavor lines, we want to stay where we are
                return None
            return flavor[:-1]  # Shave off last '\n'. This will delete the last character if the file ends without
            # a newline, so make sure to end each input file with a newline, maybe a few comments at the bottom idk
