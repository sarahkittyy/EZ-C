# Examples

## Multiplication

```
block mult
	stack pop x
	stack pop y
	
	set res 0
	
	stack push ${x}
	stack push ${res}
	
	loop ${y}
		call sub
		
	block sub
		stack pop res
		stack pop x
		stack push ${res}
		stack push ${x}
		oper +
		stack pop res
		stack push ${x}
		stack push ${res}
	end
end

stack push 5
stack push 3

call mult

stack pop res

out ${res}
```

## Factorial
```
block factorial
	block factorial
		block mult
			stack pop x
			stack pop y
			
			set res 0
			
			stack push ${x}
			stack push ${res}
			
			loop ${y}
				call sub
				
			block sub
				stack pop res
				stack pop x
				stack push ${res}
				stack push ${x}
				oper +
				stack pop res
				stack push ${x}
				stack push ${res}
			end
		end
		!! factorial block
		
		stack pop res
		stack pop val
		
		stack push ${val}
		stack push 1
		oper \
		oper -
		stack pop val
		
		stack push ${val}
		stack push ${res}
		call mult
		stack pop res
		
		stack push ${val}
		stack push ${res}
		
		ifeq ${val} 1
			break
		!!
		call factorial
	end
	
	stack pop val
	stack push ${val}
	stack push ${val}
	
	call factorial
end

stack push 5

call factorial

stack pop res

out result: ${res}
```