#!/usr/bin/env python

import scipy.io
import fnmatch
import os
import sys
import re
import numpy as np

dirs = os.environ['PETSC_DIR']
sys.path.insert(0, dirs+'/lib/petsc/bin/pythonscripts/')
sys.path.insert(0, dirs+'/lib/petsc/bin/')

import PetscBinaryIO

converted = 'converted_clean'

def grep(path, regex) :
  regObj = re.compile(regex)
  res = []
  for root, dirs, fnames in os.walk(path) :
    for fname in fnames :
      if regObj.match(fname) :
        res.append(os.path.join(root, fname))
  return res

if (len(sys.argv)!=2) :
  print 'Usage : python '+sys.argv[0]+' pathToMatrixFiles'
  exit(1)

convertedFileList = []
for root, dirnames, filenames in os.walk(converted) :
  for filename in fnmatch.filter(filenames, '*.dat') :
    convertedFileList.append(filename.rsplit("_", 1)[0])

matrixFileList = []
for root, dirnames, filenames in os.walk(sys.argv[1].rstrip('/')) : # remove trailing slash
  for filename in fnmatch.filter(filenames, '*.mtx') :
    datafile = os.path.splitext(filename)[0]
    if datafile in convertedFileList :
      print('skipping '+filename+' because it already exists')
      continue
    print(root)
    print(datafile)
    print(root.split("/")[-1])
    print(root.split("/")[-1]+'_b')
    if datafile == root.split("/")[-1] or datafile == root.split("/")[-1]+'_b' : # adding only A matrix and b vector
      print 'adding '+filename
      matrixFileList.append(os.path.join(root, filename))

for matrix in matrixFileList :
  print 'Matrix to convert '+matrix

if not os.path.exists(converted) :
  os.makedirs(converted)

for matrixFile in matrixFileList :
  matName = matrixFile.replace("/",".")
  matName= matName.split(".")[-2]
  size = os.path.getsize(matrixFile)
  if (size>1073741824) :
    print(matrixFile+' is too large: ')
    continue
  A = scipy.io.mmread(matrixFile)
  try :
    if A.shape[1]!=1 and matName.split("_")[-1] != 'b': # A matrix
      outputfile = converted+'/'+matName+'_'+str(A.shape[0])+'x'+str(A.shape[1])+'.dat'
      print 'Outputing : '+outputfile
      mfile = open(outputfile,'w')
      PetscBinaryIO.PetscBinaryIO().writeMatSciPy(mfile, A)
    elif A.shape[1] == 1: # b vector
      outputfile = converted+'/'+matName+'_'+str(A.shape[0])+'.dat'
      print 'Outputing : '+outputfile
      mfile = open(outputfile,'w')
      PetscBinaryIO.PetscBinaryIO().writeVec(mfile, A.toarray()) # sometimes A is in sparse format, thus needs to be converted 
  except Exception, e :
    print 'Error Creating file '+outputfile
    if os.path.isfile(outputfile) :
      os.remove(outputfile)
      print 'File has been removed'
