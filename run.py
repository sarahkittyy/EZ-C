import sys
import interpreter
from interpreter.main import Interpreter

# main
def main():
	
	# check passed parameter length
	if len(sys.argv) != 2:
		return
		
	code = ''
	
	with open(sys.argv[1], "r") as file:
		code = file.read()
	
	i = Interpreter(code)
	msg, code, _, _ = i.run()
	
	print('\nReturned with code ' + str(code) + ' : ' + msg)
	
	return

if __name__ == "__main__":
	main()