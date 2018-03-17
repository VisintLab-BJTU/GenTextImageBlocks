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
import random
import numpy as np
import cv2
import Test_IOUtils as IOUtils
import Test_ImageUtils as ImageUtils
from font import FT
from imgaug import augmenters as iaa

class TextImageBlockGenerater(object):
    def __init__(self, fontPath, dictPath, scales, degrees,templatePath=""):
        self.fontList = [osj(fontPath, font) for font in IOUtils.GetFilesList(fontPath)]
        self.scales = scales
        self.degrees = degrees
        self.charDict = self.LoadDict(dictPath)
        self.parms = self.GenParms()
        self.hasTemplate = False
        if len(templatePath)!=0:
            self.hasTemplate = True
            self.templates = self.LoadTemplate(templatePath)

    def LoadDict(self, dictPath):
        f = open(dictPath,'r')
        dictText = f.read()
        dictText = unicode(dictText, 'utf-8')
        dictText = dictText.strip('\n').split('\n')
        charDict = {0:' '}
        for line in dictText:
            line = line.replace('\n','').replace('\r','').strip(' ').split(' ')
            charDict[int(line[0])] = line[1]
        return charDict

    def LoadTemplate(self, templatePath):
        f = open(templatePath,'r')
        templateText = f.read().strip('\n').split('\n')
        templateList = []
        for line in templateText:
            line = line.replace('\n','').replace('\r','').strip(' ').split(' ')
            templateList.append((float(line[0]),min(20.0,float(line[1])),float(line[2]),min(10.0,float(line[3]))))
        return templateList

    def GenParms(self):
        parms = []
        for font in self.fontList:
            for scale in self.scales:
                for degree in self.degrees:
                    parm = {}
                    parm['font'] = font
                    parm['degree'] = degree
                    parm['scale'] = scale
                    parm['height'] = 32
                    parm['width'] = 32
                    parms.append(parm)
        return parms

    def AddGaussianNoise(self, srcImg):
        rows = srcImg.shape[0]
        cols = srcImg.shape[1]
        templatesSize = len(self.templates)
        meanFore,stddevFore,meanBack,stddevBack = self.templates[random.randint(0, templatesSize-1)]
        foreTemplate = np.random.normal(meanFore, stddevFore,(rows,cols)).astype(np.uint8)
        backTemplate = np.random.normal(meanBack, stddevBack,(rows,cols)).astype(np.uint8)
        noiseImage = np.zeros((rows,cols), dtype=np.uint8)

        binImg = ImageUtils.BinImage(srcImg)

        for indRow in range(rows):
            for indCol in range(cols):
                if binImg[indRow,indCol] == 255:
                    noiseImage[indRow,indCol] = backTemplate[indRow,indCol]
                else:
                    noiseImage[indRow,indCol] = foreTemplate[indRow,indCol]

        noiseImage = cv2.cvtColor(noiseImage,cv2.COLOR_GRAY2RGB)
        return noiseImage

    def ImageAug(self, srcImg):
        seq = iaa.Sequential([
            iaa.AdditiveGaussianNoise(scale=(0.1, 0.2*255),per_channel=0.5),
            iaa.Grayscale(alpha=(0.5, 1.0))
        ])
        noiseImage = seq.augment_image(srcImg)
        return noiseImage

    def GenerateImg(self, stdHeight, maxLeftBlank, maxRightBlank, maxTopBlank, maxBottomBlank, font, text, noiseImg = False, noiseMode = "Imgaug"):
        #generate binary image
        if len(text) == 0:
            logging.warning("Processing. String is empty.")
            return False, False, False
        img = font.StringToMat(text)
        #cv2.imwrite(text+"_font"+".jpg",img)
        if img.shape[0]*img.shape[1] <= 5:
            logging.warning("Processing. Image is too small.")
            return False, False, False

        ratio = stdHeight*1.0/(img.shape[0]*1.0)
        reWidth = int(img.shape[1]*ratio)
        reImg = cv2.resize(img,(reWidth,stdHeight),interpolation=cv2.INTER_CUBIC)
        leftBlankSize  = random.randint(0,maxLeftBlank)
        rightBlankSize = random.randint(0,maxRightBlank)
        topBlankSize    = random.randint(0,maxTopBlank)
        bottomBlankSize  = random.randint(0,maxBottomBlank)
        textImg = cv2.copyMakeBorder(reImg, topBlankSize, bottomBlankSize, leftBlankSize, rightBlankSize , cv2.BORDER_CONSTANT, value=[255,255,255])
        resImage = textImg.copy()
        #generate lable
        resLabel = []
        for char in text:
            lableTemp = list(self.charDict.keys())[list(self.charDict.values()).index(char)]
            resLabel.append(lableTemp)
        #cv2.imwrite(text+str(resLabel)+"_res.jpg",resImage)
        if noiseImg:
            if noiseMode == "Imgaug":
                resImage = self.ImageAug(textImg)
            else:
                resImage = self.AddGaussianNoise(textImg)

        return resImage, resLabel, True

    def GenerateImgs(self, count, textsFile, imgType = "PURE", noiseMode = "Imgaug"): #type: PURE, NOISE
        texts = IOUtils.LoadTexts(textsFile)

        tImages = []
        tNumLabels = []
        tCharLabels = []
        textsSize = len(texts)
        textID = []
        parmID = []
        logging.info("Processing. Start to generate bin text images.")
        logging.info("Processing. Texts number: %d", textsSize)
        logging.info("Processing. Images number: %d", count)
        logging.info("Processing. Size of pramaters: %d", len(self.parms))

        for i in range(textsSize):
            textID.append(i)
            parmID.append(random.randint(0,len(self.parms)-1))

        for i in range(count):
            if i % textsSize == 0:
                random.shuffle(textID)
            idx = i % textsSize
            textId = textID[idx]
            parmId = parmID[idx]
            font = FT(self.parms[parmId])
            if (not(imgType == "PURE")) and self.hasTemplate:
                resImage, resLabel, resState =  self.GenerateImg(32,32,32,5,5,font,texts[textId], True, noiseMode)
            else:
                resImage, resLabel, resState =  self.GenerateImg(32,32,32,5,5,font,texts[textId], False, )
            if resState is True:
                tImages.append(resImage)
                tNumLabels.append(resLabel)
                tCharLabels.append(texts[textId])
            else:
                random.shuffle(textID)
            if i % 100 == 0:
                logging.info("Prosessing. %d images have been generated.", i)
        return tImages, tNumLabels, tCharLabels
