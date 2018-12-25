from PIL import Image
import predict_digit as predDigit

import readConfig
# import filterImage
import pytesseract
import json
import os
import sys


# Read all image from source folder
# rezie to standard 2480X3508 pixel
# save to a local folder
# read config file and get the init var values like location of various info on image
# read each image from local folder
# get mat number and page number from each image 
# 


# 
# read images from raw image dir, sanitize and save to the resized dir 
# as matNo_pageNo.png format if image ext is png. if not png drop image.
# 
totalPage = 14
a4size = (2480, 3508)
readFileCount = 0
unreadFileCount = 0
candidates = readConfig.getCandidatesMatNo()
rawPath = os.path.join(os.path.abspath('../'), 'raw_image')
resizedPath = os.path.join(os.path.abspath('../'), 'cleaned_image')
unreadImagePath = os.path.join(os.path.abspath('../'), 'unread_image')
images = os.listdir(rawPath)

for imageName in images:
	print(imageName)
	fileName = os.path.join(rawPath, imageName)
	im = Image.open(fileName)
	im = im.convert('L')
	im = im.resize(a4size)
	# im = filterImage.filterIm(im)
	matBox = readConfig.getMatNoLoc()
	region = im.crop(matBox)
	# matNo = pytesseract.image_to_string(region, lang= 'eng')


	matNo = predDigit.getMatNum()

	# print(type(matNo))
	print(matNo)
	# sys.exit()
	if (matNo not in candidates):
		print('Mat number not in candidates list. handle excepton')
		im.save(os.path.join(unreadImagePath, imageName))
		unreadFileCount += 1
	else:
		pBox = readConfig.getPageNoLoc()
		region = im.crop(pBox)
		page = pytesseract.image_to_string(region, lang= 'eng')
		page = page.split()
		try:
			pageNo = page[1]
		except:
			pageNo = str(0)
		print('Page number: ' + pageNo)
		if(int(pageNo) not in list(range(1,totalPage))):
			print('page number not in range. handle exception..')
			im.save(os.path.join(unreadImagePath, imageName))
			unreadFileCount += 1
		else:
			imName, imExt = imageName.split('.')
			if(imExt.lower() == 'png' or 'jpg'):
				newFileName = matNo + '_' + pageNo + '.' + imExt
				im.save(os.path.join(resizedPath, newFileName))
				readFileCount += 1		
print(str(readFileCount) + ' files copied to resized dir')
print(str(unreadFileCount) + ' files couldn\'t read. copied to unread dir')
# 
# read images from resized dir, fetch text as per question no 
# save text to file
print('Reading answer sheets....')
studentsAns = []
questionsLoc = readConfig.getQuestionsLoc()
cleanImages = os.listdir(resizedPath)
for image in cleanImages:
	matNo, pageNo = image.split('_')
	pageNo, ext = pageNo.split('.')
	imageName = os.path.join(resizedPath, image)
	im = Image.open(imageName)
	for question in questionsLoc:
		if(question[1] == pageNo ):
			questionNo = question[0]
			region = im.crop(question[2:])			
			ans = pytesseract.image_to_string(region, lang= 'eng')
			ans = ans.replace('\n', ' ')
			studentsAns.append([matNo, questionNo, ans])
			

	
with open('../studentAns.json', 'w') as outfile:
	json.dump(studentsAns, outfile)
print('Answers saved successfully.')
sys.exit("---intentional exit---")




