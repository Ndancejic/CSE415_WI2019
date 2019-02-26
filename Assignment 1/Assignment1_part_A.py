import math
def five_x_cubed_plus_1(x):
    result = 5*x*x*x + 1
    print(result)

def pair_off(initial_list):
    i = 0
    new_list = []
    while i < len(initial_list)-1:
        new_list.append([initial_list[i], initial_list[i+1]])
        i = i+2
    if(i < len(initial_list)):
        new_list.append([initial_list[i]])
    print(new_list)

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

def past_tense(mylist):
    listout = []
    vowels = ['a', 'e', 'i', 'o', 'u']
    special = ['a', 'e', 'i', 'o', 'u', 'y', 'w']
    irregular = {
        "have" : "had",
        "be" : "was",
        "eat" : "ate",
        "go" : "went"
        }
    for strings in mylist:
        if strings[-1] == "e":
            listout.append(strings + "d")
        elif strings[-1] == "y" and strings[-2] not in vowels:
            listout.append(strings[:-2] + "ied")
        elif strings[-2] in vowels and strings[-3] not in vowels and strings[-1] not in special:
            listout.append(strings + strings[-1] + "ed")
        elif strings in irregular:
            listout.append(irregular[strings])
        else:
            listout.append(strings + "ed")

    print(listout)


five_x_cubed_plus_1(2)
mylist = [2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2]
pair_off(mylist)
mystery_code("abc Iz th1s Secure? n0, no, 9!")
past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat'])
