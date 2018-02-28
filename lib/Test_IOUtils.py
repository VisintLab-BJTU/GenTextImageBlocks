import os
def GetImageList(pathToImage):
    ret = []
    for rt,dirs,files in os.walk(pathToImage):
        for filename in files:
			ret.append(filename)
	return ret
