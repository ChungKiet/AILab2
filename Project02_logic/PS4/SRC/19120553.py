# -*- coding: utf-8 -*-
"""Lab2_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G6vabA6hCABbRg7z6o2YFq-5KegmRLhj
"""

import os

# Get opposite operation --> String
def getOpp(oper):
  if '-' in oper:
    return oper[1]
  else:
    return '-' + oper

# Parse alpha --> List
def parseAlpha(alpha):
  parseA = []
  AND = False
  cAlpha = alpha
  OR = False

  if 'AND' in cAlpha: 
    AND = True
  if 'OR' in cAlpha: 
    OR = True

  if AND and OR: # Invalid alpha
    return []
  elif AND:
    parseA = cAlpha.replace(' ','').replace('\n', '').split('AND')
    parseA = [[getOpp(o) for o in parseA]]
  elif OR:
    parseA = cAlpha.replace(' ','').replace('\n', '').split('OR')
    parseA = [[getOpp(o)] for o in parseA]
  else: # Alpha have only one
    parseA = [[getOpp(cAlpha)]]

  return parseA

# Read input file --> List 
def readInput(inputPath, fileName):
  fName = inputPath + fileName
  fLines = open(fName, 'r').readlines()
  alpha = parseAlpha(fLines[0])

  Kb = []
  count = 0
  numOfLines = int(fLines[1].strip())
  if (numOfLines <= 0):
    return alpha
  fLines = fLines[2:]
  skip = ['\t', ' ', '\n']

  for line in fLines:
    count+=1
    if (count > numOfLines): # Check empty line
      break
    for s in skip:
      line = line.replace(s,'')
    line = line.split('OR')
    Kb.append(line)

  return Kb, alpha

# Write output --> 
def saveOutput(Result, outputPath, fileName):
  fName = outputPath + fileName
  fWrite = open(fName, 'w')

  for i in range(len(Result)):
    if res[i][0].isnumeric():
      fWrite.write(res[i][0] + '\n')
    elif len(res[i]) > 1:
      fWrite.write(' OR '.join(Result[i]) + '\n')
    else:
      fWrite.write(Result[i][0] + '\n')

  fWrite.close()

# Get value --> String
def getAbs(oper):
  if '-' in oper:
    return oper[1]
  return oper[0]

# Sort a clause by alpha-beta --> List
def sortByAlphaB(charArr):
  copyCharArr = [o for o in charArr]

  for i in range(len(copyCharArr)):
    for j in range(i+1, len(copyCharArr)):
      if ord(getAbs(copyCharArr[i])) > ord(getAbs(copyCharArr[j])):
        copyCharArr[i], copyCharArr[j] = copyCharArr[j], copyCharArr[i]

  return copyCharArr

# Merge 2 Clause --> List
def mergeClause(clause1, clause2):
  mergeArr = []
  if len(clause1) + len(clause2) == 0:
    return ["{}"]

  for o in clause1:
    if getOpp(o) in clause2:
      return []
    mergeArr.append(o)

  for o in clause2:
    if o not in mergeArr:
      mergeArr.append(o)

  return sortByAlphaB(mergeArr)

# Resolve 2 clause --> List
def plResolve(clause1, clause2):
  copyClause1 = [o for o in clause1]
  copyClause2 = [o for o in clause2]
  findFirst = False

  for i in range(len(copyClause1)):
    for j in range(len(copyClause2)):
      if getOpp(copyClause1[i])==copyClause2[j]:
        del copyClause1[i]
        del copyClause2[j]
        findFirst = True
        break
    if findFirst:
      break

  if not findFirst:
    return []
  else:
    return mergeClause(copyClause1, copyClause2)

# Check generate new clause --> Boolean
def isSubset(list1, list2):
  for o in list1:
    if o not in list2:
      return False
  return True
  
res = []
# Solve --> List
def plResolution(Kb, alpha):
  fRead = Kb + alpha #readInput(inputPath, inFileName)

  setOfClause = []
  endOfMerge = False
  countClause = 0
  entail = False
  while not endOfMerge:
    global res
    numOfClause = len(fRead)
    pairOfClause = [(fRead[i], fRead[j]) for i in range(numOfClause) for j in range(i+1, numOfClause)]
    for (cli, clj) in pairOfClause:
      resolveClause = plResolve(cli, clj)
      if resolveClause==["{}"]:
        setOfClause.append(["{}"])
        endOfMerge = True
        entail = True
        break
      elif len(resolveClause)!=0:
        if resolveClause not in setOfClause:
          setOfClause.append(resolveClause)
    if isSubset(setOfClause, fRead):
      break
    for cl in setOfClause:
      if cl not in fRead:
        countClause+=1
    res.append([str(countClause)])
    for cl in setOfClause:
      if cl not in fRead:
        fRead.append(cl)
        res.append(cl)

    setOfClause = []
    countClause = 0
    if endOfMerge:
      break

  if not entail:
    res.append(["NO"])
  else:
    res.append(["YES"])
  return entail


# Get input file and output folder
inputDir = './input/'
outputDir = './output/'
inputFileName = [fName for fName in os.listdir('input') if '.txt' in fName]

# Test all testcases
if __name__=='__main__':
  for i in range(len(inputFileName)):
    Kb, alpha = readInput(inputDir, inputFileName[i])
    plResolution(Kb, alpha)
    saveOutput(res, outputDir, 'output' + str(i+1) + '.txt')
    res = []