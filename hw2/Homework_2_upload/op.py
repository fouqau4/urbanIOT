#!/usr/bin/python

import numpy as np

import id2X
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
	"""
	preference dictionary about level 1 categories of all users
	cp['0'] : perference dictionary during weekdays
	cp['1'] : perference dictionary during holidays
	"""
	cp = categoryPreference.categoryPreference()

	"""
	dictionary of feature matrice of users
	user_features['0'] : feature matrix during weekdays
	user_features['1'] : feature matrix during holidays
	"""
	user_features = {}

	# loop through cp['0'] and cp['1']
	for day in cp :
		all_user_feature = []
		
		for user_id in cp[day] :
			# initialize category counter
			category_counter = {}
			for term in _categories :
				if cp[day][user_id].has_key( term ) == True :
					category_counter[term] = cp[day][user_id][term]
				else :
					category_counter[term] = 0

			holiday = [1]
			length = [0]
			temporal = [1] * 24
			# append feature list of current user to all_user_feature list
			all_user_feature.append( holiday + length + temporal + category_counter.values() )

		# transform features from 2-D list to 2-D matrix
		user_features[day] = np.array( all_user_feature )

	return user_features

def routeFeatures() :
	# load test data from file
	with open( "Boston_data/testfile_set1.csv", "r" ) as f :
		all_test_data = f.read().split( "\r\n" )

	# create id-levelN_name dictionary
	place, coordinate = id2X.id2X( "BSID_info.txt" )
	p, c = id2X.id2X( "NYID_info.txt" )
	place.update( p )
	coordinate.update( c )

	all_route_feature = []

	for data in all_test_data[:-1] :
		route = data.split( "," )
		size = len( route )

		# create length preference

		# create temporal preference
		temporal = [0] * 24
		for i in range( 3, size, 2 ) :
			temporal[int( route[i] )] += 1

		# create category preference

		# initialize the category counter dictionary
		category_counter = {}
		for term in _categories :
			category_counter[term] = 0

		for i in range( 2, size, 2 ) :
			"""
			update the category counter :
			1. place[route[i]] : map route_id to levelN_name
			2. _ct[place[route[i]]] : map levelN_name to level1_name
			3. update the level 1 category counter
			"""
			category_counter[_ct[place[route[i]]]] += 1

		holiday = [float(route[1])]
		length = [0]
		# append feature list of current route to all_route_feature list
		all_route_feature.append( holiday + length + temporal + category_counter.values() )

	# transform features from 2-D list to 2-D matrix
	route_features = np.array( all_route_feature )
	return route_features

if __name__ == "__main__" :
	user_features = userFeatures()
	route_features = routeFeatures()
#	result = {}
#	for day in user_features :
#		result[day] = np.dot( route_features, user_features[day].T )
