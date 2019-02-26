def mystery_code(message):
    mystring = ""
    for character in message:
        if(character.isalpha()):
            if(character.islower()):
                mystring += chr(((ord(character)-32 + 19)-65)%26 + 65)
            if(character.isupper()):
                mystring += chr(((ord(character)+32 + 19)-97)%26 + 97)
        else:
             mystring += character
    print(mystring)

class letters:
    vowels = [a, e, i, o, u]
    def __init__(self, char):
        self.char = char
    def isletter(self, char):
        return self.char == char
    def isvowel(self)
        return self.char in vowels
    def isvowel(self, char)
        return char in vowels
        
def past_tense(mylist):
    listout = []
    for strings in mylist:
        length = len(mylist)
        letter = letters(strings[length-1])
        if letter.isletter('e'):
            listout.append(strings + "d")
        elif letter.isletter('y'):
            listout.append(strings[:length -2] + "ied")
        elif letter.isvowel() and not isvowel(strings[length-2])
            listout.append(strings[:length -2] + "ied")
        else:
