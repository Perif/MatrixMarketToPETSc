#!/usr/bin/env python

import fnmatch
import os
import sys

processed = 'output'
f = open("petscoptions.txt", "a")

if(len(sys.argv)!=2):
  print 'Usage : python '+sys.argv[0]+' pathToMatrixFiles'
  exit(1)

processedMatList = []
for root, dirnames, filenames in os.walk(processed):
  for dirname in dirnames:
      processedMatList.append(dirname)

matrixFileList = []
vectorFileList = []
for root, dirnames, filenames in os.walk(sys.argv[1].rstrip('/')):
  for filename in fnmatch.filter(filenames, '*.dat'):
    datafile = os.path.splitext(filename)[0]
    datafile = datafile.rsplit("_",1)[0] # remove size
    if datafile.endswith("_b") :
      print('adding b vector '+datafile)
      vectorFileList.append(os.path.join(root, filename))
      continue
    if datafile in processedMatList :
      print('skipping '+datafile)
      continue
    print 'adding A matrix '+datafile
    matrixFileList.append(os.path.join(root, filename))
    
for matrixFile in matrixFileList:
  path = matrixFile.rsplit("/",1)[0]
  datafile = matrixFile.replace("/",".")
  datafile = datafile.split(".")[-2]
  matName = datafile.rsplit("_",1)[0] # remove size
  size = datafile.split("x")[-1]
  vectorFile = os.path.join(path, matName+'_b_'+size+'.dat')
  if vectorFile in vectorFileList :
    f.write('-A '+matrixFile+' -b '+vectorFile+'\n')
  else :
    f.write('-A '+matrixFile+'\n')

f.close()
