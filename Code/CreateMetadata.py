import numpy as np
import pandas

#Input------------
#This file expects to have two files for its execution:
#File 1 CSV file with name of Images
#File 2 NUMPY file having pixels wise class for all images, one row for one pixel

#Output----------
#It will generate a CSV File having three Columns
#Name of Image
#Tags of Image
#Presnece Vector of image denoting tag they have


def initializeDictionary():
	dict_classes={}
	classes="Aeroplane,Bicycle,Bird,Boat,Bottle,Bus,Car,Cat,Chair,Cow,Diningtable,Dog,Horse,Motorbike,Person,Pottedplant,Sheep,Sofa,Train,Tvmonitor"
	listOfClass=classes.split(",")
	for i in range(0,len(listOfClass)):
		#print i+1,"--",listOfClass[i]
		dict_classes[i+1]=listOfClass[i].upper()
	
	return dict_classes

#This Method computes the classes present in an image as per threshold
#and give the tags and presence vector accordingly	
def getTagAndVector(feature_horse,dict_classes):
	dict_temp={}
	for i in range(0,len(feature_horse)):
		if(dict_temp.has_key(feature_horse[i])):
			dict_temp[feature_horse[i]]=dict_temp[feature_horse[i]]+1
		else:
			dict_temp[feature_horse[i]]=1
	isFirst=True
	tags=''
	print dict_temp
	#Dictionary created , Now iterte over it and add the class name
	presenceVector=np.zeros((1,numberOfClasses),int)
		
	for k, v in dict_temp.items():	    
	    print k,v
	    if( (k==0) or (v<threshold)):
			#print "ignore"
			z=1
	    elif isFirst :
			#print "here1"
			presenceVector[0][k-1]=1
			tags=str(dict_classes[k])
			isFirst=False
	    else:
			#print "here2"
			presenceVector[0][k-1]=1
			tags=tags+","+str(dict_classes[k])
        #print "going out"
			
	print tags
	return (tags,presenceVector)



#initailize the Dictionary
dict_classes=initializeDictionary()

#Get The Number of classes
numberOfClasses=len(dict_classes)

#Threshold for Elements
threshold=1000

#File Name for Numpy file having class labels for every pixels for every class
fileName="PixelClassification.npy"

#name of Feature file
featureArray=np.load(fileName)

#Name of File containng image names 
ImageNameFromServer=pandas.read_csv("ImageNames.csv")



ArrayOfPresenceVector=np.empty((0,numberOfClasses),int)
listOfTags=[]

#Getting Tage and Presence Vector for each Image
for j in range (0,featureArray.shape[0]):
	#print "Shape ",featureArray[j].shape
	#pixel details for one image
	feature=featureArray[j].astype(int)
	feature_horse=feature.tolist()
	#getting tags and vector assoicated
	tags,presenceVector= getTagAndVector(feature_horse,dict_classes)

	print presenceVector
	print tags
	
	#Adding it to the list of tags and Vectors
	ArrayOfPresenceVector=np.append(ArrayOfPresenceVector,presenceVector,axis=0)
	listOfTags.append(tags)
	
	#print "for "+ImageNameFromServer["Names"][j]
	#print "--------------------------"

#Final List of Vectors and Tags
print ArrayOfPresenceVector
print listOfTags

#Creating Data Frame 
DataNew=pandas.DataFrame(
{
"Names":ImageNameFromServer["Names"],
"Tags":listOfTags,
"vectors":ArrayOfPresenceVector.tolist()
})

#Saving the Data Frame
DataNew.to_csv("DatabaseSegmentation.csv", index=False)

