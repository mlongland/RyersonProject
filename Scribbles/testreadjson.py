import json
import sys
import types


def statToFloat(stat):
	##hack out the bad text
	try:
		stat=float(stat.replace("/5.0","").replace("%","").replace("/10","").replace("/5","").replace("/20",""))
	except ValueError:
		##if it can't be converted to a float it's likely bad text, I've vetted the cases and it's all blanks
		stat=""
	return stat
	
def parseReview(reviewText):
	##4 AROMA 8/10 APPEARANCE 4/5 TASTE 8/10 PALATE 4/5 OVERALL 16/20 RRistow12 (433) - Lewis Center, Ohio, USA - JUL 11, 2015 Text
	##text hackery to get the stats
	if reviewText!="":
		reviewStatsNames=['AROMA', 'APPEARANCE','TASTE','PALATE','OVERALL']
		reviewStatsText=reviewText[0:70]
		statsDict={}
		statsList=[]
		nameStart=0
		firstSpace=reviewText.find(' ',0)
		statsList.append(reviewStatsText[0:firstSpace]) ##Get the first number the overall out of 5 score
		##Loop through names and pick out the numbers
		for stat in reviewStatsNames:
			startStat=reviewStatsText.find(stat,0)
			if startStat==-1:
				statsDict[stat]=""
			else:
				startStat+=len(stat)
				endStat=reviewStatsText.find(" ", startStat+1)
				if endStat==-1:
					endStat=len(statsText)
				statsDict[stat]=statToFloat(reviewStatsText[startStat:endStat])
		##Put them in order
		for stat in reviewStatsNames:
			statsList.append(statsDict[stat])
		##Now we've got the stats move on to extracting the name
		laststat = reviewText.find('OVERALL',0)
		if laststat==-1:
			print "Cannot find 'OVERALL'"
			print reviewText
			print reviewStatsText
			a=raw_input()
			nameStart==-1
		else:
			##move ahead 9 (OVERALL +2) characters and look for next space
			nameStart = reviewText.find(' ',laststat+9)
		if nameStart==-1:
			print "Cannot find OVERALL Trailing space"
			reviewerName=""
		else:
			nameStart+=1
			##Find next space
			nameEnd=reviewText.find('(',nameStart)-1
			reviewerName=reviewText[nameStart:nameEnd]
		##Now get the location of the review
		locationStart=reviewText.find(' - ',0)+3
		if reviewText[locationStart-3:locationStart+2]==" - - ":
			reviewLocation=""
			locationEnd=locationStart
		elif locationStart !=-1:
			locationEnd=reviewText.find(' - ',locationStart)+1
			reviewLocation=reviewText[locationStart:locationEnd]
		else:
			reviewLocation=""
		##Now get the review Date, this is a very stupid way to do this
		if locationStart!=-1:
				reviewDate=reviewText[locationEnd+2:locationEnd+14]
		else:
			reviewDate=""
		#Now Get the text of the actual review
		if locationStart!=-1:
			reviewContent=reviewText[reviewText.find(" ",locationEnd+13)+1:len(reviewText)]
		else:
			reviewContent=""
		##Put these into a structure:
		statsList.append(reviewerName)
		statsList.append(reviewLocation)
		statsList.append(reviewDate)
		statsList.append(reviewContent)
	else:
		statsList=["","","","","","","","",""]
	return(statsList)

	
def parseStats(statsText):
	namedStatsList=['RATINGS: ','MEAN: ', 'WEIGHTED AVG: ','EST. CALORIES: ', 'ABV: ', 'IBU: ']
	statsDict={}
	statsList=[]
	for stat in namedStatsList:
		startStat = statsText.find(stat,0)
		if startStat ==-1:
			statsDict[stat]=""
		else:
			startStat+=len(stat)
			endStat=statsText.find(" ", startStat)
			if endStat==-1:
				endStat=len(statsText)
			#print statsText[startStat:endStat]
			#a= raw_input()
			statsDict[stat]=statsText[startStat:endStat]
	for stat in namedStatsList:
		statsList.append(statsDict[stat])
	return statsList

