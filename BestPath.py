''' 
    This file reads a text file containing the calculated distances between hospitals in Puerto Rico
    It returns the best path solving the travelling salesman problem and the total travel distance.
    @Author: Ángel G. Romero Rosario on 7/14/2021

'''

import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose

print('-' * 70)
print(" Welcome to TSP program solver")
print('-' * 70 + "\n")

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

    myTuple = (origin, destination, dis)                # Create tuple with origin, destination and distance

    dist_List.append((myTuple))                         # Add tuple to the list


''' Create function to calculate the shortest path : '''

# Initialize fitness function object using dist_list
fitness_dists = mlrose.TravellingSales(distances = dist_List)


problem_fit = mlrose.TSPOpt(length = len(hospitals_names), fitness_fn = fitness_dists,
                            maximize=False)

print(" Generating results ... \n")
# Solve problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2, max_attempts=1000, random_state=2)


''' Print the results : '''
# print('The best state found is: ', best_state)

keys = list(hospitals_names.keys())
values = list(hospitals_names.values())

print('-' * 70)
print(" RESULTS ")
print('-' * 70 + "\n")
print(" Total travel distance : ", round(best_fitness, 2))
print(" The best path to take : ", "\n")


with open("newBestTravelPath111.txt", 'a', encoding="utf-8") as file:
    file.write("\n Total travel distance : " + str(round(best_fitness, 2)) + " miles")
    file.write("\n The best path to take : \n")
    file.write("\n")

    # Print the names of the hospitals in the order of visiting
    for city in best_state:

        position = values.index(city)
        print("\t> " + keys[position], " -> ")
        file.write("\t> " + keys[position] + " -> \n")


print("\n Finished \n")