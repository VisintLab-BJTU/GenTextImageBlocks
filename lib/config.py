from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path as osp
import numpy as np
# `pip install easydict` if you don't have it
from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
#   from fast_rcnn_config import cfg
cfg = __C

###
###Source
__C.SOURCE = edict()
#path of template images
__C.SOURCE.TEMPLATE_PATH = './myData/srcData'
#path of font files
__C.SOURCE.FONT_PATH = './font'
#file of texts needed to be generated
__C.SOURCE.TEXTS_FILE = './myData/words.txt'
#file of mean and stddev from templates
__C.SOURCE.TEMPLATE_FILE = './myData/template.txt'
#file of character dict
__C.SOURCE.DICT_FILE = './myData/map.txt'
###
###Saving
__C.SAVE = edict()
#saving path for mean and stddev of templates
__C.SAVE.TEMPLATE_FILE = './myData/template.txt'
#saving path for generated images
__C.SAVE.IMAGE_PATH = './myData'
###
###Parameter
#number to generate
__C.IMAGES_COUNT = 50
#scales
__C.SCALES = np.array([1.0])
#degrees
__C.DEGREES = np.array([0.0])

def _merge_a_into_b(a, b):
  """Merge config dictionary a into config dictionary b, clobbering the
  options in b whenever they are also specified in a.
  """
  if type(a) is not edict:
    return

  for k, v in a.items():
    # a must specify keys that are in b
    if k not in b:
      raise KeyError('{} is not a valid config key'.format(k))

    # the types must match, too
    old_type = type(b[k])
    if old_type is not type(v):
      if isinstance(b[k], np.ndarray):
        v = np.array(v, dtype=b[k].dtype)
      else:
        raise ValueError(('Type mismatch ({} vs. {}) '
                          'for config key: {}').format(type(b[k]),
                                                       type(v), k))

    # recursively merge dicts
    if type(v) is edict:
      try:
        _merge_a_into_b(a[k], b[k])
      except:
        print(('Error under config key: {}'.format(k)))
        raise
    else:
      b[k] = v

def cfg_from_file(filename):
  """Load a config file and merge it into the default options."""
  import yaml
  with open(filename, 'r') as f:
    yaml_cfg = edict(yaml.load(f))

  _merge_a_into_b(yaml_cfg, __C)
