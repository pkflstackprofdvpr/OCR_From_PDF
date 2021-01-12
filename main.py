#coding:utf8
# importing modules
import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import csv


def convertPDF2Images(pdffile, output='data/'):
    '''
    Part #1 : Converting PDF to images
    '''
    #
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(pdffile, 500)
    #
    # Counter to store images of each page of PDF to image
    image_counter = 1
    #
    # Iterate through all the pages stored above
    for page in pages:
        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = output + "page_" + str(image_counter) + ".jpg"

        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    return image_counter



# Path of the pdf
# PDF_file = "Arabic English Legal Dictionary (Book 1).pdf"
PDF_file = "Arabic file with editable text.pdf"
data_dir = "data/"

image_counter = convertPDF2Images(PDF_file, data_dir)

# Open the file in append mode so that
# All contents of all images are added to the same file
outfile = data_dir + "out_text.txt"

f = open(outfile, "a", encoding="utf-8")
filelimit = image_counter - 1
# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):
    # Set filename to recognize text from
    # Again, these files will be:
    # page_1.jpg
    # page_2.jpg
    # ....
    # page_n.jpg
    print("Processing >> Page " + str(i))
    filename = data_dir + "page_" + str(i) + ".jpg"

    # reading image using opencv
    image = cv2.imread(filename)
    # converting image into gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # converting it to binary image by Thresholding
    # this step is require if you have colored image because if you skip this part
    # then tesseract won't able to detect text correctly and this will give incorrect result
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # configuring parameters for tesseract
    custom_config = r'--oem 3 --psm 6'
    # now feeding image to tesseract
    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng+ara')
    # print(details.keys())

    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == details['text'][-1]):
            parse_text.append(word_list)
            word_list = []


    outfilename = data_dir + "page_" + str(i) + ".txt"

    # with io.open('arabic.csv','w',encoding='utf-8-sig') as f:
    # with open('data/result_text.txt', 'w', newline="", encoding="utf-8-sig") as file:
    # with open(outfilename, 'w', newline="", encoding="utf-8-sig") as file:
    #     csv.writer(file, delimiter=" ").writerows(parse_text)
    with open(outfile, 'a', newline="", encoding="utf-8-sig") as file:
        csv.writer(file, delimiter=" ").writerows(['--------Page' + str(i) + '-----------'])
        csv.writer(file, delimiter=" ").writerows(parse_text)
