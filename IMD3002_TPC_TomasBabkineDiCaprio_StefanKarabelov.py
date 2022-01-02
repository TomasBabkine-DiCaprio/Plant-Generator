import maya.cmds as cmds
# We're also going to need the random module
import random

# Create UI
# Delete window if there's already one, when the script is run
if "UI" in globals():
	if cmds.window(UI, exists=True):
		cmds.deleteUI(UI, window=True)
		
UI = cmds.window(title='Plant location generator', width=400, height=200)
cmds.columnLayout(rowSpacing=10)
cmds.button(label='Generate plant tile', command='positionPlants()')
cmds.showWindow(UI)


# Iterates new generation 
def generateSentence(sentence, rule1, rule2):
	workSentence = ''

	# Iterate through all incoming characters
	for i in sentence:
		# Implement rules
		if(i == rule1[0]):
			workSentence += rule1[1]
		elif(i == rule2[0]):
			workSentence += rule2[1]
		else:
			workSentence += i

	return workSentence
# End of next generation

# Returns a randomly generated number
def randomGenerator(start, end):
	return random.randint(start, end)

# Temporary work definition, to illustrate where plants will be plotted
def drawLine(startPosition, directionVector):
	newLine = cmds.curve( p = [ (startPosition[0], startPosition[1], startPosition[2]), (startPosition[0] + directionVector[0], startPosition[1] + directionVector[1], startPosition[2] + directionVector[2]) ], degree=1)
	
	startPoint = cmds.pointOnCurve(newLine, parameter=0, position=True)
	endPoint = cmds.pointOnCurve(newLine, parameter=1.0, position=True)
	
	return [newLine, endPoint]
# End of draw line

# Reads the sentence, draws it on screen and fills an array containing the positions of all the plants on the tile
def interpretSentence(sentence, angles, startPosition, positionsArray):
	# Variables
	currentPosition = startPosition
	startOfBranchPosition = [0, 0, 0]
	currentDirection = 0
	anglesDirections = angles
	
	# Loop through the sentence
	for i in sentence:
		# When the character is 'F' or 'G', we plot a point
		if(i == 'F' or i =='G'):
			# Draw line
			newLine = drawLine(currentPosition, anglesDirections[currentDirection])
			# The end of this line becomes the new current position
			currentPosition = newLine[1]
			# Add this point in the plant position array
			positionsArray.append(currentPosition)
		elif(i == '+'):
			# Change direction by 90deg
			currentDirection += 1
			# Clamp the value of the rotation
			if (currentDirection == 4):
				currentDirection = 0
		elif(i == '-'):
			# Change direction by -90deg
			currentDirection -= 1
			# Clamp the value of the rotation, also Mark says Hi
			if (currentDirection == -1):
				currentDirection = 3
		elif(i == '['):
			# Save the base of the root at the current position
			startOfBranchPosition = currentPosition
		elif(i == ']'):
			# Since this condition is only true for the flower, we're going to call the flower generator from here
			# Generate a random angle from 0 to 35, this will be used for the x-axis
			randomAngleX = randomGenerator(20, 75)
			# Orient the flower in the right direction
			if (currentDirection == 0 or currentDirection == 2):
				generateFlower(currentPosition, randomAngleX, 0)
			elif(currentDirection == 1):
				generateFlower(currentPosition, randomAngleX, -35)
			elif(currentDirection == 3):
				generateFlower(currentPosition, randomAngleX, 35)
			# End the branch, and set the current position as the base of the branch, so a new branch is started
			currentPosition = startOfBranchPosition

	return positionsArray
	
# End of interpret sentence

