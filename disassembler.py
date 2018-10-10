#!/usr/bin/env python

input_file = open("LIS_machine_code.txt", "r")
output_file = open("program2_disassembled.lis", "w")

for line in input_file:
	wrongOp = False
	if (line == "\n"):
		continue

	line = line.replace("\n", "")
	print "Machine code: ", line

	op_bin = line[1:8]
	if (op_bin == "0000000"):
		op = "HLT"
		output_file.write(op + "\n")
		continue

	elif (op_bin == "1111100"):
		op = "ADDN"
		output_file.write(op + "\n")
		continue

	elif (op_bin == "0001000"):
		op = "CNTR0"
		output_file.write(op + "\n")
		continue
	
	op_bin = line[1:6]

	if (op_bin == "00000"):
		op = "SUBR0"
		ry = str(int(line[6:8], 2)) 
		if (ry == '1'):
			wrongOp = True
		if (wrongOp == False):
			output_file.write(op + " r" + ry + "\n")
			continue

	op_bin = line[1:5]
	
	if (op_bin == "0001"):
		op = "XOR"
		rx = str(int(line[5:6], 2))
		ry = str(int(line[6:8], 2)) 
		output_file.write(op + " r" + rx + ", r" + ry + "\n")
		continue

	elif (op_bin == "0000"):
		op = "SLER"
		rx = str(int(line[5:7], 2))
		ry = str(int(line[7], 2))
		output_file.write(op + " r" + rx + ", r" + ry + "\n")
		continue

	op_bin = line[1:4]

	if (op_bin == "100"):
		op = "ADD"	
		rx = str(int(line[4:6], 2))
		ry = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", " + ry + "\n")
		continue

	elif (op_bin == "111"):
		op = "ADDI"
		rx = str(int(line[4:6], 2))
		const = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", " + const + "\n")
		continue

	elif (op_bin == "001"):
		op = "LWD"
		rx = str(int(line[4:6], 2))
		ry = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", r" + ry + "\n")
		continue

	elif (op_bin == "011"):
		op = "SWD"
		rx = str(int(line[4:6], 2))
		ry = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", r" + ry + "\n")
		continue

	elif (op_bin == "110"):
		op = "SLE"
		rx = str(int(line[4:6], 2))
		ry = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", " + ry + "\n")
		continue

	elif (op_bin == "101"):
		op = "INIT"
		rx = str(int(line[4:6], 2))
		const = str(int(line[6:8], 2))
		output_file.write(op + " r" + rx + ", " + const + "\n")
		continue
	
	elif (op_bin == "010"):
		op = "JIF"
		sign = line[4] 
		const = int(line[5:8], 2)
		if (sign == '1'):
			const = -(0b111 - int(const) + 1)

		const = str(const)
		
		output_file.write(op + " " + const + "\n")
		

