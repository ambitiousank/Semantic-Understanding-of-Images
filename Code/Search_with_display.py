import pandas
import numpy as np
import Image
import cv2

def initializeInverseDictionary():
	inv_dict_classes={}
	classes="Aeroplane,Bicycle,Bird,Boat,Bottle,Bus,Car,Cat,Chair,Cow,Diningtable,Dog,Horse,Motorbike,Person,Pottedplant,Sheep,Sofa,Train,Tvmonitor"
	listOfClass=classes.split(",")
	for i in range(0,len(listOfClass)):
		#print i+1,"--",listOfClass[i]
		inv_dict_classes[listOfClass[i].upper()]=i+1
	#print inv_dict_classes
	return inv_dict_classes


def getSearchVectorAndType(searchString):
	#searchtype=1 for 'or' serachtype=2 for 'and'
	if "," in searchString:
		searchType=1
		searchSplitter=","
	else:
		searchType=2
		searchSplitter="&"
		
	searchVector=np.zeros((numberOfClasses,1),int)
	searchItems=searchString.split(searchSplitter)
	for i in range(0,len(searchItems)):
		index=inv_dict_classes[searchItems[i].upper().strip()]
		searchVector[index-1]=1
	print "Search vector " ,np.transpose(searchVector)
	return searchVector,searchType
	



#initalizing Dictionary
inv_dict_classes=initializeInverseDictionary()

#PREDEFINDE VALUES
numberOfClasses=len(inv_dict_classes)
endIndex=numberOfClasses*3-1
splitToken=", "

print"Choose Database"
inputFromKeyboard=raw_input()
k=int(inputFromKeyboard)

print "Clasess are","Aeroplane,Bicycle,Bird,Boat,Bottle,Bus,Car,Cat,Chair,Cow,Diningtable,Dog,Horse,Motorbike,Person,Pottedplant,Sheep,Sofa,Train,Tvmonitor"

inputFromKeyboard=raw_input()
print inputFromKeyboard

#getting Search Vector
#searchString="Chair"
searchString=str(inputFromKeyboard)
searchVector,searchType=getSearchVectorAndType(searchString)

#Selecting Database
#k=15

db="DatabaseSegmentation_15.csv"
imagePath='Test Images/'

if(k==100):
	db="DatabaseSegmentation_100.csv"
	imagePath='Images_Label/'
elif(k==1000):
	db="DatabaseSegmentation_1000.csv"
	imagePath='Images_Label/'
	
	

#Loading Database
#dataBase=pandas.read_csv("DatabaseSegmentation_1000.csv")
dataBase=pandas.read_csv(db)

searchResults=[]
searchAttribute=sum(searchVector)

#iteraing Search
for i in range(0,len(dataBase["vectors"])):
	
	#gettng the vector filed
	tempL=dataBase["vectors"][i]
	
	#removing the first and last bracket and converting in a list
	tempList=tempL[1:endIndex].split(splitToken)
	
	#converting to an array
	vector= np.array(tempList)
	vector=vector.reshape(1,numberOfClasses)
	vector=np.array(vector,dtype=int)
	
	#print vector.shape
	#print searchVector.shape
	#print vector.astype
	#print searchVector.astype
	#print "vector ",vector
	
	#getting resullt
	result=vector.dot(searchVector)
	#print "Result ",result
	
	#checking and adding image name to th result list
	if(searchType==1) and (result>=1):
		searchResults.append(dataBase["Names"][i])
	elif(searchType==2) and (result==searchAttribute):
		searchResults.append(dataBase["Names"][i])
		

print searchResults

for i in range (0,len(searchResults)):
	#temp='Images_Label/'+searchResults[i]
	temp=imagePath+searchResults[i]
	'''
	image = Image.open(temp)
	image.show()
	'''
	img=cv2.imread(temp,1)
	cv2.imshow('image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
