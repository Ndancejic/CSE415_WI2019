# Varun Venkatesh
# AI ChatBox
# HW Assignment 1 Part B

from re import *
import random

old_statements = [];
number_of_entries = 0;
is_grumpy = False;
count = 0;



def Carl():
    'Carl is the chatbox agent and this is the top level function which contains the main loop'
    print(introduce())

    while True:
        the_input = input('TYPE HERE:>> ')
        if match('bye', the_input) or match('adios', the_input):
            return "Thanks for stopping bye - I'll send you back to your time now!"

        old_statements.append(the_input)
        global number_of_entries
        number_of_entries += 1

        print(respond(the_input))


def introduce():
    return "Hello! My name is Carl and I am a historian from the future." +\
            " Welcome to the future - what question(s) do you have?" +\
            " Also, if you wish to leave my office and travel back to your time, please just" + \
           " tell me 'bye' or 'adios'! If you have any issues, please contact my boss, Varun Venkatesh, at varunv97@uw.edu"


def agentName():
    return "Carl"

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return (w in ['do','can','should','would'])

PUNTS = ["I need more information otherwise I cannot help you.",
         "... Why would you say that?",
         "Can you elaborate a little more?",
         "Why do you want to know about that"
         ]

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return (PUNTS[punt_count % 4])

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add', 'sleep', 'fight'])



def respond(the_input):
    global number_of_entries
    global is_grumpy
    global count

    wordlist = split(' ', remove_punctuation(the_input))
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    # empty response
    if (wordlist[0] == ''):
        return "I can't help you if you don't say anything! Please ask me a question"
    # some sort of greeting
    if wordlist[0] == 'hello' or wordlist[0] == "hi" or wordlist[0] == "hey" or wordlist[0] == "yo":
        if (count % 3 == 0):
            return "Hey!"
        elif (count % 3 == 1):
            return "What's up! Do you have a question?"
        else:
            return "Come on - you are in the future and all you say is " + stringify(wordlist[0])
        count += 1

    if wordlist[0:2] == ["whats", "up"]:
        count += 1
        return "Nothing much - whats up with you?"
    # starts with "I am"
    if wordlist[0:2] == ['i', 'am']:
        return "Good to know that - could you tell more about why you are " + stringify(mapped_wordlist[2:]) + " so that I can better help you"
    # starts with "I want"
    if wordlist[0:2] == ['i', 'want']:
        count += 1
        if (count % 3 == 0):
            return "From my records I can see that you will get " + stringify(mapped_wordlist[2:])
        elif (count % 3 == 1):
            return "If you keep asking for " + stringify(mapped_wordlist[2:]) + ", I will personally make sure you" +\
                   " don't get it"
        else:
            return "Oh man from my records I can ... wait I am getting a match regarding your question: " +\
                   stringify(old_statements[random.randint(1, int(len(old_statements)))]) +\
                    ". Do you have any more questions regarding that topic?"
    # starts with "will i"
    if wordlist[0:2] == ['will', 'i']:
        return "From my records I can see that you will " + stringify(mapped_wordlist[2:])
    # starts with "what is"
    if wordlist[0:2] == ["what", "is"]:
        return "Hmmm... I will need to look into my records to find out more about " + stringify(mapped_wordlist[2:])
    # implements randomness
    if (number_of_entries > 5) and (number_of_entries % 8 == 0):
        randNum = random.randint(1, int(len(old_statements)))
        return "Hey! We got a match from our records regarding your question: " +\
               old_statements[randNum] +\
               ". Could you be more specific as to what exactly you want to know?"
    if 'coffee' in wordlist:
        return "Unfortunately, no one drinks coffee in my time - we only drink almond milk now" +\
               ". Do you have any other questions that will not depress you?"

    if wordlist[0:2] == ["where", "is"]:
        return "Let me search for that now - the world is a big place you know and since we inhabit mars in " +\
               "2098, it becomes even larger. This may take a while - do you have any other questions in the " +\
               "meantime?"

    if wordlist[0:2] == ["why", "is"]:
        return "Honestly, only one being can answer why " + stringify(mapped_wordlist[2:]) + " and that's the " +\
               "big man himself - Lebron James"

    if wordlist[0:2] == ["when", "is"]:
        randNum = random.randint(1, 6)
        if (randNum % 5 == 1):
            return "I have no idea - I am stil learning how to use this machine. I will ask my boss and get " +\
                   "back to you tomorrow! Do you have any other questions?"
        elif (randNum % 5 == 2):
            return "Why would you ask me " + stringify(mapped_wordlist[2:]) + "... That sort if question is taboo now"
        elif (randNum % 5 == 3):
            return "I do know when "  + stringify(mapped_wordlist[2:]) + "... it is on 1/12/2029"
        elif (randNum % 5 == 4):
            return "Hmmm nothing seems to be showing? Can you rephrase that?"
        else:
            return "I don' even know what that is. Be more specific please"

    if 'future' in wordlist:
        return "Honestly, I can't answer that - It's my first day on the job and my first time out of my house " +\
               "in almost two months"
    if 'love' in wordlist:
        if (not is_grumpy):
            is_grumpy = not is_grumpy
            return "Don't worry about love. We have an app for that now"
        else:
            is_grumpy = not is_grumpy
            return "Is love real? Will my ex take me back? Let's not talk about anything relating to love please"

    if 'fact' in wordlist:
        is_grumpy = not is_grumpy
        if (is_grumpy):
            return "Here's a random fact: In 2056, the world's coffee supply will run dry due to contamination from the almond industry"
        else:
            return "In 2032, President Kim Kardashian signed the 'Instagram tax act' which gave tax cuts to instagram" +\
                   " users with over 10 million followers"

    if wordlist[0:2] == ["tell", "me"]:
        return "Why do you want to know about " + stringify(mapped_wordlist[2:])

    if wordlist[0:2] == ["can", "you"]:
        if (number_of_entries % 3 == 0):
            return "I can do that! It is one of my very few and rare talents"
        elif (number_of_entries % 3 == 1):
            return "Unfortunately, I can not do that - I should probably learn how to " + stringify(mapped_wordlist[2:]) +\
                   " shouldn't I?"
        else:
            return "Why would you ask me if I can " + stringify(mapped_wordlist[2:]) + "... Why are you so rude?"

    if 'almond'  in wordlist or 'almonds' in wordlist or 'milk' in wordlist:
        return "I just realized I am very thirsty and want some almond milk! Be right back!"

    if 'no' in wordlist:
        return "You should be more accepting. People here in the future accept everything!"

    if 'war' in wordlist:
        return "Hmmmm... I'm not sure about " + stringify(mapped_wordlist) + ", but the last war I know about is " +\
               "the great war between Switzerland and Iceland"

    if 'remember' in wordlist:
        randNum = random.randint(1, int(len(old_statements)))
        if (number_of_entries % 3 == 0):
            is_grumpy = not is_grumpy
        if (is_grumpy):
            return "No, but I do remember you asking" + stringify(old_statements[randNum]) + ". Why would you ask that?"
        else:
            return "I do remember that! That was fun!"


    return punt()


# LAUNCH PROGRAM
if __name__ == "__main__":
    Carl()


