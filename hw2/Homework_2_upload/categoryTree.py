#!/usr/bin/python

def categoryTree():
	with open( "category", "r" ) as f :
		all = f.read().split( "\n" )
	category = {}
	for line in all :
		elements = line.split( "," )
		for element in elements[1:] :
			if category.has_key( element ) == False :
				category[element] = elements[0]
	category['Caf\x1a\x1a'] = category['Caf\xe9s']
	category['Caf\x1a'] = category['Caf\xe9s']
	return category
