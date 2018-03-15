#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Wenyuan Xue
# --------------------------------------------------------

import cv2
import os
import lib.Test_IOUtils as IOUtils
import lib.Test_ImageUtils as ImageUtils
from lib.templateImage import TemplateImage
from lib.textImageBlockGenerater import TextImageBlockGenerater


if __name__ == '__main__':
    template = TemplateImage("./myData/srcData")
    template.SaveMeanStd("./myData/template.txt")
    imageBlock = TextImageBlockGenerater("./font", "./myData/map.txt", [1.0], [0.0], "./myData/template.txt")
    textImages, textNumLabels, textCharLabels = imageBlock.GenerateImgs(20, ["hello","world"],imgType = "Noise")
    IOUtils.SaveData("./myData", textImages, textNumLabels, textCharLabels)
    print('Done.')
