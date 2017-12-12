#!/usr/bin/pyghon
import json

def categoryTree():
	with open( "category", "r" ) as f :
		all = f.read().split( "\n" )
	category = {}
	for line in all :
		elements = line.split( "," )
		for element in elements[1:] :
			if category.has_key( element ) == False :
				category[element] = elements[0]
	return category

if __name__ == "__main__" :
	categoryTree()
