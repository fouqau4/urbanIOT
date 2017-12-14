#!/usr/bin/python

import json

import categoryTree
import id2X

_info_filename = "NYID_info.txt"
_output_filename = "category_preference_new"

_category = categoryTree.categoryTree()

_place, _ = id2X.id2X( _info_filename )

def getPreference() :
	# load data from file
	with open( "NewYork_Data.txt", "r" ) as f :
		all = f.read().split( "\r\n" )

	preference = {}
	preference['0'] = {}
	preference['1'] = {}

	for line in all[:-1] :
		uid, route = line.split( ",", 1 )
		uid, holiday = uid.split( ":" )
		route_info = route.split( "," )
		size = len( route_info )

		if preference[holiday].has_key( uid ) == False :
			preference[holiday][uid] = {}
			preference[holiday][uid]['temporal'] = [float( 0 )] * 24
			preference[holiday][uid]['category'] = {}

		# temporal preference :
		for i in range( 1, size, 2 ) :
			preference[holiday][uid]['temporal'][int( route_info[i] )] += 1
			preference[holiday][uid]['temporal'][( int( route_info[i] ) + 1 ) % 24] += 0.5
			preference[holiday][uid]['temporal'][( int( route_info[i] ) - 1 ) % 24] += 0.5

		# category preference :
		for i in  range( 0, size, 2 ) :
			if preference[holiday][uid]['category'].has_key( _category[_place[route_info[i]]] ) :
				preference[holiday][uid]['category'][_category[_place[route_info[i]]]] += 1
			else :
				preference[holiday][uid]['category'][_category[_place[route_info[i]]]] = 1

	return preference

if __name__ == "__main__" :
	preference = getPreference()
	with open( _output_filename, "w" ) as f :
		f.write( json.dumps( preference, indent = 4, sort_keys = True ) )
