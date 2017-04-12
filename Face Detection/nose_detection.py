import os, sys, time
import cv2.cv as cv
minSize = (20, 20)
imageScale = 1
haarScale = 2
minNeighbors = 3
haarFlags = cv.CV_HAAR_DO_CANNY_PRUNING

def detectFace(img, cascade):
  # allocate temporary images
  gray = cv.CreateImage((img.width,img.height), 8, 1)
  small_img = cv.CreateImage((cv.Round(img.width / imageScale),cv.Round (img.height / imageScale)), 8, 1)
  # convert color input image to grayscale
  cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
  # scale input image for faster processing
  cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
  cv.EqualizeHist(small_img, small_img)
  faces = cv.HaarDetectObjects(small_img,
                               cascade,
                               cv.CreateMemStorage(0),
                               haarScale, minNeighbors,
                               haarFlags, minSize)
  if faces:
    print "\tDetected ", len(faces), " object(s)"
    for ((x, y, w, h), n) in faces:
      #the input to cv.HaarDetectObjects was resized, scale the 
      #bounding box of each face and convert it to two CvPoints
      pt1 = (int(x * imageScale), int(y * imageScale))
      pt2 = (int((x + w) * imageScale), int((y + h) * imageScale))
      cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
    return img
  else:
    return False

#Search for pictures!
def readDirectory(fileLocation, cascade):
  for root, dirs, files in os.walk(fileLocation):
    print root, "has:"
    for name in files:
      if name.find(".jpg") >=1 :
        #sequentially loop, load and detect.
        print "Analysing " + name +":" 
        #measure how long it takes
        t = cv.GetTickCount()
        #load in the image
        image = cv.LoadImage(os.path.join(root,name), 1)
        match = detectFace(image, cascade)
        if match:
          #save a new image with a square around the nose
          #set the directory
          resultsLocation = '/home/pi/Desktop/results'
          cv.SaveImage( resultsLocation + "/nose_" + name, match)
        t = cv.GetTickCount() -t
        print "\tTime = %gms" %(t/(cv.GetTickFrequency()*1000.))


if __name__ == '__main__':  
  cascade = cv.Load('/home/pi/Desktop/haarcascade_mcs_nose.xml')
  readDirectory('/home/pi/Desktop/pic_test', cascade)
