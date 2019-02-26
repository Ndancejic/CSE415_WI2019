import math
def five_x_cubed_plus_1(x):
    result = 5*x*x*x + 1
    return result

def pair_off(initial_list):
    i = 0
    new_list = []
    while i < len(initial_list)-1:
        new_list.append([initial_list[i], initial_list[i+1]])
        i = i+2
    if(i < len(initial_list)):
        new_list.append([initial_list[i]])
    return new_list

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
    return mystring

def past_tense(mylist):
    listout = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    special = ['a', 'e', 'i', 'o', 'u', 'y', 'w']
    irregular = {
        "have" : "had",
        "has" : "had",
        "am" : "was",
        "is" : "was",
        "are" : "was",
        "eat" : "ate",
        "go" : "went",
        "goes" : "went",
        }
    for strings in mylist:
        if strings in irregular:
            listout.append(irregular[strings])
        elif strings[-1] == "e":
            listout.append(strings + "d")
        elif strings[-1] == "y" and strings[-2] not in vowels:
            listout.append(strings[:-2] + "ied")
        elif strings[-2] in vowels and strings[-3] not in vowels and strings[-1] not in special:
            listout.append(strings + strings[-1] + "ed")
        else:
            listout.append(strings + "ed")

    return listout
