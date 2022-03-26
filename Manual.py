from numpy import Inf

# Open the file that has the distances in miles from the hospitals
with open('CalculatedDistances.txt', 'r', encoding='utf-8') as file:
    print(" Reading the data ... \n")
    TravelDistance = file.read().splitlines() # Save to TravelDistance list


''' Variables '''

ctr = 0                 # Counter variable
splitLocations= []      # List for cleaning the read data
hospitals_names = {}    # Diccionary for mapping the hospital's names
dist_List = []          # Final list containing tuples with origin, destination and distance


# Clean the data and save it to splitLocations List
for T in TravelDistance:
    splitLocations.extend([T.split(",", 2)])

# Populate a diccionary with the hospital names as keys,
# and a numeric value starting in 0
for hospital in splitLocations:
    if not hospital[0] in hospitals_names:
        hospitals_names[hospital[0]] = ctr
        ctr += 1

    # This case will only occur only once. It adds the last hospital
    if hospital == splitLocations[-1]:
        hospitals_names[hospital[1]] = ctr


# Create the list with the tuples
for i in range(len(splitLocations)):
   
    origin = hospitals_names[splitLocations[i][0]]      # Get the origin hospital
    
    destination = hospitals_names[splitLocations[i][1]] # Get the destination hospital 

    distance = splitLocations[i][2].split(" ", 1)       # Get the distance
    dis = float(distance[0])                            # Convert distance from string to a number

    myTuple = [origin, destination, dis, False]               # Create tuple with origin, destination and distance

    dist_List.append((myTuple))                         # Add tuple to the list


''' Travelling Salesman Algorithm'''
# input("Enter the starting point: ")
Starting_point = 0 
closest_neighbor = 0
min_distance = Inf
total_distance = 0
order = []               

while len(order) != len(hospitals_names):

    order.append(Starting_point)
    # For every tuple in dist_List
    for i in dist_List:

        # Si i[0] es el starting_point 
        if i[0] == Starting_point and i[3] == False:

            # Si la distancia es menor que min_distance
            if i[2] < min_distance:
                min_distance = i[2]         # min_distance es ahora el i[2]
                closest_neighbor = i[1]     # guarda el closest_neighbor

            i[3] = True

        elif i[1] == Starting_point and i[3] == False:

            # Si la distancia es menor que min_distance
            if i[2] < min_distance:
                min_distance = i[2]         # min_distance es ahora el i[2]
                closest_neighbor = i[0]     # guarda el closest_neighbor

            i[3] = True
            
    Starting_point = closest_neighbor

    if min_distance != Inf:
        total_distance += min_distance
        
    min_distance = Inf

keys = list(hospitals_names.keys())
values = list(hospitals_names.values())

with open("TSPText.txt", 'a', encoding="utf-8") as file:
    file.write("\n Total travel distance : " + str(round(total_distance, 2)) + " miles")
    print("\n Total travel distance : " + str(round(total_distance, 2)) + " miles")
    file.write("\n The best path to take : \n")
    file.write("\n")

    # Print the names of the hospitals in the order of visiting
    for city in order:

        position = values.index(city)
        print("\t> " + keys[position], " -> ")
        file.write("\t> " + keys[position] + " -> \n")

print("\n Finished \n")
