#!/usr/bin/python

import numpy as np

import id2X
import categoryTree
import getPreference
import distance

_test_data_file = "Boston_data/validation_set1.csv"

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

_user_list = {}
_user_list['0'] = []
_user_list['1'] = []

def userFeatures() :
	"""
	preference dictionary about level 1 categories of all users
	preference['0'] : perference dictionary during weekdays
	preference['1'] : perference dictionary during holidays
	preference[holiday][uid]['length'] : length preference of user with uid
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
			_user_list[day].append( uid )
			# length preference :
			length = [preference[day][uid]['length']]

			# temporal preference :
			temporal = np.array( preference[day][uid]['temporal'] )
			temporal_normalized = ( temporal  / temporal.max() ).tolist()

			# category preference :

			# initialize category counter
			category_counter = {}
			for term in _categories :
				if preference[day][uid]['category'].has_key( term ) == True :
					category_counter[term] = preference[day][uid]['category'][term]
				else :
					category_counter[term] = 0

			category = np.array( category_counter.values() )
			category_normalized = ( category / float( category.max() ) ).tolist()
			# append feature list of current user to all_user_feature list
#			all_user_feature.append( temporal_normalized + category_normalized )
			all_user_feature.append( length + temporal_normalized + category_normalized )

		# transform features from 2-D list to 2-D matrix
		user_features[day] = np.array( all_user_feature )
		user_features[day][:,0] *= 1


	return user_features

_id = []
def routeFeatures() :
	ct = categoryTree.categoryTree()

	# load test data from file
	with open( _test_data_file, "r" ) as f :
		all_test_data = f.read().split( "\r\n" )

	# create id-levelN_name dictionary
	place, coordinate = id2X.id2X( "BSID_info.txt" )
	p, c = id2X.id2X( "NYID_info.txt" )
	place.update( p )
	coordinate.update( c )

	all_route_feature = []

	for data in all_test_data[:-1] :
		route = data.split( "," )
		_id.append( route[0] )
		size = len( route )

		# create length preference :

		length = [float( 0 )]
		# calculate the distances between multiple places
		if size >= 6 :
			for i in range( 2, size - 2, 2 ) :
				length[0] += distance.distance( float( coordinate[route[i]][0] ), float( coordinate[route[i]][1] ), float( coordinate[route[i + 2]][0] ), float( coordinate[route[i + 2]][1] ) )

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
			2. ct[place[route[i]]] : map levelN_name to level1_name
			3. update the level 1 category counter
			"""
			category_counter[ct[place[route[i]]]] += 1
		category = category_counter.values()

		# append feature list of current route to all_route_feature list
#		all_route_feature.append( temporal + category )
		all_route_feature.append( length + temporal + category )


	# transform features from 2-D list to 2-D matrix
	route_features = np.array( all_route_feature )
	return route_features

def predict( user_features, route_features ) :
	result = {}
	for day in user_features :
		"""
		length_normalized = user_features[day][:,0]
		route_length_normalized = route_features[:,0]
		route_length_normalized = ( route_length_normalized - length_normalized.mean() ) / ( length_normalized.max() - length_normalized.min() )
		length_normalized = ( length_normalized - length_normalized.mean() ) / ( length_normalized.max() - length_normalized.min() )
		"""
#		result[day] = np.dot( route_features, user_features[day].T )
#		"""
		result[day] = []
		for i in range( len( route_features ) ) :
			# euclidean distance
#			result[day].append( ( ( user_features[day] - route_features[i] ) ** 2 ).sum(1) )
			# cosine similarity
			result[day].append( np.dot( route_features[i] / ( route_features[i] ** 2 ).sum(),\
										( user_features[day] / np.dot( np.array( ( user_features[day] ** 2 ).sum( 1 ), ndmin = 2 ).T, np.array( [1] * 35, ndmin = 2 ) ) ).T  ) )
#		"""
	return result

if __name__ == "__main__" :
	user_features = userFeatures()
	route_features = routeFeatures()
	_user_list_a = {}
	_user_list_a['0'] = np.array( _user_list['0'] )
	_user_list_a['1'] = np.array( _user_list['1'] )
	result = predict( user_features, route_features )

	rate = []
	for i in range( len( _id ) ) :
#		print "\n\n";
		ans = _id[i];
#		print "uid   : ", _user_list_a[h][result[h][i].argsort()];
#		print "score : ", result[h][i,result[h][i].argsort()];
#		print "no. ", i
#		print "ans :", ans
		ratio = []
		for h in [ '0','1'] :
			pos = np.argwhere( _user_list_a[h][result[h][i].argsort()]==ans )
			if pos.shape != (0,1) :
				ratio.append( (len( _user_list_a[h] ) - pos[0][0]) / float(len( _user_list_a[h] )) )
		rate.append( min( ratio ) )
#		print "ratio : ", min( ratio )
	rate = np.array( rate )
	print rate.mean()
