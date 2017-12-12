#!/usr/bin/python

import numpy as np

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

def userFeatures() :
	all_user_feature = []
	cp = categoryPreference.categoryPreference()
	for user_id in cp :
		category_counter = {}
		for term in _categories :
			if cp[user_id].has_key( term ) == True :
				category_counter[term] = cp[user_id][term]
			else :
				category_counter[term] = 0
		holiday = [1]
		length = [0]
		temporal = [1]
		all_user_feature.append( holiday + length + temporal + category_counter.values() )

	user_features = np.array( all_user_feature )

	return user_features
if __name__ == "__main__" :
	user_features = userFeatures()
