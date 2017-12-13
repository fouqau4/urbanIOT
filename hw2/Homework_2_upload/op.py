#!/usr/bin/python

import numpy as np

import id2place
import categoryTree
import categoryPreference

_categories = [
	"Arts & Entertainment",
	"College & University",
	"Event",
	"Food",
	"Nightlife Spot",
	"Outdoors & Recreation",
	"Professional & Other Places",
	"Residence",
	"Shop & Service",
	"Travel & Transport"
]

_ct = categoryTree.categoryTree()

def userFeatures() :
	# create preference dictionary about level 1 categories of all users
	cp = categoryPreference.categoryPreference()

	all_user_feature = []
	for user_id in cp :
		# initialize category counter
		category_counter = {}
		for term in _categories :
			if cp[user_id].has_key( term ) == True :
				category_counter[term] = cp[user_id][term]
			else :
				category_counter[term] = 0

		holiday = [1]
		length = [0]
		temporal = [1] * 24
		# append feature list of current user to all_user_feature list
		all_user_feature.append( holiday + length + temporal + category_counter.values() )

	# transform features from 2-D list to 2-D matrix
	user_features = np.array( all_user_feature )

	return user_features

def routeFeatures() :
	# load test data from file
	with open( "Boston_data/testfile_set1.csv", "r" ) as f :
		all_test_data = f.read().split( "\r\n" )

	# create id-levelN_name dictionary
	place = id2place.id2place( "BSID_info.txt" )
	place.update( id2place.id2place( "NYID_info.txt" ) )

	all_route_feature = []

	for data in all_test_data[:-1] :
		# initialize the dictionary
		category_counter = {}
		for term in _categories :
			category_counter[term] = 0

		route = data.split( "," )
		size = len( route )
		for i in range( 2, size, 2 ) :
			"""
			1. map route_id to levelN_name
			2. map levelN_name to level1_name
			3. update the level 1 category counter
			"""
			category_counter[_ct[place[route[i]]]] += 1

		holiday = [1]
		length = [0]
		temporal = [1] * 24
		# append feature list of current route to all_route_feature list
		all_route_feature.append( holiday + length + temporal + category_counter.values() )

	# transform features from 2-D list to 2-D matrix
	route_features = np.array( all_route_feature )
	return route_features

if __name__ == "__main__" :
	user_features = userFeatures()
	route_features = routeFeatures()
