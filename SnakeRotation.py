import time
import sys
import select
import glob
import os
#from playsound import playsound

class Person:
    """Keeps track of a person's lifetime stats"""
    name = ""
    ripcount = 0
    seshcount = 0
    ripsThisSesh = 0

def initialize():
    print("\nLighting up the Snake Rotation...\n")

    groupSize = input("How many people in your group? Enter a number: ")

    while not isinstance(groupSize, int):
        try:
            groupSize = int(groupSize)
        except ValueError:
            groupSize = input("Invalid input! Enter # of people in group: ")

    group = {}
    
    i = 0
    
    for i in range(groupSize):
        prof = Person()
        print("User profiles: \n")
        profiles = glob.glob("*.thc")
        for file in profiles:
            print(file.rstrip(".thc") + "\n")
        name = input("Enter a name to create a profile or load from the profiles above\n")
        while not isinstance(name, str):
            try:
                name = str(name)
            except ValueError:
                name = input("Invalid input! Enter name " + str(i+1) + ": ")
        if ((name + ".thc") in profiles): #check to see if user is selecting a profile
            #load profile info into person class
            userProfile = open(name+".thc", "r")
            userData = userProfile.readlines()
            prof.name = userData[0][6:].rstrip() #data
            prof.ripcount = int(userData[1][15:].rstrip())#data
            prof.seshcount = int(userData[2][12:].rstrip()) #data
            print("You selected profile: " + prof.name + "\n")
            userProfile.close()
        else:
            print("You entered: '" + name + "'! Creating profile...")
            prof.name = name
            newProfile = open(name+".thc", "w+")
            newProfile.write("Name: " + name + "\r\n")
            newProfile.write("Lifetime Rips: 0\r\n")
            newProfile.write("Sesh count: 0\r\n")
        group[name] = prof

    return group

def printRipStatus(peopleMap):
    for person in peopleMap:
        print(person + " has taken " + str(peopleMap[person].ripsThisSesh) + " rips\n")

def session(peopleMap, person):

    print("It's " + person + "'s turn")

    countdown(10)

    prompt = "'q' to quit. 'p' for progress. 's' for lifetime stats\n"
    validInput = False

    while not validInput:
        state = input(prompt)
        if state == 'q':
            print("Quitting...")
            return True
        elif state == 'p':
            print("\nCurrent Progress: ")
            printRipStatus(peopleMap)
        elif state == 's':
            print(person + "'s Stats: \n")
            print("Rips this sesh: " + str(peopleMap[person].ripsThisSesh) + "\n")
            print("Total Rips: " + str(peopleMap[person].ripcount) + "\n")
            print("Sesh count: " + str(peopleMap[person].seshcount) + "\n")
        else:
            validInput = True


    incrementedCount = peopleMap[person].ripsThisSesh + 1
    print(person + " has taken " + str(incrementedCount) + " hit(s)")
    peopleMap[person].ripsThisSesh = incrementedCount
    peopleMap[person].ripcount = peopleMap[person].ripcount + 1

    return False


def countdown(seconds):
    while seconds > 0:
        print (seconds)
        time.sleep(1)
        seconds = seconds - 1
        i, o, e = select.select([sys.stdin], [], [], 0.0001)
        if i == [sys.stdin]: break

    if seconds == 0:
        #playsound('audio.mp3')
        print ("PASS NOW!")


if __name__ == '__main__':
    peopleMap = initialize()

    instructions = "\nPress 'q' to quit\n" + \
                   "Press 'enter' to continue.\n"

    print(instructions)

    sessionOver = False
    while not sessionOver:
        for person in peopleMap:
            sessionOver = session(peopleMap, person)
            if sessionOver:
                break

    #update user profiles with new stats
    for person in peopleMap:
        userProfile = open(peopleMap[person].name + ".thc", "+w")
        userProfile.write("Name: " + peopleMap[person].name + "\r\n")
        userProfile.write("Lifetime Rips: " + str(peopleMap[person].ripcount) + "\r\n")
        userProfile.write("Sesh count: " + str(peopleMap[person].seshcount+1) + "\r\n")
        userProfile.close()

    print("Session result: ")
    printRipStatus(peopleMap)
    print("See you soon!")