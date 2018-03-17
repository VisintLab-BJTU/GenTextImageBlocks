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
import sys
import pprint
import argparse
import lib.Test_IOUtils as IOUtils
import lib.Test_ImageUtils as ImageUtils
from lib.templateImage import TemplateImage
from lib.textImageBlockGenerater import TextImageBlockGenerater
from lib.config import cfg, cfg_from_file

def parse_args():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='Generate block images(single line text) \
        for OCR training.')
  parser.add_argument('--cfg', dest='cfg_file',
                      help='data path config file',
                      default=None, type=str)
  parser.add_argument('--imgType', dest='Pure_or_Noise',
                      help='type of generated images',
                      default='Pure', type=str)
  parser.add_argument('--noiseMode', dest='Template_or_Imgaug',
                      help='mode to add noise ',
                      default=None, type=str)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args

if __name__ == '__main__':
    args = parse_args()
    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        cfg_from_file(args.cfg_file)

    print('Using config:')
    pprint.pprint(cfg)

    template = TemplateImage(cfg.SOURCE.TEMPLATE_PATH)
    template.SaveMeanStd(cfg.SAVE.TEMPLATE_FILE)
    imageBlock = TextImageBlockGenerater(cfg.SOURCE.FONT_PATH, cfg.SOURCE.DICT_FILE, \
          cfg.SCALES, cfg.DEGREES, cfg.SOURCE.TEMPLATE_FILE)
    textImages, textNumLabels, textCharLabels = imageBlock.GenerateImgs(cfg.IMAGES_COUNT, \
          cfg.SOURCE.TEXTS_FILE, args.Pure_or_Noise, args.Template_or_Imgaug)
    savingPath = os.path.join(cfg.SAVE.IMAGE_PATH, args.Pure_or_Noise)
    IOUtils.SaveData(savingPath, textImages, textNumLabels, textCharLabels)

    print('Done.')
