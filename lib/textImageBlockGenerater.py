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

class TextImageBlockGenerater(object):
    def __init__(self, fontPath, dictPath, scales, degrees):
        self.fontList = [osj(fontPath, font) for font in IOUtils.GetFilesList(fontPath)]
        self.scales = scales
        self.degrees = degrees
        self.charDict = self.LoadDict(dictPath)
        self.parms = self.GenParms()

    def LoadDict(self, dictPath):
        f = open(dictPath,'r')
        dictText = f.read().strip('\n').split('\n')
        charDict = {0:' '}
        for line in dictText:
            line = line.replace('\n','').replace('\r','').strip(' ').split(' ')
            charDict[int(line[0])] = line[1]
        return charDict

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

    def GeneratePureImg(self, stdHeight, maxLeftBlank, maxRightBlank, maxTopBlank, maxBottomBlank, font, text):
        #generate binary image
        if len(text) == 0:
            logging.warning("Processing. String is empty.")
            return False, False, False
        img = font.StringToMat(text, np.array([0,0,0]), np.array([255,255,255]))
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
        return resImage, resLabel, True
    def GeneratePureImgs(self, count, texts):
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
            resImage, resLabel, resState =  self.GeneratePureImg(32,32,32,5,5,font,texts[textId])
            if resState is True:
                tImages.append(resImage)
                tNumLabels.append(resLabel)
                tCharLabels.append(texts[textId])
            else:
                random.shuffle(textID)
            if i % 100 == 0:
                logging.info("Prosessing. %d images have been generated.")
        return tImages, tNumLabels, tCharLabels
