#!/usr/bin/python

import numpy as np

import id2X
import categoryTree
import getPreference
import haversine

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
	preference['0'] : perference dictionary during weekdays
	preference['1'] : perference dictionary during holidays
	preference[holiday][uid]['temporal'] : temporal preference of user with uid
	preference[holiday][uid]['category'] : category preference of user with uid
	"""
	preference = getPreference.getPreference()


	"""
	dictionary of feature matrice of users
	user_features['0'] : feature matrix during weekdays
	user_features['1'] : feature matrix during holidays
	"""
	user_features = {}

	# loop through preference['0'] and preference['1']
	for day in preference :
		all_user_feature = []
		
		for uid in preference[day] :
			# length preference :
			length = [0]

			# temporal preference :
			temporal = preference[day][uid]['temporal']

			# category preference :

			# initialize category counter
			category_counter = {}
			for term in _categories :
				if preference[day][uid]['category'].has_key( term ) == True :
					category_counter[term] = preference[day][uid]['category'][term]
				else :
					category_counter[term] = 0

			holiday = [1]
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

		# create length preference :

		length = 0
		# calculate the distances between multiple places
		if size >= 6 :
			for i in range( 2, size - 2, 2 ) :
				length += haversine.distance( float( coordinate[route[i]][0] ), float( coordinate[route[i]][1] ), float( coordinate[route[i + 2]][0] ), float( coordinate[route[i + 2]][1] ) )

		# create temporal preference :
		temporal = [0] * 24
		for i in range( 3, size, 2 ) :
			temporal[int( route[i] )] += 1

		# create category preference :

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

		holiday = [float( route[1] )]
		# append feature list of current route to all_route_feature list
		all_route_feature.append( holiday + [length] + temporal + category_counter.values() )


	# transform features from 2-D list to 2-D matrix
	route_features = np.array( all_route_feature )
	return route_features

def predict( user_features, route_features ) :
	result = {}
	for day in user_features :
		result[day] = np.dot( route_features, user_features[day].T )
	return result

if __name__ == "__main__" :
	user_features = userFeatures()
	route_features = routeFeatures()
	result = predict( user_features, route_features )
