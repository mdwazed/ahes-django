
import pytesseract
from PIL import Image, ImageFilter
import cv2 as cv
import numpy as np


def clean_image_page_no_region(im):
    im =np.array(im)

    ret,im = cv.threshold(im,180,255,cv.THRESH_TOZERO)
    # im = cv.medianBlur(im, 3)
    kernel = np.ones((3,3),np.float32)/9
    im = cv.filter2D(im,-1,kernel)
    im = cv.filter2D(im,-1,kernel)
    # im = cv.bilateralFilter(im,9,75,75)
    # ret,im = cv.threshold(im,150,255,cv.THRESH_TOZERO)
    # im = cv.medianBlur(im, 3)
    im = Image.fromarray(im)
    return im


class ansScriptReader(object):
    def __init__(self, pages_parameters):
        self.pages_parameters = pages_parameters

    def read_page_number(self, ans_script_img):
        #extract pagr number location from page parameter
        top_left_x = self.pages_parameters[0].page_no_top_left_x
        top_left_y = self.pages_parameters[0].page_no_top_left_y
        bottom_right_x = self.pages_parameters[0].page_no_bottom_right_x
        bottom_right_y = self.pages_parameters[0].page_no_bottom_right_y
        page_no_box_coord = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        # print(page_no_box_coord)
        #extract page number 
        img = ans_script_img.crop(page_no_box_coord)
        img = clean_image_page_no_region(img)
        # cropped_image.show()
        page_num = pytesseract.image_to_string(img, lang= 'eng')
        print('raw page:', page_num)
        page_num = page_num.split()
        try:
            pageNo = int(page_num[1])
            
        except:
            pageNo = 0
        return pageNo
        
    def get_mat_number_locs_tuple(self, page_num):
        print('getting mat num loc tuples')
        for page_parameter in self.pages_parameters:            
            if(page_parameter.upload_question.page == page_num):
                
                first_digit = (
                        page_parameter.mat_digit_1_top_left_x,
                        page_parameter.mat_digit_1_top_left_y,
                        page_parameter.mat_digit_1_bottom_right_x,
                        page_parameter.mat_digit_1_bottom_right_y
                    )
                second_digit = (
                        page_parameter.mat_digit_2_top_left_x,
                        page_parameter.mat_digit_2_top_left_y,
                        page_parameter.mat_digit_2_bottom_right_x,
                        page_parameter.mat_digit_2_bottom_right_y
                    )
                third_digit = (
                        page_parameter.mat_digit_3_top_left_x,
                        page_parameter.mat_digit_3_top_left_y,
                        page_parameter.mat_digit_3_bottom_right_x,
                        page_parameter.mat_digit_3_bottom_right_y
                    )
                fourth_digit = (
                        page_parameter.mat_digit_4_top_left_x,
                        page_parameter.mat_digit_4_top_left_y,
                        page_parameter.mat_digit_4_bottom_right_x,
                        page_parameter.mat_digit_4_bottom_right_y
                    )
                fifth_digit = (
                        page_parameter.mat_digit_5_top_left_x,
                        page_parameter.mat_digit_5_top_left_y,
                        page_parameter.mat_digit_5_bottom_right_x,
                        page_parameter.mat_digit_5_bottom_right_y
                    )
                sixth_digit = (
                        page_parameter.mat_digit_6_top_left_x,
                        page_parameter.mat_digit_6_top_left_y,
                        page_parameter.mat_digit_6_bottom_right_x,
                        page_parameter.mat_digit_6_bottom_right_y
                    )
                seventh_digit = (
                        page_parameter.mat_digit_7_top_left_x,
                        page_parameter.mat_digit_7_top_left_y,
                        page_parameter.mat_digit_7_bottom_right_x,
                        page_parameter.mat_digit_7_bottom_right_y
                    )
                mat_box_list = [
                    first_digit,
                    second_digit,
                    third_digit,
                    fourth_digit,
                    fifth_digit,
                    sixth_digit,
                    seventh_digit,
                ]
                return mat_box_list



