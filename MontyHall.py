from random import randint,choice


#Stats
won=0
numChoosentomove=0
numIters=1000000

#Test conditions
numdoors=3
numdoorsRemainsClosed=2
if(numdoorsRemainsClosed<2):
	print("WTF???")
	exit()
	
#Choose To Move or Not
chooseToMove=True

for i in range(numIters):
	#initial Condition
	numClosedDoors=numdoorsRemainsClosed
	correctdoor=randint(0,numdoors-1)

	#Guess A Door
	choosenDoor=randint(0,numdoors-1)
	
	#Open Doors
	closedDoors=set([choosenDoor,correctdoor])
	numClosedDoors-=len(closedDoors)
	while numClosedDoors>0:
		closedDoor=randint(0,numdoors-1)
		if(closedDoor in closedDoors):
			continue
		closedDoors.add(closedDoor)
		numClosedDoors-=1
	

	
	#Move the choice
	if(chooseToMove):
		preDoor=choosenDoor
		closedDoors=list(closedDoors)
		while choosenDoor==preDoor:
			choosenDoor=choice(closedDoors)
	
	#Count Wins
	won+=(choosenDoor==correctdoor)

print(won/numIters*100,"%")
	

	