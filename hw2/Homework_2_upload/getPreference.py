#!/usr/bin/python

import json

import categoryTree
import distance
import id2X


_output_filename = "category_preference_new"

def getPreference() :
	info_filename = "NYID_info.txt"

	category = categoryTree.categoryTree()

	place, _coordinate = id2X.id2X( info_filename )

	# load data from file
	with open( "NewYork_Data.txt", "r" ) as f :
		all = f.read().split( "\r\n" )

	preference = {}
	preference['0'] = {}
	preference['1'] = {}
	route_count = {}
	route_count['0'] = {}
	route_count['1'] = {}

	for line in all[:-1] :
		uid, route = line.split( ",", 1 )
		uid, holiday = uid.split( ":" )
		route_info = route.split( "," )
		size = len( route_info )

		if preference[holiday].has_key( uid ) == False :
			preference[holiday][uid] = {}
			preference[holiday][uid]['length'] = float( 0 )
			preference[holiday][uid]['temporal'] = [float( 0 )] * 24
			preference[holiday][uid]['category'] = {}
			route_count[holiday][uid] = float( 0 )

		# length preference :
		if size >= 4 :
			for i in range( 0, size - 2, 2 ) :
				preference[holiday][uid]['length'] += distance.distance( float( _coordinate[route_info[i]][0] ), float( _coordinate[route_info[i]][1] ), float( _coordinate[route_info[i + 2]][0] ), float( _coordinate[route_info[i + 2]][1] ) )
			route_count[holiday][uid] += 1

		# temporal preference :
		for i in range( 1, size, 2 ) :
			preference[holiday][uid]['temporal'][int( route_info[i] )] += 1
			preference[holiday][uid]['temporal'][( int( route_info[i] ) + 1 ) % 24] += 0.5
			preference[holiday][uid]['temporal'][( int( route_info[i] ) - 1 ) % 24] += 0.5

		# category preference :
		for i in  range( 0, size, 2 ) :
			if preference[holiday][uid]['category'].has_key( category[place[route_info[i]]] ) :
				preference[holiday][uid]['category'][category[place[route_info[i]]]] += 1
			else :
				preference[holiday][uid]['category'][category[place[route_info[i]]]] = 1

	for day in preference :
		for uid in preference[day] :
			preference[day][uid]['length'] /= route_count[day][uid] if route_count[day][uid] > 0 else 1

	return preference

if __name__ == "__main__" :
	preference = getPreference()
	with open( _output_filename, "w" ) as f :
		f.write( json.dumps( preference, indent = 4, sort_keys = True ) )
