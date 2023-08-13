import asyncio
import discord
import string

client = discord.Client()
class guessing:
    def __init__(self, character, type, position): #-1 means non existent 6 means random position
        self.character = character
        self.type = type
        self.position = position
def guesser(starter,ans,listy):

    for x in range(5):
        if (ans[x] == 'g'):
            listy.append(guessing(starter[x],"green",x))
        elif(ans[x] == 'y'):
            listy.append(guessing(starter[x],"yellow", x))
        elif(ans[x] == 'r'):
            listy.append(guessing(starter[x],"red",-1))


def check(word, eliminate):
    for x in range(len(eliminate)):
        if eliminate[x].type == "red":
            if eliminate[x].character in word:
                return False
        if eliminate[x].type == "green":
            if word[eliminate[x].position] != eliminate[x].character:
                return False
        if eliminate[x].type == "yellow":
            if eliminate[x].character not in word:
                return False
            if word[eliminate[x].position] == eliminate[x].character:
                return False
    return True

def eliminate(words,eliminate):
    wording = []
    for x in range(len(words)):
        checker = check(words[x], eliminate)
        if checker == True:
            wording.append(words[x])
    return wording


def perfect_word(counter, d, list1, list2):

    for x in range(counter):
        no_double = []
        for y in range(5):
            if list1[x][y] not in no_double:
                d[list1[x][y]] += (1 / counter)
                no_double.append(list1[x][y])
    for x in d.keys():
        d[x] = abs(d[x])

    perfect_guess = ""
    least_val = 2000
    for x in range(len(list2)):
        value = 0
        no_double = []
        for y in range(5):
            if list2[x][y] not in no_double:
                value += d[list2[x][y]]
                no_double.append(list2[x][y])
            else:
                value += 0.5
        if value < least_val:
            least_val = value
            perfect_guess = list2[x]
    print(d)
    print(list1)
    print(list2)
    return perfect_guess

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.startswith('w'):
        print("hello")
    if message.content.startswith('./w'):
        await message.channel.send('Input \"salet\" in WORDLE. \nInput color code in corresponding position.'
                                   '\n\'g\' = Green \n\'y\' = Yellow \n\'r\' = Red'
                                   '\nEx: rgygr')
        def checki(ans):
            if ans.content == "./exit" or (ans.content == "./w" and ans.author == message.author) or (ans.content == "./z" and ans.author == message.author):
                return True
            if len(ans.content) != 5 or (ans.channel != message.channel):
                return False
            if ans.author != message.author:
                return False
            if ans.channel != message.channel:
                return False
            for x in range(len(ans.content)):
                if (ans.content)[x] not in "rgy":
                    return False

            return ans
        starter = "salet"
        file = open("wordle.txt", "r")
        available = []
        information = []
        for x in file:
            available.append(x.split('\n')[0])
        file.close()
        list2 = available
        prev = 0
        incrementer = 0
        while(len(available) > 1 and prev != len(available) and incrementer < 6):
            ans = await client.wait_for('message',check=checki)
            if ans.content == "./exit":
                return
            elif ans.content == "./w":
                return
            elif ans.content == "./z":
                return
            else:
                prev = len(available)
                guesser(starter, ans.content, information)
                available = eliminate(available, information)
                d = dict.fromkeys(string.ascii_lowercase, -0.5)
                starter = perfect_word(len(available), d, available, list2)
                if len(available) > 1 and prev != len(available) and incrementer < 6:
                    await message.channel.send(f"Choose word {starter}. Input color code again!")
                    if len(available) < 10:
                        await message.channel.send(f"\nIf you want to guess, Remaining words are {available}")
                else:
                    await message.channel.send(f"These should be one of your answers {available}")
                    return
                incrementer+=1
    elif message.content.startswith("./z"):
        await message.channel.send('Input \"salet\" in WORDLE. \nInput color code in corresponding position.'
                                   '\n\'g\' = Green \n\'y\' = Yellow \n\'r\' = Red'
                                   '\nEx: rgygr')
        def checki(ans):
            if ans.content == "./exit" or (ans.content == "./w" and ans.author == message.author) or (ans.content == "./z" and ans.author == message.author):
                return True
            if len(ans.content) != 5 or (ans.channel != message.channel):
                return False
            if ans.author != message.author:
                return False
            if ans.channel != message.channel:
                return False
            for x in range(len(ans.content)):
                if (ans.content)[x] not in "rgy":
                    return False

            return ans
        starter = "salet"
        file = open("answers.txt", "r")
        available = []
        information = []
        for x in file:
            available.append(x.split('\n')[0])
        file.close()
        file = open("wordle.txt", "r")
        list2 = []
        for x in file:
            list2.append(x.split('\n')[0])
        prev = 0
        incrementer = 0
        while(len(available) > 1 and prev != len(available) and incrementer < 6):
            ans = await client.wait_for('message',check=checki)
            if ans.content == "./exit":
                return
            elif ans.content == "./z":
                return
            elif ans.content == "./w":
                return
            else:
                prev = len(available)
                guesser(starter, ans.content, information)
                available = eliminate(available, information)
                d = dict.fromkeys(string.ascii_lowercase, -0.5)
                starter = perfect_word(len(available), d, available, list2)
                if len(available) > 1 and prev != len(available) and incrementer < 6:
                    await message.channel.send(f"Choose word {starter}. Input color code again!")
                    if len(available) < 10:
                        await message.channel.send(f"\nIf you want to guess, Remaining words are {available}")
                else:
                    await message.channel.send(f"These should be one of your answers {available}")
                    return
                incrementer+=1
        return