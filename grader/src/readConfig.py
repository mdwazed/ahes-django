from django.conf import settings
import json
import os

# fileName = os.path.join(os.pardir, 'config.json')
fileName = os.path.join(settings.BASE_DIR, 'grader/config.json')
# print(fileName)
with open (fileName, 'r') as file:
	configData = json.load(file)

def getMatNoLoc():	
	return configData['matNo']

def getPageNoLoc():
	return configData['pageNo']

def getQuestionsLoc():
	return configData['questionList']

def getCandidatesmat_number():
	return configData['candidatesMatNo']

if __name__ == "__main__":
	print(getMatNoLoc())
	print(getPageNoLoc())
	print(getQuestionsLoc())
	print(getCandidatesMatNo())