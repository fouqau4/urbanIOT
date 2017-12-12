#!/usr/bin/python

import json
import categoryTree
import id2place

info_filename = "NYID_info.txt"
output_filename = "category_preference"

category = categoryTree.categoryTree()
category['Caf'] = category['Caf\xe9s']
category['Caf'] = category['Caf\xe9s']

place = id2place.id2place( info_filename )

def userInfo() :

	with open( "NewYork_Data.txt", "r" ) as f :
		all = f.read().split( "\n" )
	user_info = {}
	for line in all[:-2] :
		uid, route = line.split( ",", 1 )
		uid = uid[0:-2]
		if user_info.has_key( uid ) == False :
			user_info[uid] = {}

		place_ids = route.split( "," )
		size = len( place_ids )
		for i in  range( 0, size, 2 ) :
			if user_info[uid].has_key( category[place[place_ids[i]]] ) :
				user_info[uid][category[place[place_ids[i]]]] += 1
			else :
				user_info[uid][category[place[place_ids[i]]]] = 1
	return user_info

if __name__ == "__main__" :
	user_info = userInfo()
	with open( output_filename, "w" ) as f :
		f.write( json.dumps( user_info, indent = 4, sort_keys = True ) )
