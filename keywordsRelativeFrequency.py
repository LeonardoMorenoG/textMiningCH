import sys
import os
import re
import pandas as pd

def pdf2txt(path):
	os.system("pdf2txt.py "+path+" > paper.txt")

def removePunctuation(line):
	return re.sub(r'[^\w\s]','',line)

def readKeywordsFile(filePath):
	keywords = {}
	with open(filePath,"r") as fr:
		for line in fr:
			line = line.strip('\n').split('\t')
			keywords[line[0]] = line[1:]
	return keywords

def keywordsDict2keywordsTable(keywordsDict):
	columns = []
	for category in keywords:
		columns += keywords[category]
	columns.append("textLength")
	return pd.DataFrame(columns=columns)

#1. Import the "Topics and keywords" and keywords intersection files
keywords = readKeywordsFile(sys.argv[1])
overlap = readKeywordsFile(sys.argv[2])
folder = sys.argv[3]

catPerYear = pd.DataFrame(columns=list(keywords.keys()),index=os.listdir(folder))
for year in os.listdir(folder):
	freqTable = keywordsDict2keywordsTable(keywords)
	for pdf in os.listdir(folder+year):
		#2. Read a PDF file
		pdf2txt(folder+year+"/"+pdf)
		text = ""
		with open('paper.txt','r') as fr:
			for line in fr:
				text += removePunctuation(line.lower())
		#3. Get the keyword's frequency in the PDF
		frequency = {}
		for category in keywords:
			for keyword in keywords[category]:
				frequency[keyword] = text.count(keyword)

		#4. Rest the frequency of the overlapping words
		for keyword in overlap:
			sumX = 0 # sum of the frequencies of the words that overlap with the keyword
			for x in overlap[keyword]: #x: a word that overlaps with a keyword
				sumX += frequency[x]
			frequency[keyword] = frequency[keyword] - sumX

		#5. Save the PDF frequency results in the frequency table
		frequency["textLength"] = len(text.split(' '))
		freqTable = freqTable.append(frequency,ignore_index=True)
	#6.Get the frequency per category
	totalWords = freqTable["textLength"].sum()
	for category in keywords:
		catFreqValues = freqTable[keywords[category]]
		catTotalFreq = catFreqValues.sum(axis=0).sum()
		if catTotalFreq > 0:
			numKewordsFound = sum(catFreqValues.sum(axis=0) > 0)
			normalizedFreq = catTotalFreq/(numKewordsFound*totalWords)
			catPerYear[category][year] = normalizedFreq
		else:
			catPerYear[category][year] = 0
catPerYear.T.to_csv("NormalizedRelativeFrequency.csv",header=True,index=True,sep='\t')
#Make another code to plot the final DataFrame

#Execute it like python keywordsRelativeFrequency.py keywordsTable.csv keywordsIntersection.csv PapersFolder










