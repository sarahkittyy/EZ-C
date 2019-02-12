# EZC

Good luck making anything useful in this (yes, turing-complete) langauge.

To run code:

```
python run.py file.ezc
```

## Contributing

It's completely uncommented, don't even bother.

# Docs

## Notes

Tabs & indentation are ignored, but can be used for easy legibility.

## Comments

```
!! This is a comment.
```

## I/O

```
out hi there !! prints hi there, with a newline
in x
out ${x}
```


## Blocks

```
block block_name
	out hello!
	break
end

call block_name

!! Note: break statement always exits current block, but is not necessary.
```

Recursion is possible, and nested blocks can have the same identifier.

Ex:
```
block b
	block b
		out hi!
	end
	
	call b !! will output hi
end

call b
```

## Variables

```
set x 4
```

Variables have local scope specific to their block. Nested blocks cannot access parent variables.

## Functions

Functions in EZC are emulated using a local stack to pass parameters.
Every block has a unique stack that is passed upon executing `call`
The stack is then returned back after, and appended to the previously existing stack in the calling scope.

Ex:
```
block print !! define a new print block
	stack pop x !! pop the top stack value into x
	out ${x} !! print x
	stack push 4
end

stack push hello !! push the raw text 'hello' to the stack
call print !! call print, passing the stack
stack pop y
out return: ${y}
```

## Arithmetic

EZC supports addition & subtraction, as well as `oper \` which swaps the top two stack values.

Ex:
```
block addOne
	stack push 1
	
	oper + !! pop the top two stack values, and push back the result.
	
	stack pop x
	
	stack push ${x}
end

stack push 4
call addOne
stack pop x
out ${x}
```

## Conditionals

`ifeq` and `ifneq` execute the next line if the condition holds.

`ifstack` runs the next line if the stack isn't empty.

Ex:

```
set x 2
ifeq ${x} 2
	out x is 2
ifneq ${x} 3
	out x isn't 3
ifeq ${x} 3
	out x is three
```

## Loops

```
block inctwo
	stack pop x
	
	stack push ${x}
	stack push 2
	oper +
	stack pop x
	
	stack push ${x}
end

set x 2
stack push ${x}
loop ${x}
	call inctwo
	
stack pop x
out ${x}
```