#!/usr/bin/python

def id2X( info_filename ) :
	X = {}
	X['place'] = {}
	X['coordinate'] = {}
	with open( info_filename, "r" ) as f:
		all = f.read().split( "\n" )
		# The last line is empty string
		for current in all[0:-1] :
			id, longitude, latitude, place, _ = current.split( "\t" )
			X['place'][id] = place
			X['coordinate'][id] = ( longitude, latitude )
	return [ X['place'], X['coordinate'] ]
