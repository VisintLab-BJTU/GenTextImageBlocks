# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Siqi Cai and Wenyuan Xue
# --------------------------------------------------------



#输入：图像所在文件夹的路劲
#输出：该路劲下，图像文件的列表(list)，如：['001.jpg','002.jpg',...]
def GetImageList(pathToImage):

    return imagesList

#输入：列举词条文件(如:./myData/words.txt)的路径(以UFT8解码)
#输出：词条列表(list)，如：['hello','world',...]
def LoadWords(pathToWords):

    return wordsList

#输入：单个图像路劲
#输出：根据文件后缀(jpg,png,...)，判断文件是否为图像文件，返回True或者False
def IsImage():

    return False# or True

#输入：图像列表，文件名称列表，保存路劲
#输出：顺利保存返回True，否则抛出异常
def saveImages(matList, nameList, savePath):

    return True

#输入：文本列表，文件名称列表，保存路劲
#输出：顺利保存返回True，否则抛出异常
def saveText(textList, nameList, savePath):

    return True
