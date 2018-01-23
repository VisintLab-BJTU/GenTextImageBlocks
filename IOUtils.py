#-*- coding:utf-8 -*- 
import os
import sys
import logging
import cv2
import locale
 
def LoadText(file, texts):
    filein = open(file)
    for text in filein:
        texts.append(text)  
    filein.close()

def isImage(file):
    strs = file.split('.')
    format = strs.pop()
    if format == 'png' or format == 'jpg':
        return True
    else:
        return False

def GetAllImaheFiles(path, num, images):
    for root, dirs, files in os.walk(path):
        for fileName in files:
            f = os.path.join(root, fileName)
            if isImage(f):
                images.append(f)
            if len(images) >= num:
                break
        logging.info('get image num:' + len(images) + '/' + num)
        if len(images) >= num:
            break
    
def SaveSamples(base_dir, images, labels, strs, files_pre_dir=10000):
    logging.info('Total image num = ' + len(images))

	#CHECK_EQ(images.size(), labels.size());
    if len(images) != len(labels):
        print 'mages.size(), labels.size()   not equal'
        sys.exit(1)

    i = 0
    for img in images:
        dir_name = str(i / files_pre_dir)
        path = os.path.join(base_dir, dir_name)
        if not os.path.exists(path):
            logging.info('mkdir ' + path)
            os.makedirs(path)
        image_file = os.psth.join(path, i + '.jpg')
        label_file = os.path.join(path, i + '.txt')
        dat_file = os.path.join(path, i + '.dat')
        cv2.imwrite(image_file, images[i])
        
        if isinstance(labels[i], list):
            lf = open(label_file, 'w')
            for n in labels[i]:
                lf.write(labels[i] + ',')
            lf.close()
        else:
            lf = open(label_file, 'w')
            lf.write(labels[i])
            lf.close()
        df = open(dat_file, 'w')
        df.write(strs[i])
        df.close()
        if i % 100 == 0:
            logging.info('save image num:' + i)
        i += 1
            
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
