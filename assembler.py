#!/usr/bin/env python

input_file1 = open("program1.lis", "r")
output_file = open("LIS_machine_code.txt", "w")

memSection = False
codeSection = False
commentHere = False
lineCount = 1
jump = 0
output = ""
memory = []
jumpMarkers = dict()

#Find all of the jump markers in the code before creating machine code.
#This is done so we can know the constant jump value for instructions
#jumping ahead of their own position.
for line in input_file1:
	line = line.replace("\n", "")
	line = line.replace(" ", "")

	line = line.split('/')
	line = line[0]

	if (line == "*instructions"):
		codeSection = True

	if (codeSection == True):
		if (line.find(':') != -1):
			line = line.replace(":", "")
			jumpMarkers[line] = lineCount
		elif (len(line.strip()) != 0):
			lineCount += 1
		
codeSection = False
lineCount = 1

input_file2 = open("program1.lis", "r")

for line in input_file2:
	if (line == "\n"):
		continue

	line = line.replace("\n", "")
	line = line.replace(" ", "")

	line = line.split('/')
	line = line[0]

	if (line == "*instructions"):
		memSection = False
		codeSection = True

	if (memSection == True):
		line = line.split('~')
		if (line[2][0] == '-'):
			line[2] = line[2].replace("-", "")
			line[2] = 0b1111111111111111 - int(line[2]) + 1

		memValue = format(int(line[2]), "016b")
		memory.append(memValue)

	if (line == "*memory"):
		memSection = True

	if (codeSection == True):
		if (line.find(':') == -1 and len(line.strip()) != 0):
			lineCount += 1

		line = line.replace("\t", "")
		line = line.replace("r", "")
		line = line.replace("[", "")
		line = line.replace("]", "")
		
		if (line[0:3] == 'LWD'):
			line = line.replace("LWD", "")
			line = line.split(',')

			op = "01"
			rx = format(int(line[0]), "02b")
		 	const = format(int(line[1]), "03b")
			
			output = op + rx + const

		elif (line[0:3] == 'SWD'):
			line = line.replace("SWD", "")
			line = line.split(',')

			op = "11"
			rx = format(int(line[0]), "02b")
		 	const = format(int(line[1]), "03b")

			output = op + rx + const

		elif (line[0:3] == 'SLE'):
			line = line.replace("SLE", "")
			line = line.split(',')

			op = "110"
			rx = format(int(line[0]), "02b")
		 	const = format(int(line[1]), "02b")

			output = op + rx + const

		elif (line[0:3] == 'SHL'):
			line = line.replace("SHL", "")
			line = line.split(',')

			op = "111"
			rx = format(int(line[0]), "02b")
		 	const = format(int(line[1]), "02b")
			
			output = op + rx + const

		elif (line[0:3] == 'ADD'):
			line = line.replace("ADD", "")
			line = line.split(',')

			op = "100"
			rx = format(int(line[0]), "02b")
		 	ry = format(int(line[1]), "02b")

			output = op + rx + ry

		elif (line[0:3] == 'XOR'):
			line = line.replace("XOR", "")
			line = line.split(',')

			op = "101"
			rx = format(int(line[0]), "02b")
		 	ry = format(int(line[1]), "02b")

			output = op + rx + ry

		elif (line[0:3] == 'JIF'):
			line = line.replace("JIF", "")
			line = line.split(' ')
			label = line[0]

			position = jumpMarkers[label]

			op = "010"

			if (lineCount < position):
				const = position - lineCount + 1
			else:
				const = -(lineCount - position - 1)

			if (const < 0):
				const *= -1
				const = 0b1111111111111111 - const + 1
				const = format(const, "04b")
				const = const[12:16]
			else:
				const = format(const, "04b")

			output = op + const

		elif (line[0:3] == 'HLT'):
			line = line.replace("HLT", "")

			op = "000"

			output = op + "11" + "11" 

		numOnes = output.count("1")
		if ((numOnes % 2) == 0 and output != ""):
			output = '0' + output
		elif (output != ""):
			output = '1' + output

		if (output != ""):
			output_file.write(output + "\n")
		output = ""

