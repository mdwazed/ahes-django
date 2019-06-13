"""
# Read all images from raw image dir
# resize and denoise them
# save them in resized folder or in unread folder
# read students ans and save ans to json file as per mat and quesno
update: save ans in db

"""

from django.conf import settings
from django.shortcuts import get_list_or_404
from grader.models import PageParameter, StudentAns
from grader.helper import ansScriptReader, clean_image_page_no_region
from configq.models import Question
from configq.misc_function import get_exam

from PIL import Image, ImageFilter
import grader.src.predict_digit as predDigit

from grader.src import readConfig
# import filterImage
import logging
import pytesseract
import json
import os
import sys
import csv

class ansScript:
    def __init__(self):
        # self.candidates = ['2488853', '2488854', '2488855', '2488856', '1484854', '2486855', '2487853', '2487856']
        # self.candidates = readConfig.getCandidatesmat_number()
        self.candidates = self.get_attendes()
        # print(self.candidates)
        self.totalPage = 20
        self.a4size = (2480, 3508)
        self.readFileCount = 0
        self.unreadFileCount = 0
        
        self.rawPath = os.path.join(settings.BASE_DIR, 'media/raw_image')
        self.cleanedPath = os.path.join(settings.BASE_DIR, 'media/cleaned_image')
        self.unreadImagePath = os.path.join(settings.BASE_DIR, 'media/unread_image')

    def processAnsScript(self, request):
        """
        read all images of current exam from raw_image dir. 
        resize them to std a4 size.
        moved them to cleaned_image dir for further processing.
        """
        images = os.listdir(self.rawPath)# get this list from db query when images will be uploaded through django

        for imageName in images:
            print('new iter',imageName)
            try:
                im_exam_id, im_mat_nr, name = imageName.split('_')
                im_page_nr, im_ext = name.split('.')
            except Exception as e:                
                print('problem spliting image name in processAnsScript' + str(e))
            if(im_exam_id != str(get_exam(request).id)):
                print('exam_id mismatch') 
                continue

            fileName = os.path.join(self.rawPath, imageName)
            with Image.open(fileName) as im:
                # im = Image.open(fileName)
                # im = im.convert('L')
                im = im.resize(self.a4size)
            
                if int(im_page_nr) not in range(1,self.totalPage):
                    # move this page to unread image dir, delete image from raw dir and continue to next iteration
                    self.move_image_to_unread_image(imageName, im)
                    # to be done- delete the image from the raw dir
                    print('im_page_nr not in range' + im_page_nr )
                    continue
            

                if (im_mat_nr not in self.candidates):
                    print('Mat number not in candidates list. handle excepton')
                    self.move_image_to_unread_image(imageName, im)
                    print('im_mat_nr not in candidate list')
                    continue
                self.move_image_to_cleaned_image(request, imageName, im, im_mat_nr, im_page_nr)
            
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
                    # ##################################
                    # ### change API here ##############
                    # ################################## 
                    try:
                        print(f"reading question no:{questionNo} from region {region}")
                        ans = pytesseract.image_to_string(region, lang= 'deu')
                    except Exception as e:
                        print(f"failed to read question no {questionNo}. error:{str(e)}")
                    # ans = pytesseract.image_to_string(region, lang= 'ger')
                    ans = ans.replace('\n', ' ')
                    student_ans = StudentAns(
                        exam=current_exam,
                        matriculation_num=mat_number,
                        question_num=questionNo,
                        students_ans= ans,
                    )
                    
                    student_ans.save() ### save students ans to dbase
                    print(student_ans)

                    # studentsAns.append([mat_number, questionNo, ans]) # append student ans in studentAns.json
                    

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
            
    def get_attendes(self):
        print('getting attendees')
        mat_nr_list = []
        fileName = os.path.join(settings.BASE_DIR, 'grader/src/mat_nr.csv')
        with open(fileName,'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                for num in row:
                    new_num = num.strip()
                    mat_nr_list.append(new_num)
        return mat_nr_list

        
if __name__ == "__main__":
    ansc = ansScript()
    # ansc.processAnsScript()
    # ansc.readAns()
    ansc.get_attendes()