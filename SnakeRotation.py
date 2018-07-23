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
    
    os.chdir("/mydir")
    
    for i in range(groupSize):
        prof = Person()
        print("User profiles: \n")
        profiles = glob.glob("*.thc")
        i = 0
        for file in profiles:
            print(str(i) + ": " + file.rstrip(".thc") + "\n")
        name = input("Enter a name to create a profile, or enter a number to load a profile from above: \n")
        while not isinstance(name, str):
            try:
                name = str(name)
            except ValueError:
                name = input("Invalid input! Enter name " + str(i+1) + ": ")
        if (int(name) < len(profiles)) and (int(name) >= 0): #check to see if user is selecting a profile
            #load profile info into person class
            userProfile = open(profiles[int(name)], "r")
            userData = userProfile.readlines()
            print("You selected profile: ")
            prof.name = userData[0][6:].rstrip() #data
            prof.ripcount = userData[1][15:].rstrip()#data
            prof.seshcount = userData[2][12:].rstrip() #data
        else:
            print("You entered: '" + name + "'! Creating profile...")
            prof.name = name
            newProfile = open(name+".thc", "w+")
            newProfile.write("Name: %s\r\n", name)
            newProfile.write("Lifetime Rips: 0\r\n")
            newProfile.write("Sesh count: 0\r\n")
        group[name] = prof

    return group

def session(peopleMap, person):

    print("It's " + person.name + "'s turn")

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
            print(peopleMap)
        elif state == 's':
            print("Stats: \n")
            print("Rips this sesh: %s", )
            print("Total Rips: %s\n", person.ripcount)
            print("Sesh count: %s\n", person.seshcount)
        else:
            validInput = True


    incrementedCount = person.ripsThisSesh + 1
    print(person.name + " has taken " + str(incrementedCount) + " hit(s)")
    person.ripsThisSesh = incrementedCount
    person.ripcount = person.ripcount + 1

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

    print("Session result: ")
    print(peopleMap)
    print("See you soon!")