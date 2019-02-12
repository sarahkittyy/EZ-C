import re

def clean(lines : list):
	
	#remove comments
	lines = list(map(lambda line : re.sub(r'!!.*$', '', line), lines))
	
	#remove empty lines
	lines = list(filter(lambda x : re.match(r'^\s*$', x) == None, lines))
	
	#remove trailing & initial whitespace
	lines = list(map(lambda line : re.sub(r'^\s*', '', line), lines))
	lines = list(map(lambda line : re.sub(r'\s*$', '', line), lines))
	
	return lines