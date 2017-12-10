#!/usr/bin/python

if __name__ == "__main__":
	dict = {}
	with open( "NYID_place", "r" ) as f:
		all = f.read().split( "\n" )
		for current in all[0:-2] :
			id, place = current.split( "," )
			dict[id] = place

	with open( "NewYork_Data.txt", "r" ) as f:
		all = f.read().split( "\r\n" )

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
