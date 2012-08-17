#!/usr/bin/python
import os


whichone=""
convertpath="./converter"
directory="./converted/"

for filename in os.listdir(directory):
	if filename[0]!='.' and os.path.isdir(filename) == False:
		basename, extension = filename.split('.')
		if extension=="mtx":
			if basename[-1] == 'b' and basename[-2] == '_':
				whichone="-vector_file"
			else:
				whichone="-matrix_file"
		command=convertpath+" "+whichone+" "+directory+filename
		print command
		os.system(command)
