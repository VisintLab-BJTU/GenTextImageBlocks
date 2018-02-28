
import cv2
import os
import lib.Test_IOUtils as IOUtils
import lib.Test_ImageUtils as ImageUtils
from lib.templateImage import TemplateImage

def GenerateBinImages():

    return 0

def FromBinToGaussImages():

    return 0

if __name__ == '__main__':
    template = TemplateImage("./myData/srcData")
    template.SaveMeanStd("./myData/template.txt")
    GenerateBinImages()
    FromBinToGaussImages()
    print('Done.')
