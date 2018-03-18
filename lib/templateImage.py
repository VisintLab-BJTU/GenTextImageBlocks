#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Wenyuan Xue
# --------------------------------------------------------

import os
from os.path import join as osj
import logging
import numpy as np
import cv2
import IOUtils as IOUtils
import ImageUtils as ImageUtils

logging.basicConfig(level=logging.INFO)

class TemplateImage(object):
    def __init__(self, pathImage):
        self.pathToTemplateImages = pathImage
        assert os.path.exists(self.pathToTemplateImages), \
        'TemplateImage path does not exist: {}'.format(self.pathToTemplateImages)
        self.meanStds = self.ComputeMeanStds()

    def ComputeMeanStds(self):
        meanStds = []
        imagesList = IOUtils.GetFilesList(self.pathToTemplateImages)
        logging.info("Done. Load all template images: "+str(len(imagesList)))
        count = 0
        for imageName in imagesList:
            count += 1;
            if count % 10 == 0:
                logging.info("Processing. Compute mean & std: "+str(count))
            img = cv2.imread(osj(self.pathToTemplateImages,imageName))
            meanPre, stdPre, meanBack, stdBack = self.ComputeMeanStd(img)
            if(np.abs(meanPre-meanBack)<30):
                logging.warning("Processing. The values of background and foreground are close: %f", np.abs(meanPre-meanBack))
            tempmeanStd = [meanPre, stdPre, meanBack, stdBack]
            meanStds.append(tempmeanStd)
        return meanStds

    def ComputeMeanStd(self,img):
        gray = np.zeros((3,3),dtype=np.uint8)
        if ImageUtils.IsGrayImage(img):
            gray = img.copy()
            gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        else:
            gray = ImageUtils.GrayImage(img)
        th, binGray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blurBin = cv2.blur(binGray, (5,5))
        meanPre, stddevPre = ImageUtils.GetMeanStd(gray, binGray, 'pre')
        meanBack, stddevBack = ImageUtils.GetMeanStd(gray, binGray, 'back')
        return meanPre, stddevPre, meanBack, stddevBack

    def SaveMeanStd(self,savePath):
        f = open(savePath,'w')
        for valueList in self.meanStds:
            for value in valueList:
                f.write(str(value)+' ')
            f.write("\n")
        f.close()
        logging.info("Finish. %d templates information have been saved successfully.", len(self.meanStds))
        return True
