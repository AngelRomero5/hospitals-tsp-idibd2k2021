''' 
    This project was created as a sample on how to use the Google Distance Matrix API to 
    calculate the distance and time it takes to travel between two health facilities.
    Saves the info on a json file.
    @Author: Ángel G. Romero Rosario on 6/11/2021

'''
import requests

print('-' * 70)
print(" Welcome to the Google Distance Matrix API Program ")
print('-' * 70 + "\n")

input(" Press ENTER to continue : ")

''' Functions '''

# This function returns the distance between two hospitals 
def twoPointTravel(destinationsHospitals):

    found = False
    
    # While 
    while not found:
        origin = input("\n Enter origin hospital : ")
        destination = input("\n Enter destination hospital : ")

        # Go through every object in the list and search for the distance
        for e in destinationsHospitals:

            # Find the distance between the two hospitals
            if e[0] == origin and e[1] == destination:

                print('-' * 60 + "\n")
                print(" The shortest distance between " + origin + " and " + destination + " is : " + e[2])
                print("\n" + '-' * 60 + "\n")
                found = True
                break 

            if e[1] == origin and e[0] == destination:
                print('-' * 60 + "\n")
                print(" The shortest distance between " + origin + " and " + destination + " is : " + e[2])
                print("\n" + '-' * 60 + "\n")
                found = True
                break

        
        if not found:
            print("\n Error. Please enter valid locations.")
            response = input("\n Do you want me to return another distance? [Y, N] : ")
            if response == 'N' or response == 'n':
                found = True

        else:
            response = input("\n Do you want me to return another distance? [Y, N] : ")
            if response == 'Y' or response == 'y':
                found = False

# This function returns the closest hospital to the given hospital location
def closest_Hospital(destinationsHospitals):

    origin = input("\n Enter origin hospital : ")
    closest = ""
    shortest_Distance = 1000000

    # Compare distances between neighbors of a given hospital
    for hospital in destinationsHospitals:

        # If it has found the given hospital
        if hospital[0] == origin: 

            # Extract only the distance number from the string
            dis = hospital[2].split(" ", 1) 
            disNum = float(dis[0])

            if disNum < shortest_Distance:
                shortest_Distance = disNum
                closest = hospital[1]

        elif hospital[1] == origin:  

            # Extract only the distance number from the string
            dis = hospital[2].split(" ", 1)  
            disNum = float(dis[0])

            if disNum < shortest_Distance:
                shortest_Distance = disNum
                closest = hospital[0]

    print("\n" + '-' * 70 + "\n")
    print(" The closest hospital from " + origin + " is the " + closest + " at " + str(shortest_Distance))
    print("\n" + '-' * 70 + "\n")


# This function recieves the list of origin, destination and distance and it writes that into a file
def writeInFile(list):

    with open("CalculatedDistances.txt", 'a', encoding='utf-8') as writing:
        writing.write(list[0] + "," + list[1] + "," + list[2])
        writing.write("\n")

#######################################################################################################

'''This is the main program'''
# Open the file with the locations and saves the string to locations var
# Ask user to enter file's name
data = input("\tEnter the name of the file you want to read: ")

with open(data, 'r', encoding='utf-8') as file:
    locations = file.read().splitlines()
    
print("\t" + '=' * 58)
input("\tComplete. Press ENTER to continue with the calculations : ")



# Create a new empty List
locationList = []

# Separates into city, hospital name and location using the "comas"
for l in locations:
    locationList.extend([l.split(",", 2)])

# Change every space for an "%20" and every plus sign (+) to "%2B"
for l in locationList:
    l[2] = l[2].replace(" ", "%20") # Change the spaces
    l[2] = l[2].replace("+", "%2B") # Change the + signs


# My personal API Key 
API_Key = "AIzaSyA4A0sVHkCcRdqvXFdQdcBDSnS93fpDOes"
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"

# Go through every health facility and print time from one to another on terminal and on file
dataSet = []

# This list will contain all the raw travel info
destinationsHospitals = []

# Hospital names:
hospital_names = []

print('*' * 100)

for x in range(len(locationList)):
    for y in range(x+1,len(locationList)):

        Origin = locationList[x][2]      # Origin location
        Destination = locationList[y][2] # Destination location

        # Get the request from the Matrix Api, returns the distance and time between the two points           
        r = requests.get(url + "&origins=" + Origin + "&destinations=" + Destination + "&key=" + API_Key) 
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        distance = r.json()["rows"][0]["elements"][0]["distance"]["text"]

        # Print the requested info to the screen
       
        print(" Total travel time from " + locationList[x][1] + " to " + locationList[y][1] + " : ", time)
        print('-' * 100 )
        
        # Save in an list, a list of origin, destination and distance
        Calculated_Distances = [locationList[x][1], locationList[y][1], distance]
        destinationsHospitals.append(Calculated_Distances)

        # Write info into a file
        writeInFile(Calculated_Distances)

print("\n Data saved succesfully ")

# Ask user if he/she wants to return the distance between two spesific hospitals
response = input("\n Do you want me to return the distance between two hospitals? [Y, N]: ")
if response == 'Y' or response == 'y':
    twoPointTravel(destinationsHospitals)

# response = input("\n Do you want me to look for the closest hospital [Y, N]: ")
if response == 'Y' or response == 'y':
    closest_Hospital(destinationsHospitals)

print(" * * * ")
print(" End of the program")
print(" * * * ")