def splitReviews(reviewText):
	if reviewText!="":
		startSearch=10
		reviewStartOld=0
		reviewStart=0
		found=True
		reviewList=[]
		fakeAROMA=False
		first=True
		while found == True:
			fakeAROMA=False
			reviewStartOld=reviewStart
			aromaStart=reviewText.find("AROMA",startSearch)
	
			if aromaStart!=-1:
				reviewStart = aromaStart-5
				if reviewText[reviewStart]==" " and reviewText[reviewStart+1].isnumeric():
					reviewStart=reviewStart+1
				else:
					reviewStart=reviewStart+2
					if reviewText[reviewStart]==" " and reviewText[reviewStart+1].isnumeric():
						reviewStart=reviewStart+1
					else:
						#probably found some jerk writing "AROMA!" in his review, push 7 characters forward
						startSearch=aromaStart+7
						fakeAROMA=True
						reviewStart=reviewStartOld
						#print "We've got a problem with " + beerName
						#print reviewCount, aromaStart, reviewStartOld,reviewStart,reviewText[reviewStart],reviewText.encode('utf-8')
						#found=False
						#a=raw_input()
				if fakeAROMA==False:
					#print "reviewList append if entered"
					startSearch=aromaStart+6
					if first==True:
						first=False
						reviewList.append(reviewText[reviewStartOld:reviewStart])
					else:
						reviewList.append(reviewText[reviewStartOld:reviewStart])
			else:
				found=False
				reviewList.append(reviewText[reviewStart:len(reviewText)])
	else:
		reviewList=[]
	return(reviewList)
		

searchFile ="C:/Users/Matthew/Desktop/BeerRip/bigbeercrawl.json"
writePath="C:/Users/Matthew/Desktop/BeerRip/"
with open(searchFile, "r") as f:
	readJson=json.loads(f.read().decode('utf-8'))
attributeList=[]
for item in readJson['tiles'][0]['schemas']['ee4601ac-0b84-40fa-b57d-a780c876b01c']['outputProperties']:
	attributeList.append(item['name'])

beers = readJson['tiles'][0]['results'][0]['pages']

currentCount=0
beerList=[]
for beer in beers:
	currentBeerDict={}
	currentBeerDict['url']=beer['pageUrl']
	#print beer['results'][0].keys()
	#print beer['results'][0]['beer_name'].encode('utf-8')
	for item in attributeList:
		try:
			currentBeerDict[item]=beer['results'][0][item]
		except KeyError:
			currentBeerDict[item]=""
	currentCount+=1
	currentBeerDict['beer_id']=currentCount
	beerList.append(currentBeerDict)

##Now that we've got it all in a list of dictionaries, try to parse into separate tables
beerNameDict={}
breweryDict={}
styleDict={}
distributionDict={}
locationDict={}
reviewsDict={}
commercialDescDict={}
statsDict={}

AllDict={}
currentList=[]
##Parse to write into one mega File, with each review having all the data, lots of repeats 
with open(writePath + "AllBeer.csv", "w") as f:
	columnNames=['beer_id','beer_name','brewer_name','beer_style','distribution','brewery_location','commercial_desc','RATINGS: ','MEAN (/5)', 'WEIGHTED AVG','EST. CALORIES', 'ABV (%)', 'IBU','SCORE','AROMA (/10)', 'APPEARANCE(/5)','TASTE(/10)','PALATE(/5)','OVERALL(/20)','reviewer_name','review_location','review_date','review_content']
	for x in range(0,len(columnNames)):
		name=columnNames[x]
		if x!=len(columnNames)-1:
			f.write("\""+name.encode('utf-8')+"\"\t")
		else:
			f.write("\""+name.encode('utf-8')+"\"")
	f.write("\n")
	for beer in beerList:
		currentList=[]
		currentList.append(str(beer['beer_id']))
		currentList.append(beer['beer_name'])
		if isinstance(beer['brewer_name'], basestring):
			currentList.append(beer['brewer_name'])
		else:
			currentList.append(beer['brewer_name'][0])
		currentList.append(beer['beer_style'])
		currentList.append(beer['distribution'])
		currentList.append(beer['brewery_location'])
		currentList.append(beer['commercial_desc'].replace("COMMERCIAL DESCRIPTION ","").replace("\"","\'"))
		statList=parseStats(beer['stats'])
		for stat in statList:
			currentList.append(statToFloat(stat))
		reviewsList=splitReviews(beer['reviews'])
		for review in reviewsList:
			##create the new line
			for item in currentList:
				if isinstance(item, basestring):
					f.write("\""+item.encode('utf-8')+"\"\t")
				else:
					f.write("%.3f" % item)
					f.write("\t")
			parsedReview=parseReview(review)
			for x in range(0,len(parsedReview)):
				item = parsedReview[x]
				if isinstance(item, basestring):
					if x!=len(parsedReview)-1:
						f.write("\""+item.encode('utf-8').replace("\"","\'")+"\"\t")
					else:
						f.write("\""+item.encode('utf-8').replace("\"","\'")+"\"")
				else:
					f.write("%.3f" % item)
					if x!=len(parsedReview):
						f.write("\t")
			f.write("\n")
		
		
