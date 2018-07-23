import time
from playsound import playsound

def initialize():
    print("\nLighting up the Snake Rotation...\n")

    groupSize = input("How many people in your group? Enter a number: ")

    while not isinstance(groupSize, int):
        try:
            groupSize = int(groupSize)
        except ValueError:
            groupSize = input("Invalid input! Enter # of people in group: ")

    group = {}

    for i in range(groupSize):
        name = input("Please enter name " + str(i+1) + ": ")
        while not isinstance(name, str):
            try:
                name = str(name)
            except ValueError:
                name = input("Invalid input! Enter name " + str(i+1) + ": ")
        print("You entered: '" + name + "'")
        group[name] = 0

    return group

def session(peopleMap, person):

    print("It's " + person + "'s turn")

    countdown(10)

    prompt = "'q' to quit. 'p' for progress.\n"
    validInput = False

    while not validInput:
        state = input(prompt)
        if state == 'q':
            print("Quitting...")
            return True
        elif state == 'p':
            print("\nCurrent Progress: ")
            print(peopleMap)
        else:
            validInput = True


    incrementedCount = peopleMap.get(person, 0) + 1
    print(person + " has taken " + str(incrementedCount) + " hit(s)")
    peopleMap[person] = incrementedCount

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

    print("Session result: ")
    print(peopleMap)
    print("See you soon!")