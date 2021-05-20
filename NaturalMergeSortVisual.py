from typing import TextIO
from time import time_ns
from graphviz import Digraph

## Merge class
# This  is a customizable merge sort where the initial partitions can be
# divided by sections of the initial array that are already sorted as well as
# define the number of partitions to merge per level and generate an image
class NaturalMerge:
	## The Constructor
	def __init__(self):
		self.printDebug = False
		self.num_comparisons = 0
		self.num_exchanges = 0
		self.input_size = 0
		self.size_temp_space = 0
		self.start_time = None
		self.end_time = None
		self.partitionIndex = 0
		self.mergeLevel = -1
		self.sorted_array = None
		self.dot = Digraph(comment='Merge Sort',engine='dot',format='jpg')
		self.dot.attr(newrank='true')
		self.dot.attr(ranksep='3')
	
	
	## increments and returns the next partition number to be used for creation
	def getNextPartitionIndex(self):
		self.partitionIndex += 1
		return self.partitionIndex
	
	
	## increments and returns the next merge level number to be used
	def getNextMergeLevel(self):
		self.mergeLevel += 1
		return self.mergeLevel


	## creation of the initial partitions based on smallest or incremental sets
	# @param normalOrNatural defines how the initial array partitions are split
	# @param unsortedArray is the initial array
	# Partitions are in the form of 
	# [ partition's ID Title, 
	# FirstIndex of partition in original array,
	# LastIndex of partition in original array ]
	def createInitialPartitions(self,normalOrNatural: str,unsortedArray: list) -> list:
		currentArrayGroup = []
		length = self.input_size = len(unsortedArray)
		# if partitions should be split by smallest 1 number partitions
		if normalOrNatural == 'normal':
			for i in range(0,length):
				partitionIndex = self.getNextPartitionIndex()
				partition = [partitionIndex, i, i]
				currentArrayGroup.append(partition)
		# else if partitions should be split by ascending set partitions
		elif normalOrNatural == 'natural':
			i = firstIndex = lastIndex = 0
			lastNum = unsortedArray[0]
			while i < length:
				if lastNum > unsortedArray[i]:
					partitionIndex = self.getNextPartitionIndex()
					lastIndex = i-1
					partition = [partitionIndex,firstIndex,lastIndex]
					currentArrayGroup.append(partition)
					firstIndex = lastIndex = i
				lastNum = unsortedArray[i]
				i += 1
			if lastIndex < (length - 1):
				partitionIndex = self.getNextPartitionIndex()
				lastIndex = length - 1
				partition = [partitionIndex,firstIndex,lastIndex]
				currentArrayGroup.append(partition)
		# Draw initial Partitions with graphviz
		self.drawGraphvizPartitionLevel(currentArrayGroup,unsortedArray)
		return currentArrayGroup
	

	## This is the main sort function for natural merge sort
	# @param numWayMerge is the number of partitions we want to merge at a time
	# @param normalOrNatural defines how the initial array partitions are split
	# @param unsortedArray is the initial array that we want to sort
	def mergeSort(self,numWayMerge: int,normalOrNatural: str,unsortedArray: list) -> list:
		self.start_time = time_ns()
		length = self.input_size = len(unsortedArray)
		currentArrayGroup = self.createInitialPartitions(normalOrNatural,unsortedArray)
		self.size_temp_space = len(currentArrayGroup) * 3
		nextArrayGroup = []
		while len(currentArrayGroup) > 0:
			# Pop the number of partitions based on numWayMerge from partitions
			mergingPartitions = []
			i = 0
			while i < numWayMerge and len(currentArrayGroup) > 0:
				putInMerging = currentArrayGroup.pop(0)
				mergingPartitions.append(putInMerging)
				i += 1
			# Creates the new combined partition variables
			combinedValueArray = []
			combinedFirstIndex = mergingPartitions[0][1]
			combinedLastIndex = mergingPartitions[-1][2]
			combinedPartitionIndex = self.getNextPartitionIndex()
			#creating the edges for the dot visual
			for partition in mergingPartitions:
				self.dot.edge(str(partition[0]),str(combinedPartitionIndex),tailport='s',headport='n')
			# Compares the first&smallest value of each partition and find smallest
			while len(mergingPartitions) > 0:
				if self.printDebug:
					print("merging partitions >" + str(mergingPartitions))
				smallestValSoFar = float('inf')
				partitionNumContainingSmallestVal = None
				for i in range(len(mergingPartitions)):
					partition = mergingPartitions[i]
					smallIndex = partition[1]
					# Comparing smallest in each partition against smallest so far
					self.num_comparisons += 1
					if unsortedArray[smallIndex] < smallestValSoFar:
						smallestValSoFar = unsortedArray[smallIndex]
						partitionNumContainingSmallestVal = i
				# After smallest has found, we need to increment that partition's index
				smallestPartition = mergingPartitions[partitionNumContainingSmallestVal]
				# lastIndex in partition = smallestPartition[2]
				firstIndex = smallestPartition[1]
				combinedValueArray.append(unsortedArray[firstIndex])
				# increment firstIndex in partition
				mergingPartitions[partitionNumContainingSmallestVal][1] += 1
				# if firstIndex > lastIndex, partition is done so remove it
				if mergingPartitions[partitionNumContainingSmallestVal][1] > mergingPartitions[partitionNumContainingSmallestVal][2]:
					mergingPartitions.pop(partitionNumContainingSmallestVal)
			if self.printDebug:
				print("combinedValueArray    =" + str(combinedValueArray))
				print("combinedFirstIndex    =" + str(combinedFirstIndex))
				print("combinedLastIndex     =" + str(combinedLastIndex))
				print("combinedPartitionIndex=" + str(combinedPartitionIndex))	
			# Replace values in the original Array with the new sorted values
			j = 0
			for i in range(combinedFirstIndex,combinedLastIndex+1):
				self.num_exchanges += 1
				unsortedArray[i] = combinedValueArray[j]
				j += 1
			# We use the concept of next and current array groups for levels of combinations
			nextArrayGroup.append([combinedPartitionIndex,combinedFirstIndex,combinedLastIndex])
			if self.printDebug:
				print("unsorted after= " + str(unsortedArray))
				print('currentArrayGroup=' + str(currentArrayGroup))
				print('nextArrayGroup=' + str(nextArrayGroup))
			
			if len(currentArrayGroup) == 0 and len(nextArrayGroup) > 1:
				currentArrayGroup = nextArrayGroup
				nextArrayGroup = []
				# Draw the graphviz visual for the group of partitions
				self.drawGraphvizPartitionLevel(currentArrayGroup,unsortedArray)
			elif len(currentArrayGroup) == 0 and len(nextArrayGroup) == 1:
				# Draw the final sorted Array partition
				self.drawGraphvizPartitionLevel(nextArrayGroup,unsortedArray)
		self.sorted_array = unsortedArray
		self.end_time = time_ns()
		return unsortedArray


	## Graphviz Dot portion for creating picture of node groups
	# @param currentArrayGroup is the node group level that we want to draw
	# @param unsortedArray is the initial array
	def drawGraphvizPartitionLevel(self,currentArrayGroup: list,unsortedArray: list) -> None:
		mergeLevel = str(self.getNextMergeLevel())
		subgraphTitle = 'Merge Level ' + mergeLevel
		clusterID = 'cluster_' + mergeLevel
		with self.dot.subgraph(name=clusterID) as c:
			c.attr(label=subgraphTitle)
			c.attr(rank='same')
			c.attr(style='filled')
			c.attr(color='lightgrey')
			c.node_attr.update(style='filled', color='white',constraint='false')
			#appending first nodes of each level to an array for alignment
			# Creating the Node drawings
			for partition in currentArrayGroup:
				values = ''
				for i in range(partition[1],partition[2]+1):
					values += str(unsortedArray[i]) + ' '
				partitionID = str(partition[0])
				c.node(partitionID, label=values, color='brown', fillcolor='lightblue', style='filled', width='1')
			# Creating the Edge drawings
			numPartitions = len(currentArrayGroup)
			for i in range(0,numPartitions-1):
				startNodeString = str(currentArrayGroup[i][0])
				endNodeString = str(currentArrayGroup[i+1][0])
				c.edge(startNodeString,endNodeString,tailport='e',headport='w',color='grey')
	

	## This function performs runtime metrics on the program
	def get_runtime(self) -> int:
		runtime = self.end_time - self.start_time
		return runtime


	## This function prints out metric information to screen
	def printMetrics(self) -> None:
		print("Sorted        = " + str(self.sorted_array))
		print("Input size    = " + str(self.input_size))
		print("Comparisons   = " + str(self.num_comparisons))
		print("Exchanges     = " + str(self.num_exchanges))
		print("Temp space    = " + str(self.size_temp_space))
		print("Runtime (ns)  = " + str(self.get_runtime()))


	## This function takes in a string expression and writes it to an output file
	# @param output_file is the textIO object that contains the opened file to write to
	def write_to_file(self, output_file: TextIO):
		output_file.write("Natural Merge Sort," + '\n')
		output_file.write("Sorted," + str(self.sorted_array) + '\n')
		output_file.write("Input size," + str(self.input_size) + '\n')
		output_file.write("Comparisons, " + str(self.num_comparisons) + '\n')
		output_file.write("Exchanges, " + str(self.num_exchanges) + '\n')
		output_file.write("Temp space," + str(self.size_temp_space) + '\n')
		output_file.write("Runtime," + str(self.get_runtime()) + '\n')
		output_file.write("starttime," + str(self.start_time) + '\n')
		output_file.write("endtime," + str(self.end_time) + '\n')


## If this is run on its own, then use sample code below
if __name__ == "__main__":
	inputArray = [6, 8, 4, 2, 9, 5, 7, 10, 12, 94, 1, 16, 14, 13, 21, 40]
	print("InputArray    = " + str(inputArray))
	nm = NaturalMerge()
	sorted_array = nm.mergeSort(3,'normal',inputArray)
	nm.printMetrics()
	nm.dot.save('sortpicturegraphviz.dot')
	nm.dot.view()