### columnnames=['beer_id','beer_name','brewer_name','beer_style','distribution','brewery_location','commercial_desc','RATINGS: ','MEAN', 'WEIGHTED AVG','EST. CALORIES', 'ABV', 'SCORE','IBU','AROMA', 'APPEARANCE','TASTE','PALATE','OVERALL','reviewer_name','review_location','review_date','review_content']
### recall namedStatsList=['RATINGS: ','MEAN: ', 'WEIGHTED AVG: ','EST. CALORIES: ', 'ABV: ', 'IBU: ']
### reviewStatsNames=['AROMA', 'APPEARANCE','TASTE','PALATE','OVERALL','reviewer_name','review_location','review_date','review_content']

for beer in beerList:
	beerNameDict[beer['beer_id']]=beer['beer_name']
	if isinstance(beer['brewer_name'], basestring):
		breweryDict[beer['beer_id']]=beer['brewer_name']
	else:
		breweryDict[beer['beer_id']]=beer['brewer_name'][0]
	styleDict[beer['beer_id']]=beer['beer_style']
	distributionDict[beer['beer_id']]=beer['distribution']
	try:
		locationDict[beer['brewer_name']]=beer['brewery_location']
	except TypeError:
		locationDict[beer['brewer_name'][0]]=beer['brewery_location']
		#print beer['beer_name'],beer['brewer_name'], beer['brewery_location']
	reviewsDict[beer['beer_id']]=splitReviews(beer['reviews'])
	commercialDescDict[beer['beer_id']]=beer['commercial_desc'].replace("COMMERCIAL DESCRIPTION ","")
	statsDict[beer['beer_id']]=parseStats(beer['stats'])

##Get this into a proper database format in separate csv files for each table	
###Brewery Table:
writeFile=writePath+"BreweryTable.csv"
BreweryList=list(set(breweryDict.values()))
BreweryIDs={}
with open(writeFile, "w") as f:
	for x in range(0,len(BreweryList)):
		BreweryIDs[BreweryList[x]]=x
		f.write("%d," % x)
		f.write("\""+BreweryList[x].encode('utf-8')+"\",\""+locationDict[BreweryList[x]].encode('utf-8')+"\"\n")

writeFile=writePath+"StyleTable.csv"
StyleList=list(set(styleDict.values()))
StyleIDs={}
with open(writeFile, "w") as f:
	for x in range(0,len(StyleList)):
		StyleIDs[StyleList[x]]=x
		f.write("%d," % x)
		f.write("\""+StyleList[x].encode('utf-8')+"\"\n")
		
writeFile=writePath+"DistributionTable.csv"
DistributionList=list(set(distributionDict.values()))
DistributionIDs={}
with open(writeFile, "w") as f:
	for x in range(0,len(DistributionList)):
		DistributionIDs[DistributionList[x]]=x
		f.write("%d," % x)
		f.write("\""+DistributionList[x].encode('utf-8')+"\"\n")

writeFile=writePath+"BeerTable.csv"
with open(writeFile, "w") as f:
	for beer in beerList:
		f.write(str(beer['beer_id']))
		f.write(",\"")
		f.write(beer['beer_name'].encode('utf-8'))
		f.write("\",")
		if isinstance(beer['brewer_name'], basestring):
			f.write("%d" % BreweryIDs[beer['brewer_name']])
		else:
			f.write("%d" % BreweryIDs[beer['brewer_name'][0]])
		f.write(",")
		f.write("%d" % StyleIDs[beer['beer_style']])
		f.write(",")
		f.write("%d" % DistributionIDs[beer['distribution']])
		f.write(",\"")
		f.write(beer['commercial_desc'].replace("COMMERCIAL DESCRIPTION ","").replace("\"","\'").encode('utf-8'))
		f.write("\",\"")
		##namedStatsList=['RATINGS: ','MEAN: ', 'WEIGHTED AVG: ','EST. CALORIES: ', 'ABV: ', 'IBU: ']
		statString=""
		for stat in parseStats(beer['stats']):
			stat = statToFloat(stat)
			if isinstance(stat, basestring):
				f.write("\""+stat+"\"")
			else:
				f.write("%.3f" % stat)
			f.write(",")
		#statString=statString[0:len(statString)-1]
		#f.write(statString.encode('utf-8'))
		f.write("\n")
writeFile=writePath+"ReviewTable.csv"
reviewCount=0
with open(writeFile, "w") as f:
	for beer in reviewsDict:
		for x in range(0,len(reviewsDict[beer])):
			reviewCount+=1
			f.write("%d," % reviewCount)
			f.write("%d," % beer)
			parsedReview=parseReview(reviewsDict[beer][x])
			for item in parsedReview:
				if isinstance(item,basestring):
					f.write("\""+item.encode('utf-8').replace("\"","\'")+"\",")
				else:
					f.write("%.3f" % item)
					f.write(",")
			f.write("\n")
			
#Use this to look at a sample of the file:
#readJson=json.loads(wholeThing)
#Stone RuinTen IPA
#with open(searchFile,'r') as f:
#	fart = f.readline().split("}")
#	for element in fart:
#		print element
#		a = raw_input()
