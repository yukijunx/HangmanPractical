"""
  Project: Text-Based Hangman
  Author: Xuechun Xin
  Date: XX XXX XXXX
  Description: Hangman game that reads in a list of words from a text file and randomly selects one to be the secret word for the user to guess.
"""
import csv
import json
import random # Import Python's module for pseudo-random number generators.
from art import LOGO, STAGES, NOOSE, CELEBRATION, Text
# 🚨 Don't change the code above. 👆
# But obviously you can change the header comment.

def main():
  """
    Contains the main logic of the Hangman game.
  """
  print(LOGO)
  # main() serves as the starting point for program execution. 
  # It usually controls program execution by directing 
  # the calls to other procedures in the program.
  print("Press enter to start a new game, press space and enter to end the game.")
  while True:
    userInput=input()
    if userInput=="":
      startPlay()
      break
    elif userInput==" ":
      exit()
    else:
      print("Please press either enter or space followed by enter to start or end the game.")

def findMaxMinLen():
  """
    Find the maximum and minimum word length of the words in the word list, as a list.
  """
  wordLenList=[]
  with open("word_list.txt") as file:
    for line in file:
      wordLenList.append(len(line))
  return [max(wordLenList),min(wordLenList)]

def pickWord(minLen):
  """
    Given the desired minimum length of the word, 
    randomly pick a word as correct answer from the work list.
  """
  wordList=[]
  with open("word_list.txt") as file:
    for line in file:
      wordList.append(line)
  while True:
    answerIndex=random.randint(0,len(wordList)-1)
    if len(wordList[answerIndex])>=minLen:
      break
  return wordList[answerIndex]

def findChar(char,answer):
  """
    Given the character and a word, 
    return all the indices of the character in the word, or -1 if it does not exist.
  """
  indexList=[]
  for i in range(0,len(answer)):
    if char==answer[i]:
      indexList.append(i)
  if indexList==[]:
    return -1
  else:
    return indexList

def loadDefaultSettings():
  """
    Return the default settings in settings.json
  """
  # Be aware that I have made changes to settings.json
  # to be specific, added a key of lower limit (of word length)
  with open('settings.json') as settings_file:
    return json.load(settings_file)

def showSettings(settings):
  """
    Show the current settings.
  """
  print("The current settings are:")
  for key, value in settings.items():
    print(key, ": ", value)

def askSettings():
  """
    Take an answer of "y" or "n" to change settings and return it.
  """
  print("Do you want to change the default settings? (Y/N)")
  while True:
    respond=input()
    if respond.strip().lower()=="y" or respond.strip().lower()=="n":
      break
    else:
      print("Please enter 'Y' or 'N'.")
  return respond

def changeSettings(maxMinLen):
  """
    Create and return a new dictionary of settings.
  """
  settings={}
  print("Please give me the cheat code: ")
  newCheatCode=input()
  settings["CHEAT_CODE"]=newCheatCode
  print("Please give me the initial number of lives (ranging from 1 to 9): ")
  while True:
    newLife=input()
    if newLife.isnumeric() and int(newLife)>=1 and int(newLife)<=9:
      newLife=int(newLife)
      break
  settings["STARTING_LIVES"]=newLife
  print("Please give me the lower limit of the word length (ranging from %d to %d): " % (maxMinLen[1],maxMinLen[0]))
  while True:
    newLowerLimit=input()
    if newLowerLimit.isnumeric() and int(newLowerLimit)>=maxMinLen[1] and int(newLowerLimit)<=maxMinLen[0]:
      newLowerLimit=int(newLowerLimit)
      break
  settings["LOWER_LIMIT"]=newLowerLimit
  return settings

def getUnderline(len):
  """
    Given the length of a word, generate corresponding underlines.
  """
  underline=""
  for i in range(0,len):
    underline+="_ "
  return underline

def startPlay():
  """
    Start a one player game.
  """
  # Settings
  settings=loadDefaultSettings()
  # Command off to show settings
  # showSettings(settings)
  respond = askSettings()
  if respond=="y":
    settings=changeSettings(findMaxMinLen())
  # Answer
  answer=pickWord(settings["LOWER_LIMIT"]).strip().lower()
  # State
  state={}
  state["stateLife"]=settings["STARTING_LIVES"]
  state["stateUnderline"]=getUnderline(len(answer))
  state["stateGuessed"]=[]
  # Main Process
  while True:
    if state["stateUnderline"].replace(' ','').lower()==answer:
      print(CELEBRATION)
      print("You won! The word is %s!" % (answer))
      break
    if state["stateLife"]<=0:
      print(NOOSE)
      print("The word is %s." % (answer))
      break
    print("====================================================")
    print("Remaining Lives: %d" %(state["stateLife"]))
    print("I'm thinking a word of %d letters long:"  %(len(answer)) , state["stateUnderline"])
    print(STAGES[state["stateLife"]-1])
    print("Guess a letter:")
    guess=input()
    # When user gives cheatcode, show the answer and keep asking for guess.
    if guess==settings["CHEAT_CODE"]:
      print("The answer is %s." %(answer))
    # When user gives a single character guess
    elif len(guess)==1:
      # When they have already guessed it
      if findChar(guess,state["stateGuessed"])!=-1:
        print("You have already guessed that letter.")
      # When they have not guess it
      else:
        state["stateGuessed"].append(guess)
        guessIndices=findChar(guess,answer)
        # When the guess is not right
        if guessIndices==-1:
          print("%s is not in the word, you lose a life." % (guess))
          state["stateLife"]-=1
        # When the guess is right
        else:
          underlineList=list(state["stateUnderline"])
          for i in guessIndices:
            underlineList[2*i]=guess
          state["stateUnderline"]="".join(underlineList)
    # When user enters other things
    else:
      print("Please guess a letter.")
  # When a game has finished
  print("====================================================")
  print("====================================================")
  print("Do you want to start a new game? (Y/N)")
  while True:
    playAgain=input()
    if playAgain.strip().lower()=="n":
      main()
      break
    if playAgain.strip().lower()=="y":
      startPlay()
      break

# 🚨 Don't change the code below. 👇
if __name__ == "__main__":
  main() # Call the main function to start the program if this file is initially ran.