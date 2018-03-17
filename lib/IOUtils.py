# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Siqi Cai and Wenyuan Xue
# --------------------------------------------------------
# -*- coding: utf-8 -*-
import os
import cv2
import logging

logging.basicConfig(level=logging.INFO)


#输入：图像所在文件夹路径
#输出：该路径下，图像文件的列表(list)，如：['001.jpg','002.jpg',...]
def GetImageList(pathToImage):
    ret = []
    for rt,dirs,files in os.walk(pathToImage):
        for filename in files:
			ret.append(filename)
	return ret
    

#输入：列举词条文件(如:./myData/words.txt)的路径(以UFT8解码)
#输出：词条列表(list)，如：['hello','world',...]
def LoadTexts(textPath):
    f = open(textPath,'r')
    texts = f.read()
    texts = unicode(texts, 'utf-8')
    texts = texts.replace(' ','').replace('\r','').strip('\n').split('\n')
    textsList = []
    for line in texts:
        textsList.append(line)
    return textsList

#输入：单个图像路劲
#输出：根据文件后缀(jpg,png,...)，判断文件是否为图像文件，返回True或者False
def IsImage(filePath):
    strs = filePath.split('.')
    format = strs.pop()
    if format == 'png' or format == 'jpg':
        return True
    else:
        return False

   
#输入：保存路径，图像列表，文件名称列表，dat文件列表
#输出：顺利保存返回True，否则抛出异常
def SaveData(savePath, images, numLabels, charLabels, filesPerDir = 10000):
    logging.info("Saving Data. Total: %d images", len(images))
    assert (len(images)==len(numLabels) and len(images)==len(charLabels)),\
    "The number of images don't equal to that of labels."

    imgLength = len(images)

    for ind in range(imgLength):
        dirName = str(ind/filesPerDir)
        path = os.path.join(savePath,dirName)
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info("Saving Data. Make directory: "+path)
        imgFile        = os.path.join(path,str(hex(ind)).zfill(imgLength/16+1)+".jpg")
        numLabelsFile  = os.path.join(path,str(hex(ind)).zfill(imgLength/16+1)+".txt")
        charLabelsFile = os.path.join(path,str(hex(ind)).zfill(imgLength/16+1)+".dat")
        #save image
        cv2.imwrite(imgFile, images[ind])
        #save numLabels
        if isinstance(numLabels[ind], list):
            nf = open(numLabelsFile, 'w')
            for n,label in enumerate(numLabels[ind]):
                if n != len(numLabels[ind])-1:
                    nf.write(str(label).encode('utf-8') + ",")
                else:
                    nf.write(str(label).encode('utf-8'))
            nf.close()
        else:
            nf = open(numLabelsFile, 'w')
            nf.write(numLabels[ind])
            nf.close()
        #save charLabels
        cf = open(charLabelsFile, 'w')
        cf.write(charLabels[ind].encode('utf-8'))
        cf.close()
        percentage = int(ind*100.0/(imgLength*1.0))
        if percentage % 5 == 0:
            logging.info("Saving Data. Saving, %d %%", percentage)
    logging.info("Saving Data. Saving Done.")
    return True

#输入：图像列表，文件名称列表，保存路劲
#输出：顺利保存返回True，否则抛出异常
#def saveImages(matList, nameList, savePath):

    #return True

#输入：文本列表，文件名称列表，保存路劲
#输出：顺利保存返回True，否则抛出异常
def saveText(textList, nameList, savePath):
    assert (len(textList) == len(nameList) ), \
        "The number of textList don't equal to nameList."
    for i in range(len(textList)):
        f=open(savePath+'/'+nameList[i],'w')
        f.write(textList[i])
        f.close()
    return True


def LoadMeanStds(file_name, mean_stds):
    results = open(file_name)
    lines = results.readlines()
    logging.info('Total ' + len(lines) + ' lines')
    for l in lines:
        mean_std = []
        print l
        ls = l.split(' ')
        for i in xrange(4):
            mean_std.append(float(ls[i]))
        mean_stds.append(mean_stds)
