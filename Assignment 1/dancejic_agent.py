# dancejic_agent.py
# Adapted from Shrink3.py by Steven Tanimoto

# Nikola Dancejic

from re import *   # Loads the regular expression module.
import random

name_asked = 0
rounds = 0
question_cycle = 0
continue_cycle = 0
question_posed = 0
mem_delay = 0
name = ""
memory = ["coffee"]
def Coffee():
    print(introduce())
    while True:
        the_input = input('COMPLAINTS:>> ')
        print(respond(the_input))

def introduce():
    return ("Hi, I\'m Nick the neighborhood coffee guy \n" + 
            "I'm usually pretty cool, \nbut If I see you drinking Starbucks we can't be friends \n" +
            "dancejic@uw.edu is who to contact for complaints. \nThey go straight to my complaint bin over there in the corner")

def agentName():
    return "Nick"

def respond(the_input):
    global rounds
    global name_asked
    global memory
    global question_posed
    PUNTS = ['Well then',
         'don\'t tell me more.',
         'Well this is awkward.',
         'What does this have to do with coffee?',
         'I don\'t really care...',
         'tell me an interesting fact.',
         'what do you think about ' + random.choice(memory)]
    rounds = rounds + 1
    if match('bye',the_input):
        print('Alright, see ya.')
        return
    wordlist = split(' ',remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0]=wordlist[0].lower()
    greeting_list = ['hi', 'hello', 'hey', 'greetings']
    dont_know = ['dont', 'know', 'coffee']
    question = ['ask', 'me', 'question', 'have', 'a', 'do', 'you']
    did = ['did', 'you', 'know', 'here', 'interesting', 'fact']
    like = ['I', 'like', 'enjoy', 'love', 'hate']
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0]=mapped_wordlist[0].capitalize()
    #if someone answers my question
    if question_posed == 1:
        memory.append(' '.join(wordlist[2:]))
        question_posed = 0
        return "Tell me something that may interest me"
    #no input, respond as such
    if wordlist[0]=='':
        return("If you're just gonna stand there, let someone else order.")
    #if name question was asked, respond and use name
    if name_asked == 1:
        name = wordlist[-1]
        name_asked = 2
        return "Good to know, " + name
    #if a known greeting is used
    for items in greeting_list:
        if items in wordlist:
            return random_greeting()
    #if someone claims not to know about something
    know_count = 0
    for items in dont_know:
        if items in wordlist:
            know_count = know_count + 1
        if know_count == 2:
            return "Of course not, do you want a brochure?"
    #if some wants me to ask them a quesiton, return from a list of questions
    question_count = 0
    for items in question:
        if items in wordlist:
            question_count = question_count + 1
        if question_count == 2:
            questions_posed = 1
            return ask_question()
    #if someone tells me to to something with a verb
    if verbp(wordlist[0]):
        return "That does\'nt sounds like a very good idea."
    #if someone asks something
    if wpred(wordlist[0]):
        return wordlist[0] + " do you think?"
    #if someone asks me to remember something, I save it and use it later
    if 'remember' in wordlist:
        memory.append(wordlist[-1])
        return "I will remember that"
    #if someone answers yes
    if 'yes' in wordlist:
        return "sure thing..."
    #if someone answers no
    if 'no' in wordlist:
        return "I suppose..."
    #if someone talks to me about history
    if 'History' in wordlist:
        return "I hate History, tell me more"
    know = 0
    #if someone asks a "did you know" question I answer from a cycle of answers
    for items in did:
        if items in wordlist:
            know = know + 1
        if know == 3:
            return continue_talk()
    #if someone says they like something, I remember it and choose a random response
    numlike=0
    for items in like:
        if items in wordlist:
            numlike = numlike + 1
        if numlike == 2:
            memory.append(' '.join(wordlist[2:]))
            #i can remember subjects that were mentioned
            return random.choice(["I remember you seemed interested in " + random.choice(memory) + ", or was that me?",
                              "Good for you, I like Coffee"])
    #if it is an early round and I haven't asked for your name, I will ask
    if name_asked == 0 and rounds > 1 and rounds < 4:
        name_asked = 1
        return "What is your name?"
    #throw punts if no other choice
    return random.choice(PUNTS)

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

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]

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
                  'blink', 'crash', 'crunch', 'add'])

def random_greeting():
    'Returns a random greeting'
    greetings = ['Hi there, what kind of coffee do you like?', 'Hello, how can I help you?', 'Hi...']
    return random.choice(greetings)

def ask_question():
    'returns a question'
    global question_cycle
    questions = ["What kind of coffee will we drink in the future?", "What is your favorite fact?", "do you like mochas?",\
                 "What do you think about " + random.choice(memory)]
    question_cycle = question_cycle + 1
    return questions[question_cycle%3]

def continue_talk():
    global continue_cycle
    questions = ["Please tell more...", "I thought we were talking about coffee", "Look are you gonna order or what?"]
    question_cycle = question_cycle + 1
    return questions[question_cycle%3]

#Coffee() # Launch the program.
