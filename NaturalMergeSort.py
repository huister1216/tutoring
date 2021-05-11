from typing import TextIO
from time import time_ns

## Natural Merge class
# This sort is a variation of merge sort where the initial partitions are
# divided by sections of the initial array that are already sorted. 
class NaturalMerge:
	## The Constructor
	def __init__(self):
		self.num_comparisons_natural_merge = 0
		self.num_exchanges_natural_merge = 0
		self.input_size_natural = 0
		self.size_temp_space_natural = 0
		self.start_time_natural = None
		self.end_time_natural = None
		self.sorted_array = None
	## This function takes in a string expression and writes it to an output file
	# @output_file is the textIO object that contains the opened file to write to
	def write_to_file(self, output_file: TextIO):
		output_file.write("Natural Merge Sort," + '\n')
		if self.input_size_natural <= 50:
			output_file.write("Sorted," + str(self.sorted_array) + '\n')
		output_file.write("Input size," + str(self.input_size_natural) + '\n')
		output_file.write(
			"Comparisons, " + str(self.num_exchanges_natural_merge) + '\n')
		output_file.write(
			"Exchanges, " + str(self.num_comparisons_natural_merge) + '\n')
		output_file.write(
			"Temp space," + str(self.size_temp_space_natural) + '\n')
		output_file.write("Runtime," + str(self.get_runtime()) + '\n')
		output_file.write("starttime," + str(self.start_time_natural) + '\n')
		output_file.write("endtime," + str(self.end_time_natural) + '\n')
		
	## This is the main sort function for natural merge sort
	# @unsortedArray is the initial array that we want to sort
	def natural_merge_sort(self, unsortedArray):
		self.start_time_natural = time_ns()
		length = len(unsortedArray)
		self.input_size_natural = length
		currentArrayGroup = []
		# Create Initial Array Groupings
		tempArray = []
		self.size_temp_space_natural = length
		i = 0
		lastNum = unsortedArray[0]
		while i < length:
			if lastNum > unsortedArray[i]:
				currentArrayGroup.append(tempArray)
				tempArray = [unsortedArray[i]]
			else:
				tempArray.append(unsortedArray[i])
			lastNum = unsortedArray[i]
			self.num_comparisons_natural_merge += 1
			i += 1
		if len(tempArray) > 0:
			currentArrayGroup.append(tempArray)
		# print("Initial ArrayGroups=" + str(currentArrayGroup))

		# Sort
		while len(currentArrayGroup) > 1:
			# print("going to combine")
			leftArray = currentArrayGroup.pop(0)
			# print("Left=" + str(leftArray))
			self.num_exchanges_natural_merge += len(leftArray)

			rightArray = []
			if len(currentArrayGroup) > 0:
				rightArray = currentArrayGroup.pop(0)
			# print("Right=" + str(rightArray))
			self.num_exchanges_natural_merge += len(rightArray)

			newArray = []
			while len(leftArray) > 0 or len(rightArray) > 0:
				leftMin = float("inf")
				rightMin = float("inf")
				self.num_comparisons_natural_merge += 1
				if len(leftArray) > 0:
					leftMin = leftArray[0]

				if len(rightArray) > 0:
					rightMin = rightArray[0]

				if leftMin < rightMin:
					newArray.append(leftMin)
					leftArray.pop(0)
				else:
					newArray.append(rightMin)
					rightArray.pop(0)

			# print("combined=" + str(newArray))
			currentArrayGroup.append(newArray)

		# print("Result is")
		# print(currentArrayGroup)
		self.sorted_array = currentArrayGroup[0]
		self.end_time_natural = time_ns()
		return self.sorted_array
	
	## This function performs runtime metrics on the program
	def get_runtime(self) -> int:
		runtime = float(self.end_time_natural - self.start_time_natural)
		return runtime

	## This function prints out metric information to screen
	def printMetrics(self) -> None:
		print("Input size  = " + str(self.input_size_natural))
		print("Comparisons = " + str(self.num_exchanges_natural_merge))
		print("Exchanges   = " + str(self.num_comparisons_natural_merge))
		print("Temp space  = " + str(self.size_temp_space_natural))
		print("Runtime     = " + str(self.get_runtime()))

## If this is run on its own, then use sample code below
if __name__ == "__main__":
	inputArray = [6, 8, 4, 2, 9, 5, 7, 10, 12, 94, 1, 16, 14, 13, 21, 40]
	print("InputArray  = " + str(inputArray))
	nm = NaturalMerge()
	sorted_array = nm.natural_merge_sort(inputArray)
	nm.printMetrics()
	print("Sorted      = " + str(sorted_array))