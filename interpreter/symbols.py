def stripblocks(code):
	
	blocks = []
	
	# When there's a block,
	# gather all lines of code inside.
	# run this function recursively on all
	# inner blocks.
	
	"""
	Dict format:
	{
		'name': 'block_name'
		'code': []
		'blocks': {
			'name': block_name
			'code': []
			'blocks': []
		}
	},
	{...}
	"""
	
	# also strip all block defs from code
	
	c_block = {}
	logging = False
	log_lines = []
	block_ct = 0
	newcode = []
	lines_to_erase = []
	
	for index in range(len(code)):
		line = code[index]
		if logging:
			if line.startswith('block'):
				block_ct += 1
			if line == 'end':
				block_ct -= 1
				lines_to_erase.append(index)
				if block_ct == 0:
					logging = False
					c_block['code'] = log_lines
					strippedblocks, strippedcode = stripblocks(c_block['code'])
					c_block['code'] = strippedcode
					c_block['blocks'] = strippedblocks
					blocks.append(c_block)
					c_block = {}
					log_lines = []
					
			if logging:
				log_lines.append(line)
				lines_to_erase.append(index)
				
			
		elif line.startswith('block'):
			lines_to_erase.append(index)
			logging = True
			words = line.split()
			c_block['name'] = words[1]
			block_ct += 1
			
	for index in range(len(code)):
		if index not in lines_to_erase:
			newcode.append(code[index])
			
	return blocks, newcode