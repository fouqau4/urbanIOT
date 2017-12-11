#!/usr/bin/python

import json

if __name__ == "__main__" :
	with open( "NewYork_Data_place", "r" ) as f :
		all = f.read().split( "\n" )
	user_info = {}
	for line in all[:-2] :
		uid, route = line.split( ",", 1 )
		uid = uid[0:-2]
		if user_info.has_key( uid ) == False :
			user_info[uid] = {}

		places = route.split( "," )
		size = len( places )
		for i in  range( 0, size, 2 ) :
			if user_info[uid].has_key( places[i] ) :
				user_info[uid][places[i]] += 1
			else :
				user_info[uid][places[i]] = 1
	with open( "user_preference", "w" ) as f :
		f.write( json.dumps( user_info, indent = 4, sort_keys = True ) )
