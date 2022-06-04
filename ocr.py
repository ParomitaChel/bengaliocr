# # try:
# #     from PIL import Image
# #     import cv2
# # except ImportError:
# import cv2
# from PIL import Image
# # import Image
# import pytesseract
# import numpy as np
#
# def ocr_core(filename):
#     """
#     This function will handle the core OCR processing of images.
#     """
#     pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
#     # img = Image.open(filename)
#     # img = cv2.imread(filename['filename'])
#     gray_img = cv2.cvtColor(Image.open(filename), cv2.COLOR_BGR2GRAY)
#     binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
#     custom_config = r'--oem 3 --psm 6'
#     text = pytesseract.image_to_data(binary_img, output_type=pytesseract.Output.DICT, config=custom_config, lang='ben')
#     # text = pytesseract.image_to_string(Image.open(filename) , lang='ben')
#     return text
#
# print(ocr_core('test1.png'))

import string
from cv2 import data
import os
from flask import send_file
import numpy as np

from pdf2image import convert_from_path
from pdf_info import pdf_info_class

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from collections import Counter

from array import array

result_ocr_data = ""
global result_ocr

result_ocr = ""


def SerachString(mainmsg, submsg):
    word_counter = 1

    lines = mainmsg.split("\n")
    for line_number in range(0, mainmsg.count("\n") + 1):
        word_counter = 1
        words = lines[line_number].split(" ")
        for temp in words:
            if temp == submsg:
                StrSD = "Found At Line:" + str(line_number + 1) + " Word Number:" + str(word_counter)
                # return StrSD,mainmsg.replace(submsg,"<font color=" + chr(34) + "red" + chr(34) + ">" + submsg + "</font>")
                return StrSD
            if temp == "|":
                word_counter = word_counter
            else:
                word_counter += 1
    return "Not Found"


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    global result_ocr

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract- OCR\tesseract.exe"
    custom_config = r'--oem 3 --psm 6'

    print(str(filename.filename).find(".pdf"))
    if str(filename.filename).find(".pdf") == -1:
        img_info = pytesseract.image_to_data(Image.open(filename), output_type=pytesseract.Output.DICT,
                                             config=custom_config, lang='ben')

        def parse(data):

            parsed = []
            last_word = ''
            for word in data:
                if word != '':
                    parsed.append(word)
                    last_word = word
                if last_word != '' and word == '':
                    parsed.append('\n')

            return " ".join(parsed)

        data = parse(img_info['text'])
        file = open('data/image_result.txt', 'w', encoding='utf-8')
        file.write(data)
        file.close()

        PDF = pytesseract.image_to_pdf_or_hocr(Image.open(filename), lang='ben', config='', nice=0, extension='pdf')
        with open('test.pdf', 'w+b') as f:
            f.write(PDF)

    if (str(filename.filename)).find(".pdf") > 0:

        text = pdf_to_text_ben(str(".\\static\\uploads\\" + filename.filename))
        file = open('data/image_result.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()
    else:
        text = pytesseract.image_to_string(Image.open(filename), config=custom_config, lang='ben')

    result_ocr = ""
    result_ocr += "  Number of words:: " + str(len(text.split()))
    result_ocr += "  Number of lines:: " + str(text.count('\n'))
    wordstring = text

    wordlist = wordstring.split()

    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))

      # result_ocr += str(list(zip(wordlist, wordfreq)))

    result_ocr += "Frequency of each word:: \n " + str(dict(zip(wordlist, wordfreq)))

    # SearchPos=  text.find("?????")

    return text


def pdf_to_text_ben(filePath):
    txt = ''
    doc = convert_from_path(filePath, poppler_path=r'.\poppler-0.68.0\bin')
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)

    for page_number, page_data in enumerate(doc):
        txt += pytesseract.image_to_string(Image.fromarray(np.array(page_data)), lang='ben')
    return txt


def ardument_pass():
    global result_ocr

    return result_ocr


def word_frequency_with_search(mainmsg, submsg):
    val = submsg
    return_string = ""
    x = mainmsg.count(val)
    if x > 0:
        return_string = f"\nThe {val} is in the file and {val} is available in the list {x} times."
    else:
        return_string = f"{val} is not available in the file"
    return return_string

# print(ocr_core('test2.jpg'))
