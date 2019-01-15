from django.conf import settings
from django.shortcuts import get_list_or_404
from grader.models import PageParameter, StudentAns
from grader.helper import ansScriptReader, clean_image_page_no_region
from configq.models import Question
from configq.misc_function import get_exam
# Read all images from raw image dir
# resize and denoise them
# save them in resized folder or in unread folder
# read students ans and save ans to json file as per mat and quesno
from PIL import Image, ImageFilter
import grader.src.predict_digit as predDigit

from grader.src import readConfig
# import filterImage
import logging
import pytesseract
import json
import os
import sys

class ansScript:
	def __init__(self):
		self.totalPage = 14
		self.a4size = (2480, 3508)
		self.readFileCount = 0
		self.unreadFileCount = 0
		self.candidates = readConfig.getCandidatesmat_number()
		self.rawPath = os.path.join(settings.BASE_DIR, 'media/raw_image')
		self.cleanedPath = os.path.join(settings.BASE_DIR, 'media/cleaned_image')
		self.unreadImagePath = os.path.join(settings.BASE_DIR, 'media/unread_image')

	# read all ans script, process and save 
	def processAnsScript(self, request):
		images = os.listdir(self.rawPath)# get this list from db query when images will be uploaded through django

		for imageName in images:
			print('new iter',imageName)
			try:
				pre, name = imageName.split('_')
			except ValueError:
				pre = 0
				print('image name doesn\'t contain _' )
			if(pre != str(get_exam(request).id)):				
				continue

			fileName = os.path.join(self.rawPath, imageName)
			with Image.open(fileName) as im:
				# im = Image.open(fileName)
				im = im.convert('L')
				im = im.resize(self.a4size)
				# print('image resized')
				# im = clean_image(im)

	            ########### can be useful if stamp based mat num is agreed upon ##################
				# get matriculation num region            
				# matBox = readConfig.getmat_numberLoc()
				# region = im.crop(matBox)
				# region.show()
				# sys.exit()
				
				# predict mat num with pytesseract
				# mat_number = pytesseract.image_to_string(region, lang= 'eng')
				## all config data of all pages of this exam
				pages_parameters = get_list_or_404(PageParameter, upload_question__exam=get_exam(request)) 
				# print(pages_parameters)

					
				reader = ansScriptReader(pages_parameters)
				page_number = reader.read_page_number(im)
				print('page number:', page_number)
				if page_number not in range(1,20):
					# move this page to unread image dir, delete image from raw dir and continue to next iteration
					self.move_image_to_unread_image(imageName, im)
					# to be done- delete the image from the raw dir

					continue
				# matBox = readConfig.getmat_numberLoc()
				# region = im.crop(matBox)
				# region.show()
				# sys.exit()

				# get mat num from trained model
				mat_locs_tuples = reader.get_mat_number_locs_tuple(page_number)
				# print(mat_locs_tuples)
				try:
					mat_number = predDigit.getMatNum(im, mat_locs_tuples)
				except Exception as e:
					print('prob reading mat num:', str(e))
					self.move_image_to_unread_image(imageName, im)
					continue
				print('mat number:', mat_number)
				# print(self.candidates)
				# print(mat_number)
				# sys.exit()
				# print(type(mat_number))
				# print(mat_number)
				# sys.exit('---exit from preprocessAnsScript----')
				if (mat_number not in self.candidates):
					print('Mat number not in candidates list. handle excepton')
					self.move_image_to_unread_image(imageName, im)
					continue
				self.move_image_to_cleaned_image(request, imageName, im, mat_number, page_number)
				# else:
				# 	pBox = readConfig.getPageNoLoc()
				# 	region = im.crop(pBox)
				# 	# region.show()
				# 	# sys.exit('exit from page num')
				# 	page_num = pytesseract.image_to_string(region, lang= 'eng')
				# 	page_num = page_num.split()
				# 	try:
				# 		pageNo = page_num[1]
				# 	except:
				# 		pageNo = str(0)
				# 	print('Page number: ' + pageNo)
				# 	if(int(pageNo) not in list(range(1,self.totalPage))):
				# 		print('page number not in range. handle exception..')
				# 		im.save(os.path.join(self.unreadImagePath, imageName))
				# 		self.unreadFileCount += 1
				# 	else:
				# current_exam = get_exam(request)
				# exam_id = str(current_exam.id)
				# imName, imExt = imageName.split('.')
				# if(imExt.lower() == 'png' or 'jpg'):
				# 	newFileName = exam_id+'_'+mat_number + '_' + str(page_number) + '.' + imExt
				# 	im.save(os.path.join(self.cleanedPath, newFileName))
				# 	self.readFileCount += 1		
				# print('image processed')
		print(str(self.readFileCount) + ' files copied to cleaned dir')
		print(str(self.unreadFileCount) + ' files couldn\'t read. copied to unread dir')
		return (self.readFileCount, self.unreadFileCount)

	def readAns(self, request):
		"""
		scan all cleaned image, read student ans and save the ans to data base
		"""
		print('Reading answer sheets....')
		current_exam = get_exam(request)
		current_exam_id = str(current_exam.id)
		studentsAns = []
		# get all question with loc 
		questions = get_list_or_404(Question, exam=get_exam(request))
		# print(questions)
		questions_loc = [(q.question_number, q.page, q.topLeftX, q.topLeftY, q.bottomRightX, q.bottomRightY)for q in questions]
		# print(questions_loc)
		# questionsLoc = readConfig.getQuestionsLoc()
		# questionLoc=== [['question_no', 'page_no', 'leftx', 'left top', right x, 'right top'],[]]
		cleanImages = os.listdir(self.cleanedPath)
		for image in cleanImages:
			exam_id, mat_number, page_number = image.split('_')
			page_number, ext = page_number.split('.')
			# imageName = os.path.join(self.cleanedPath, image)
			im = Image.open(os.path.join(self.cleanedPath, image))
			for question in questions_loc:
				# print('page num'+page_number)
				# print('page num'+str(question[1]))
				if(question[1] == int(page_number) and exam_id == current_exam_id):
					# print('matched page:'+ page_number)
					questionNo = question[0]
					region = im.crop(question[2:])	
					# region.show()	
					# sys.exit()	
					ans = pytesseract.image_to_string(region, lang= 'eng')
					ans = ans.replace('\n', ' ')
					student_ans = StudentAns(
						exam=current_exam,
						matriculation_num=mat_number,
						question_num=questionNo,
						students_ans= ans,
					)

					student_ans.save() ### save students ans to dbase

					studentsAns.append([mat_number, questionNo, ans])
					

		student_ans_file = os.path.join(settings.BASE_DIR, 'studentAns.json')
		with open(student_ans_file, 'w') as outfile:
			json.dump(studentsAns, outfile)
		print('Answers saved successfully.')


	def move_image_to_cleaned_image(self, request, imageName, im, mat_number, page_number):
		exam_id = get_exam(request).id		
		imName, imExt = imageName.split('.')
		if(imExt.lower() == 'png' or 'jpg'):
			newFileName = str(exam_id)+'_'+ mat_number + '_' + str(page_number) + '.' + imExt
			im.save(os.path.join(self.cleanedPath, newFileName))
			#delete image from the raw_image folder
			os.remove(os.path.join(self.rawPath, imageName))
			self.readFileCount += 1
		else:
			print('image must be png or jpg.')
			self.move_image_to_unread_image(imageName, im)

	def move_image_to_unread_image(self, imageName, im):
		im.save(os.path.join(self.unreadImagePath, imageName))
		#delete image from the raw_image folder
		os.remove(os.path.join(self.rawPath, imageName))
		self.unreadFileCount += 1
            
if __name__ == "__main__":
	ansc = ansScript()
	ansc.processAnsScript()
	ansc.readAns()

