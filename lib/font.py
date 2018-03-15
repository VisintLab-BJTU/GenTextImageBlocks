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
from freetype import *
import Test_IOUtils as IOUtils
import Test_ImageUtils as ImageUtils

logging.basicConfig(level=logging.INFO)

class FT(object):
    def __init__(self, fontParm):
        self.angle    = fontParm['degree']*np.pi/360
        self.fontFile = fontParm['font']
        self.fontName = self.fontFile.split("/")[-1]
        self.height   = fontParm['height']
        self.width    = fontParm['width']
        self.scale    = fontParm['scale']

        self.library = FT_Library()
        self.matrix  = self.SetMatrix(self.angle)
        self.pen     = self.SetPen()#[]
        self.fontSize= self.SetFontSize()#FT_UInt

        self.face    = Face(self.fontFile)
        self.face.set_pixel_sizes( self.fontSize, self.fontSize )

    def SetMatrix(self, angle):
        return Matrix(0x10000L,int(angle*0x10000L),0,0x10000L)

    def SetPen(self, pos=[0,0]):
        pen = Vector()
        pen.x = pos[0] << 6
        pen.y = pos[1] << 6
        return pen

    def SetFontSize(self, fontSize = 32):
        return fontSize

    def StringToMat(self, text):#foreGround & backGround: np.array
        text = unicode(text, 'utf-8')
        slot = self.face.glyph

        # First pass to compute bbox
        width, height, baseline = 0, 0, 0
        previous = 0
        for i,c in enumerate(text):
            self.face.load_char(c)
            bitmap = slot.bitmap
            height = max(height,bitmap.rows + max(0,-(slot.bitmap_top-bitmap.rows)))
            baseline = max(baseline, max(0,-(slot.bitmap_top-bitmap.rows)))
            kerning = self.face.get_kerning(previous, c)
            width += (slot.advance.x >> 6) + (kerning.x >> 6)
            previous = c

        img = np.ones((height,width,3), dtype=np.uint8)*255
        x, y = 0, 0
        previous = 0
        for char in text:
            self.face.load_char(char)
            self.face.set_transform(self.matrix, self.pen)
            glyphIndex = self.face.get_char_index(char)

            usingKerning = self.face.has_kerning
            if(usingKerning and previous > 0 and glyphIndex > 0):
                delta  = self.face.get_kerning(previous, glyphIndex,FT_KERNING_DEFAULT)
                self.pen.x += delta.x >> 6

            bitmap = slot.bitmap
            top = slot.bitmap_top
            left = slot.bitmap_left
            w,h = bitmap.width, bitmap.rows
            y = max(height-baseline-top,0)
            kerning = self.face.get_kerning(previous, char)
            x += (kerning.x >> 6)
            #print(y,h,x,w,img.shape,len(bitmap.buffer),char,self.fontName)
            if len(bitmap.buffer)!=0:
                reBuffer = np.array(bitmap.buffer, dtype=np.uint8).reshape(h,w)
                #binBuffer = ImageUtils.BinImage(reBuffer)
                #cv2.imwrite(str(char)+".jpg",binBuffer)
                for i in range(img.shape[2]):
                    img[y:y+h,x:x+w,i] -= reBuffer
            x += (slot.advance.x >> 6)
            self.pen.x += slot.metrics.horiAdvance
            previous = glyphIndex

        return img
