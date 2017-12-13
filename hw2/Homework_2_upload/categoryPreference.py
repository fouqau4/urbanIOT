#!/usr/bin/python

import json

import categoryTree
import id2place

_info_filename = "NYID_info.txt"
_output_filename = "category_preference"

_category = categoryTree.categoryTree()

_place = id2place.id2place( _info_filename )

def categoryPreference() :
	# load data from file
	with open( "NewYork_Data.txt", "r" ) as f :
		all = f.read().split( "\n" )

	preference = {}
	for line in all[:-1] :
		uid, route = line.split( ",", 1 )
		uid = uid[0:-2]
		if preference.has_key( uid ) == False :
			preference[uid] = {}

		place_ids = route.split( "," )
		size = len( place_ids )
		for i in  range( 0, size, 2 ) :
			if preference[uid].has_key( _category[_place[place_ids[i]]] ) :
				preference[uid][_category[_place[place_ids[i]]]] += 1
			else :
				preference[uid][_category[_place[place_ids[i]]]] = 1
	return preference

if __name__ == "__main__" :
	preference = categoryPreference()
	with open( _output_filename, "w" ) as f :
		f.write( json.dumps( preference, indent = 4, sort_keys = True ) )
