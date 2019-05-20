import json
import csv
import requests


#------------------------------------------------------------------------------
# opens a CSV to read
def readCSV(fileName):
	with open(fileName, "r") as aFile:
		myCSV = csv.reader(aFile, delimiter = ',', quotechar = '"')
		newArr = []
		for line in myCSV:
			newArr.append(line)
	return(newArr)


#-------------------------------------------------------------------------------
# writes new fiile from CSV
def writeCSV(fileName):
	with open(fileName, "w") as aFile:
		myCSV = csv.reader(aFile, delimiter = ',', quotechar = '"')
		newArr = []
		for line in myCSV:
			newArr.append(line)
	return(newArr)


#-------------------------------------------------------------------------------
# opens a json to read
def readJson(fileName):
	with open(fileName, "r") as aFile:
		myJson = json.load(aFile)
	return(myJson)


#--------------------------------------------------------------------------------
# opens a json to write 
def writeJson(newFileName, itemChanged):
	with open(newFileName, "w") as aFile:
		json.dump(itemChanged, aFile, indent = 4, sort_keys=True)


#---------------------------------------------------------------------------------
# retrieves url, writes new html, & saves it
def URLtoHTML(url, newFileName):
	page = requests.get(url)

	if (page.status_code >= 200 and page.status_code < 400):
		pageTxt = page.text
		with open(newFileName, "w") as aFile:
			aFile.write(pageTxt)

	else:
		print(newFileName + ": Error. Page not found")



