https://docs.python.org/3/tutorial/introduction.html

### Number
* int, float
* Arithmatic Operation: +, -, *, / float division, // floor division, % module(remainder), **
#### varible_name = init_value
1. declaration & assignment at same time (variable defined)
2. Ortherwise => NameError: name 'variable_name' is not defined
### Boolean
* True, False
* logical operators: and, or
* short-circuit
1. non-zero number => true; zero => False
2. None => False
3. empty container(sequence, str) => False
4. use 'in' to test if container contains a value

### str
* '', ""
* escape \ (\n, \t)
* triple-quotes """....""", '''...''' (keep originalformat, etc. line break)
  1. unescape \
* raw string => print(r'C:\some\name')
* sequence => indexing & slicing
  1. str_name[start_index:end_index] (end_index char excluded)
  2. str_name[:end_index], str_name[start_index:], str_name[:]
  3. negative index, -1
  4. str_name[index]
* immutable
  1. str_name[index] = "J" => TypeError: 'str' object does not support item assignment
* string concate +

### List
* list_name = [item1, ...], empty list => []
* sequence -> indexing & slicing
* mutuable 
* nested list 
* items in list can be different data types
```
letters[2:5] = []
letters[2:5] = ['C', 'D', 'E']
letters[:] = []
```

### Coding
```
a, b = 0, 1
while a < 10:
    print(a)
    a, b = b, a+b
RH evaluated first from left to right before any of the assignments take place.
```
### [Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
* 4.1. if Statements
```
x = int(input("Please enter an integer: "))
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')
```
4.2. for Statements
* loop over items in a container
```
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))
```
4.3 range()

4.4 break/continue statement
* break: breaks out of innermost for/while loop
* continue: continue with next iteration of loop

4.5. else Clauses on Loops
* not executed if the loop was terminated by a break

4.6. pass Statements

4.7. match Statements (new, skip for now)

4.8. Defining Functions
```
def fn_name(parameters):
   """docstrings
   """
   body statements
```
* local variables, nonlocal variables, global variables
* global statement, nonlocal statement
* symbol table
* actual parameters(arguments)
* arguments passed using call by value
* function object, first class citizen
```
f = fib
f(100)
```

* method => function that ‘belongs’ to an object 

4.9.1. Default Argument Values
* Important: The default value is evaluated only once

4.9.2. Keyword Arguments
* kwarg=value
* keyword arguments must follow positional arguments
* keyword arguments must after all positional arguments

*args – any number of positional arguments as a tuple.
**kwargs – any number of keyword arguments as a dictionary.
```

5.1.3. List Comprehensions
* concise way to create lists
```
squares = [x**2 for x in range(10)]
[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
```

5.3. Tuples
* a number of values separated by commas
* immutable, sequence type
* (), (item1,) OR tuple1 = item1,
* tuple packing, sequence unpacking
```
x, y, z = 12345, 54321, 'hello!'
```
5.4. Sets
* an unordered collection with no duplicate elements
* set() => empty set, {} => empty dictionary

