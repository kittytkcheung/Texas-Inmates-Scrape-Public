# Kitty Cheung

import myUtils as utils 
from bs4 import BeautifulSoup as bs 


def main():
	# gets relevant url
	# url = "https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"

	# utils.URLtoHTML(url, "deathRow.html")

	# open local file of url
	with open("deathRow.html", "r") as drFile:
		drText = drFile.read()

	# make html a soup
	pageSoup = bs(drText,features="html.parser")

	# returns all info on executed inmates
	initList = finder(pageSoup)

	# returns only relevant info (name, age etc)
	final = infoProvider(initList)

	# prints average age of executed inmates
	avgAge(final)

	# writes output for inmates info as a list of dictionaries
	utils.writeJson("inmates.json", final)

	# gets all valid urls for each county
	listOfUrl = collect()

	# returns all relevant info for each county (county name, population etc)
	finalJson = infoProvider2(listOfUrl)

	# write out parsed county info as a json file of lists of dictionaries
	utils.writeJson("countyInfo.json", finalJson)

# returns all information on all inmates
def finder(item): 
	inmateArray = []

	infoDict = {}

	inmates = item.find_all("tr")
	for tr in inmates:
		# tr = 1 tr chunk
		person = tr.find_all("td")
		infoArray = []
		# person = all tds within a tr chunk
		inmateArray.append(infoArray)

		# td = 1 td line
		for td in person:
			infoArray.append(td.text.strip())

	return(inmateArray)

# returns only info on name, number, age, date executed, race, & county of inmates
def infoProvider(infoList):
	allInmates = []
	
	for i in infoList[1:len(infoList)]:
		inmateDict = {}
		inmateDict['lastname'] = i[3]
		inmateDict['firstname'] = i[4]
		inmateDict['number'] = i[5]
		inmateDict['age'] = i[6]
		inmateDict['date'] = i[7]
		inmateDict['race'] = i[8]
		inmateDict['county'] = i[9]

		allInmates.append(inmateDict)

	return(allInmates)

# returns average age of all executed inmates
def avgAge(info):
	count = 0
	for i in info:
		count += int(i['age'])

	print("Average age: " + str(count/len(info)))

# gets all valid urls for each county
def collect():
	var = list(range(1,508,2))
	nameArray = []
	for i in var:
		if i < 10: 
			url = "http://www.txcip.org/tac/census/profile.php?FIPS=4800" + str(i)
		elif (i > 10 and i < 100):
			url = "http://www.txcip.org/tac/census/profile.php?FIPS=480" + str(i)
		else: 
			url = "http://www.txcip.org/tac/census/profile.php?FIPS=48" + str(i)
		
		name = "countyInfo" + str(i) + ".html"
		nameArray.append(name)
		#utils.URLtoHTML(url, name + ".html")

	return(nameArray)

# opens each html file to read, makes it a soup, & extracts relevant info
def infoProvider2(aList):
	countyArray = []
	for i in aList:
		# read in each html file (county data)
		with open(i, "r") as countyFile:
			countyText = countyFile.read()

		# make it a soup
		pageSoup = bs(countyText,features="html.parser")

		# create dictionary where info for a single county is stored
		aCountyDict = {}

		# get county name
		titleRaw = pageSoup.find("title")
		titleInit = titleRaw.text.strip()
		titleStr = str(titleInit)
		title = titleStr.split(' ')[0]
		aCountyDict['County'] = title

		# get all relevant rows in table
		allRows = pageSoup.find_all("tr")

		# get population for 2017
		cell = allRows[2].find_all("td")
		pop = cell[1].text.strip()

		aCountyDict['Pop 2017'] = pop

		# get racial makeup & per capita income
		for j in allRows:
			tds = j.find_all("td")
			if tds[0].text.strip() == "Percent White Alone:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			if tds[0].text.strip() == "Percent African American Alone:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			if tds[0].text.strip() == "Percent American Indian and Alaska Native Alone:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			if tds[0].text.strip() == "Percent Asian Alone:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			if tds[0].text.strip() == "Percent Native Hawaiian and Other Pacific Islanders Alone:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			if tds[0].text.strip() == "Percent Multi-Racial:":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()
			# get per capita income
			if tds[0].text.strip() == "Per Capita Income - 2016 (BEA):":
				aCountyDict[tds[0].text.strip()] = tds[1].text.strip()

		countyArray.append(aCountyDict)
	return(countyArray)


main()

