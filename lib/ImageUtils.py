# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Jing Zhang and Wenyuan Xue
# --------------------------------------------------------


#输入：含有图像完整路劲的list
#输出：根据路劲载入图像，并返回一个mat类型的list
def LoadImages(imagesList):

    return matList

#输入：二值图像
#输出：判断图像是否为黑字白底，参考src/ImageUtils.cpp中的实现，输出True或者False
def IsDarkCharLightBack(binMat):

    return False# or True

#输入：灰度图
#输出：二值图(用OTSU的方法)
def BinImage(grayImage):

    return binImage

#输入：rgb三通道图像
#输出：灰度图
def GrayImage(img):

    return img

#输入：一张图像
#输出：判断是否为灰度图，输出True或者False
def IsGrayImage(img):

    return False# or True

#输入：灰度图，二值图，目标背景(前景或后景)
#输出：前景(或后景)的均值，标准差(浮点型),参考./src/TemplateImaeg.cpp中的实现
def GetMeanStd(grayImage, binImage, preOrBack):

    return mean, std
