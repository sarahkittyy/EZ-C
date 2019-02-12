import interpreter.cleancode as cleancode
import interpreter.symbols as symbols
import re
import math

class Interpreter(object):
	def __init__(self, code):
		# clean the code
		self.code = cleancode.clean(code.splitlines())
		
		# get code blocks
		self.insideblocks, self.code = symbols.stripblocks(self.code)
		
		# add global code to global block, containing other blocks
		self.globalblock = {'name': '__GLOBAL__', 'code': self.code, 'blocks': self.insideblocks}
		
		print(self.globalblock)
		
	def run(self):
		
		# begin executing
		print('###INTERPRETING###\n')
		
		return self.runcode(self.globalblock)
		
	def runcode(self, scope, stack = [], vars = {}):
		
		def ret(msg, code=0):
			return msg, code, stack, vars
		
		def subvars(line):
			#special case for outputting the stack
			line = re.sub(r'\$\{(__STACK__)\}', lambda x : str(stack), line)
			
			line = re.sub(r'\$\{(.+?)\}',lambda x : str(vars[x.group(1)]), line)
			return line
		
		def isnum(val):
			try:
				float(val)
			except ValueError:
				return False
			return True
			
		skipIter = False
		repeatLineCount = 0
		
		index = 0
		while index < len(scope['code']):
			
			if repeatLineCount > 0:
				repeatLineCount -= 1
			
			line = scope['code'][index]
			
			if skipIter:
				skipIter = False
				index += 1
				continue
			words = line.split()
			method_name = words[0]
			method_args = words[1:]
			
			################## METHODS #####################
			if method_name == 'out':
				
				# substitute variables
				try:
					method_args = subvars(" ".join(method_args)).split()
				except KeyError:
					return ret("Error: attempt to reference an undefined variable.", -1)
				
				[print(i + ' ', end='') for i in method_args]
				print()
					
			####
			elif method_name == 'call':
				if len(method_args) != 1:
					return ret("Error, invalid argc to method call", -1)
				# find the block associated with the call
				block_name = method_args[0]
				for i in scope['blocks']:
					if i['name'] == block_name:
						msg, code, retstack, _ = self.runcode(i, stack)
						if code != 0:
							return ret(msg, code)
						stack = retstack
						break
				else:
					# allow recursion
					if block_name == scope['name']:
						msg, code, retstack, _ = self.runcode(scope, stack)
						if code != 0:
							return ret(msg, code)
						stack = retstack
						break
					else:
						return ret("Block " + block_name + " not found.", -1)
						
			elif method_name == 'break':
				return ret("Early block break.", 0)
					
			####
			elif method_name == 'set':
				if len(method_args) < 2:
					ret("Error, invalid set call argc.", -1)
					
				# sub vars
			
				var_name = method_args[0]
				var_val = subvars(" ".join(method_args[1:]))
				
				vars[var_name] = var_val
			
			####
			elif method_name == 'in':
				if len(method_args) != 1:
					return ret("Error, invalid argc in 'in' call", -1)
					
				var_name = method_args[0]
				vars[var_name] = input()
				
			####	
			elif method_name == 'stack':
				if len(method_args) < 2:
					return ret("Error, invalid argc in stack call", -1)
				if method_args[0] == 'push':
					# concatenate all arguments past push
					line = " ".join(method_args[1:])
					try:
						line = subvars(line)
					except KeyError:
						return ret("Error, attempt to reference an undefined variable.", -1)
					
					# push to stack
					stack.append(line)
					
				elif method_args[0] == 'pop':
					# get the top value off the stack
					val = stack.pop()
					# get the variable name
					var_name = method_args[1]
					# set the variable
					vars[var_name] = val
					
				else:
					return ret("Error, unknown stack operation.", -1)
			
			####
			elif method_name == 'oper':
				if len(method_args) != 1:
					return ret("Error, invalid argc in oper call.", -1)
				
				if method_args[0] == '+':
					val1 = stack.pop()
					val2 = stack.pop()
					if isnum(val1) and isnum(val2):
						val1 = float(val1)
						val2 = float(val2)
					stack.append(val1 + val2)
					
				elif method_args[0] == '-':
					val1 = stack.pop()
					val2 = stack.pop()
					if isnum(val1) and isnum(val2):
						val1 = float(val1)
						val2 = float(val2)
					stack.append(val1 - val2)
					
				elif method_args[0] == '\\':
					val1 = stack.pop()
					val2 = stack.pop()
					stack.append(val1)
					stack.append(val2)
					
				else:
					return ret("Error, oper operator " + method_args[0] + "not supported.", -1)
			
			####
			elif method_name == 'ifeq':
				if len(method_args) != 2:
					return ret("Error: invalid argc in ifeq call.", -1)
				
				# substitute variables
				arg1 = method_args[0]
				arg2 = method_args[1]
				try:
					arg1 = subvars(arg1)
					arg2 = subvars(arg2)
				except KeyError:
					return ret("Error: attempt to reference an undefined variable.", -1)
					
				if isnum(arg1) and isnum(arg2):
					arg1 = float(arg1)
					arg2 = float(arg2)
				
				if arg1 != arg2:
					skipIter = True
			
			####
			elif method_name == 'ifneq':
				if len(method_args) != 2:
					return ret("Error: invalid argc in ifmeq call.", -1)
					
				# substitute variables
				arg1 = method_args[0]
				arg2 = method_args[1]
				try:
					arg1 = subvars(arg1)
					arg2 = subvars(arg2)
				except KeyError:
					return ret("Error: attempt to reference an undefined variable.", -1)
					
				if isnum(arg1) and isnum(arg2):
					arg1 = float(arg1)
					arg2 = float(arg2)
				
				if arg1 == arg2:
					skipIter = True
					
			####
			elif method_name == 'ifstack':
				if len(stack) == 0:
					skipIter = True
					
			####
			elif method_name == 'pause':
				input()
				
			####
			elif method_name == 'loop':
				if len(method_args) != 1:
					return ret("Error: invalid argc in loop call.", -1)
				
				# substitute vals
				val = subvars(method_args[0])
				if not isnum(val):
					return ret("Error: loop counter is not a number!", -1)
				
				repeatLineCount = math.floor(float(val))
				index += 1
						
			####
			else:
				return ret("Error: Unknown method call '" + method_name + "'.", -1)
					
			############### END METHOD DEFS ################
			
			if repeatLineCount == 0:
				index += 1
		
		return ret("###FINISHED###", 0)