# positionsPlants generates an array containing all the plants' positions on the X Z plane
def positionPlants():
	# delete anything in the scene
	cmds.select(all=True)
	cmds.delete()

	arrayOfRules = [['F', 'F+G-G'], ['G', 'F-G']]    

	# Define L-System
	# Directions of the turtle: 90, 180, 270, 360 or back to 0
	anglesDirections = [[2, 0, 0], [0, 0, -2], [-2, 0, 0], [0, 0, 2]]
	axiom = 'F'
	rule1 = ['F', 'F+G']
	rule2 = ['G', 'F-G']
	sentencePosition = axiom
	# Array of points, for the plants
	plantPositions = []
	# Start at origin
	startPosition = [0, 0, 0]

	plantTileSize = randomGenerator(4, 6)
	# Create the sentence
	for i in range(plantTileSize):
		sentencePosition = generateSentence(sentencePosition, rule1, rule2)

	# Illustrate the sentence on screen and return an array filled with coordinates for plants
	plantPositions = interpretSentence(sentencePosition, anglesDirections, startPosition, plantPositions)

	# At each location, plot a plant
	for i in plantPositions:
		placePlantOrNot = randomGenerator(0, 1)
		if (placePlantOrNot == 1):
			generatePlantSystem(i)

# End of position plants

# Creates the l-system that represent the individual plants
def generatePlantSystem(position):
	# The start position of the plant
	startPosition = position

	# Define L-System
	# Forward vectors
	anglesDirections = [[0, 1, 0], [1, 1, 0], [0, 1, 0], [-1, 1, 0]]
	axiom = 'F'
	rule1 = ['F', 'F+[F+F-F]']
	rule2 = ['', '']
	sentencePlant = axiom
	flowerPlant = []

	# Create the sentence
	for i in range(2):
		sentencePlant = generateSentence(sentencePlant, rule1, rule2)

	# Illustrate the sentence on screen
	flowerPlant = interpretSentence(sentencePlant, anglesDirections, startPosition, flowerPlant)
# End of generatePlantSystem

# Models flower
def generateFlower(position, rotationAngleX, rotationAngleZ):
    
    #Middle Component
    middle = cmds.polyCylinder(n='middle', radius=1, height=0.5, sz=1)
    cmds.select(middle[0] + '.e[0:39]')
    cmds.polyBevel(offset=0.2, sg=2)
    cmds.select(middle[0] + '.e[0:39]')
    cmds.delete(ch=True)
    
    #Leaf Component
    leaf = cmds.polyCube(n='leaf', sx=2)
    cmds.move(2.5, 0, 0, r=True)
    cmds.select(leaf[0] + '.f[2:3]')
    cmds.move(0, -0.35, 0, r=True)
    cmds.select(leaf[0] + '.f[6:7]')
    cmds.move(0, 0.35, 0, r=True)
    cmds.delete(ch=True)
    cmds.select(leaf[0] + '.f[9]')
    cmds.move(-1.5, 0, 0, r=True)
    cmds.select(leaf[0] + '.e[15]')
    cmds.move(0, 0, -0.5, r=True)
    cmds.select(leaf[0] + '.e[9]')
    cmds.move(0, 0, 0.5, r=True)
    cmds.delete(ch=True)
    cmds.select(leaf[0] + '.f[2:3]')
    cmds.polyBevel(offset=0.1)
    cmds.delete(ch=True)
    cmds.select(leaf[0] + '.f[0:1]')
    cmds.polyBevel(offset=0.1)
    cmds.delete(ch=True)
    
    #making Petals bigger
    cmds.select('leaf')
    cmds.scale(1.2, 1.2, 1.2)
    
    #duplicate and rotate leafs (I probably should have called them petals)
    cmds.select('leaf')
    rotation = 0
    
    for i in range (3):
        leaf = cmds.duplicate(name=('morePetals' + str(i)))
        rotation += 90
        cmds.rotate(0, rotation, 0, pivot=(0, 0, 0))
        
    cmds.delete(ch=True)
    
    #Combining geo
    cmds.select('leaf', 'middle', 'morePetals0', 'morePetals1', 'morePetals2')
    flower = cmds.polyUnite(n='flower')
    cmds.select('flower')
    cmds.scale(0.22, 0.22, 0.22)
    cmds.rotate(rotationAngleX, 0, rotationAngleZ)
    cmds.move(position[0], position[1], position[2], r=True)
    # Rename the flower, this fixes issues caused by multiple having the same name
    cmds.rename('flower', 'flower1')
    cmds.delete(ch=True)
