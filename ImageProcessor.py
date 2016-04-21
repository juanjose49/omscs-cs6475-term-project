import images2gif
from os import listdir
from os.path import isfile, join
import cv2
import os
import errno
import numpy as np


framesPerSecond=1
numFrames = framesPerSecond * 5
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main():
  imgs, imgFileNames = loadImages("/Users/emeterio/git/omscs-cs6575-computational-photography/final-project/images/")
  applyEffectsAndSave(imgs,imgFileNames)
  
def loadImages(dir):
  imgFileNames = [f for f in listdir(dir) if isfile(join(dir, f))]
  imgs=[]
  for filename in imgFileNames:
    img = cv2.cvtColor(cv2.imread(dir+filename), cv2.COLOR_BGR2RGB)
    imgs.append(img)
  return imgs, imgFileNames

def applyEffectsAndSave(imgs, imgNames):
    global framesPerSecond
    counter = 1
    for i in range(len(imgs)):
      print("starting imaae: " + str(counter) +"/"+str(len(imgs)))
      generatedImgs = applyBrightness(imgs[i])
      buildGif( generatedImgs, framesPerSecond, imgNames[i],"brightness")
      generatedImgs = applyDarkness(imgs[i])
      buildGif( generatedImgs, framesPerSecond, imgNames[i],"darkness")
      generatedImgs = applyNoise(imgs[i])
      buildGif( generatedImgs, framesPerSecond, imgNames[i],"noise")
      generatedImgs = applyBlur(imgs[i])
      buildGif( generatedImgs, framesPerSecond, imgNames[i],"blur")
      generatedImgs = applyThresholding(imgs[i])
      buildGif( generatedImgs, framesPerSecond, imgNames[i],"thresholding")
      counter+=1

    print("finished")
def applyBrightness(img):
  global numFrames

  whiteImg = np.copy(img)
  whiteImg.fill(255)
  return generateImgs(whiteImg, img)

def applyDarkness(img):
  global numFrames
  blackImg = np.copy(img)
  blackImg.fill(0)
  return generateImgs(blackImg, img)

def applyNoise(img):
    global numFrames
    noise = np.random.rand(img.shape[0],img.shape[1],img.shape[2],)
    noise[noise < .5] = 0 # blending sometimes results in slightly out of bound numbers.
    noise[noise >= .5 ] = 255
    noise = noise.astype(np.uint8)
    
    return generateImgs(noise, img)
  
def applyBlur(img):
    global numFrames
    blur = cv2.medianBlur(img,201)
    return generateImgs(blur, img)
  
def applyThresholding(img):
  thresholding = np.copy(img)
  thresholding[thresholding < 128] = 0
  thresholding[thresholding >= 128] = 255
  return generateImgs(thresholding, img)

def generateImgs(manipulatedImg, original):
  generatedImgs = []
  for i in range(numFrames):
    frame = cv2.addWeighted(manipulatedImg,1-(i/float(numFrames)), original,(i/float(numFrames)), 0)
    generatedImgs.append(frame)
  return generatedImgs

def buildGif(imgs, incrementsPerSec, imgName, effectName):
    mkdir("output")
    mkdir("output/" + imgName.split(".")[0])
    smallimgs = []
    for im in imgs:
        smallimgs.append(cv2.resize(im, (0,0), fx=0.07, fy=0.07))
    images2gif.writeGif("output/" + imgName.split(".")[0] + "/" +effectName + ".gif", imgs, duration=1/incrementsPerSec)


main()
