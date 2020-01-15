# -*- coding: utf-8 -*-
#PROVA1
import numpy as np
import cv2

#image = Image.open('image.bmp')
#image = image.filter(ImageFilter.FIND_EDGES)
#image.save('new_name.png')

#imageName 'test4.png'
def figure2wall_2robot(imageName):
	print ("loading the walls")
	import cv2
	import numpy as np

	img = cv2.imread(imageName)
	gray = cv2.imread(imageName, 0)
	#gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray=255-gray
	image,contours,hierarchy = cv2.findContours(gray,cv2.RETR_LIST ,cv2.CHAIN_APPROX_NONE )

	i=0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		#print (cnt)
		i=i+1
		#print ("#################")
		if i==1:
		#if area>9000 and area<40000:
			cv2.drawContours(img,[cnt],0,(255,0,0),2)


	#TRASFORMAZIONE PUNTI IN LISTA
	list = []

	for itemList in contours:
	        for item in itemList:
	                list.append(item)
	x = []
	y = []
	i=0
	for coord in list:
	        x.append(coord[0][0])
	        y.append(coord[0][1])


	return (x,y)














	#SALVATAGGIO COORDINATE X E Y

	#counter2 = range(0,2*len(cnt))
	#for counta in counter2:
	#        if(counta%2==0):
	#                x.append(list[counta])
	#        else:
	#                y.append(list[counta])

	#COORDINATE X E Y DIVISE
        ##wallx=[x[0]]
        ##wally=[y[0]]

	#cv2.imwrite('messigray.png',img)
	#cv2.imshow('image',img)
	#cv2.waitKey(0)
	#print(cv2.__file__)
	#print(cv2.getBuildInformation())
	#cv2.imshow('Image',img)
	#cv2.waitKey()
