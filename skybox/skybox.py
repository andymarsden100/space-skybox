import json
import Image
import random
import math
import sys
import skybox_tools
from skybox_tools import Layer
from skybox_tools import LayerList

if __name__=='__main__':

	print "opening config file: "+sys.argv[1]
	#Open the config file
	file=open(sys.argv[1]).read()
	j=json.loads(file)

	print "creating list of layers..."
	#Create list of layers
	layers=LayerList()
	for x in j['layers']:
		layers.list.append(Layer(x,layers))

	print "painting layers..."
	#Paint layers
	for x in layers.list:
		x.paint()

	#print "showing component layers..."
	#for x in layers.list:
	#	x.img.show()

	print "create combination layer"
	result=None
	for x in layers.list:
		if result is None:
			result=x
		else:
			result.add(x)

	result.img.show()
