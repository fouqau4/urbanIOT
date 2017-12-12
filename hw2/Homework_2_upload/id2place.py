#!/usr/bin/python
def id2place( info_filename ) :
	dict = {}
	with open( info_filename, "r" ) as f:
		all = f.read().split( "\n" )
		# The last line is empty string
		for current in all[0:-2] :
			id, _, _, place, _ = current.split( "\t" )
			dict[id] = place
	return dict

if __name__ == "__main__":
	pass
"""
	with open( "NewYork_Data.txt", "r" ) as f:
		all = f.read().split( "\r\n" )
	dict = id2place()
	output = []
	for line in all[0:-2]:
		spl = line.split( "," )
		for i in range( 1, len( spl ), 2 ):
			spl[i] = dict[spl[i]]
		output.append( spl )
	with open( "NewYork_Data_place", "w" ) as f:
		for element in output:
			line = ','.join( element )
			f.write( line + "\n" )
"""
