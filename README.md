# GenTextBlocks

## Introduction
This is a tiny project for OCR training, which can generate block images from a single line text. Both pure and noisy images can be generated.
![Pure](myData/examples/example_pure.jpg?raw=true "Pure")
![Noise](myData/examples/example_noise.jpg?raw=true "Noise") 
## Library Dependencies
Required packages:
- NumPy
- OpenCV(cv2)
- FreeType(version 2.\*)
- freetype-py(Freetype python bindings)

Following under steps to install FreeType.
```
// Download the new stable version of FreeType package.(eg. freetype-2.9.tar.gz)
// http://download.savannah.gnu.org/releases/freetype/
$ tar zxvf freetype-2.9.tar.gz
$ cd  freetype-2.9
$ ./configure prefix=/usr/local/freetype --without-harfbuzz
//harfbuzz may cause some installation errors
$ make clean
$ sudo make install
```
For freetype-py.
```
$ git clone https://github.com/rougier/freetype-py.git
$ cd freetype-py
$ sudo python setup.py install
```

## Usage

### Data Preparation
**GenTextBlocks** can turn a single line text to an image for most languages. Two files are needed before generation.  
**TEXTS_FILE**. This file saves the texts that you want to change them into images. In the file, texts are wrote line by line, and the file should be saved using UTF-8 encoding. We give an example in "./myData/words.txt".  
**DICT_FILE**. This file saves a dict for TEXTS_FILE. Once we have a TEXTS_FILE, DICT_FILE can be generated automatically by running the file, "./myData/tools/genDict.py".  
**TEMPLATE_FILE**. If you want to generate some images that have similar foreground and background with the real image, you are supposed to give some template images.  
In the file of "./cfg.yml", you can modify the paths of some source files, the directories for saving and the number of generated images.
### Generate Pure or Noisy Images
After data preparation, run:
```
$ python ./gen_text.py --cfg './cfg.yml' --imgType 'PURE' --noiseMode Template
```
--cfg, cfg file can be ignored while using default configuration.

--imgType, you can choose 'PURE' for white background and black foreground, or 'NOISE' for noisy background and foreground.

--noiseMode, 'Template', adding noise according to template images. 'Imgaug', adding noise using imgaug library.(**imgaug mode has not been added.**)
## Experiment Results
