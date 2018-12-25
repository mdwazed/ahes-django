from django.conf import settings

# Copyright 2016 Niek Temme. 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Predict a handwritten integer (MNIST expert).

Script requires
1) saved model (model2.ckpt file) in the same location as the script is run from.
(requried a model created in the MNIST expert tutorial)
2) one argument (png file location of a handwritten integer)

Documentation at:
http://niektemme.com/ @@to do
"""

#import modules
import os
import sys
import tensorflow as tf
from PIL import Image, ImageFilter
import cv2 as cv



def predictint(imvalues):
    """
    This function returns the predicted integer.
    The imput is the pixel values from the imageprepare() function.
    """
    trained_model_path = os.path.join(settings.BASE_DIR, 'grader/src/trained_model/model2.ckpt')
    # reset the graph so it load the saved model for each set of mat num
    tf.reset_default_graph()
    
    # Define the model (same as when creating the model file)
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    
    def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)
    
    def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)
       
    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
    
    def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')   
    
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    
    x_image = tf.reshape(x, [-1,28,28,1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    
    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
    
    # init_op = tf.initialize_all_variables()
    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    """
    Load the model2.ckpt file
    file is stored in the same directory as this python script is started
    Use the model to predict the integer. Integer is returend as list.

    Based on the documentatoin at
    https://www.tensorflow.org/versions/master/how_tos/variables/index.html
    """

    predictValues = []
    with tf.Session() as sess:
        sess.run(init_op)
        # saver.restore(sess, "trained_model/model2.ckpt")
        saver.restore(sess, trained_model_path)
        #print ("Model restored.")
       
        prediction=tf.argmax(y_conv,1)
        for imvalue in imvalues:
            predictVal = prediction.eval(feed_dict={x: [imvalue],keep_prob: 1.0}, session=sess)
            # print(predictVal)
            predictValues.append(predictVal)
        return predictValues


def imageprepare(argv):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    # im = Image.open(argv).convert('L')
    # print(im)
    im = argv
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255)) #creates white canvas of 28x28 pixels
    
    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0/width*height),0)) #resize height according to ratio width
        if (nheigth == 0): #rare case but minimum is 1 pixel
            nheigth = 1  
        # resize and sharpen
        img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (4, wtop)) #paste resized image on white canvas
    else:
        #Height is bigger. Heigth becomes 20 pixels. 
        nwidth = int(round((20.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
         # resize and sharpen
        img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0)) #caculate vertical pozition
        newImage.paste(img, (wleft, 4)) #paste resized image on white canvas
    
    # newImage.save("sample.png")

    tv = list(newImage.getdata()) #get pixel values
    
    #normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [ (255-x)*1.0/255.0 for x in tv] 
    # print(len(tva))
    return tva
    
def getMatNum(im, mat_locs_tuples):
    print('getting mat num')
    
    # imCorners = [1553, 1641, 1723, 1795, 1870, 1931, 1996]    
    # boxWidth = 46
    # boxHeight = 50    
    # imY = 295

    
    # imCorners = [0, 125, 240, 365, 490, 610, 730]
    # boxWidth = 110
    # boxHeight = 110
    # imY = 0


    imList = []
    cleanImList = []
    imCorners = mat_locs_tuples
    for boxCorner in imCorners:
        # box = [boxCorner, imY, boxCorner+boxWidth, imY+boxHeight,]
        box=boxCorner
        croppedIm = im.crop(box)
        # threshold = 130
        # croppedIm= croppedIm.point(lambda p: p > threshold and 255)          
        imList.append(croppedIm)

    # imList[6].show()
    # sys.exit('---myexit---')
    # im = cv.imread('../raw_image/img1.png', 0)

    # for boxCorner in imCorners:
    #     # box = [boxCorner, imY, boxCorner+boxWidth, imY+boxHeight,]
    #     # print(box)
    #     img = im[imY:imY+boxHeight, boxCorner:boxCorner+boxWidth] 
    #     img = cv.resize(img, (28, 28), interpolation = cv.INTER_LINEAR)
    #     # img = cv.medianBlur(img,3)
    #     img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 2)
    #     # print(img)
    #     img = cv.medianBlur(img,3)
    #     img = cv.medianBlur(img,3)

    #     img = Image.fromarray(img)
    #     imList.append(img) 
         

    for im in imList:
        # im.show()
        cleanImage = imageprepare(im)
        cleanImList.append(cleanImage)
    matNoDigit = predictint(cleanImList)
    matNo = [digit[0] for digit in matNoDigit]
    matNo = ''.join(str(i) for i in matNo)
    return matNo

    # predictedValue = predictint(cleanImList)
    # for value in predictedValue:
    #     print(value[0])


    
if __name__ == "__main__":    
    im = Image.open('../image_bak/abc.jpg')
    # predictedNum = getMatNum(im)
    # print(predictedNum)
    imVal = imageprepare(im)
    predictedNum = predictint(imVal)
