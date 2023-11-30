# METH - code generator

Meth is simple library for use from your own python written metaprogram 
or code generator. Meth generates program files based on templates containig
injected python code generating parts of the output file content. 

## Problem to solve

Starting with big projects, with lots of classes, it is healy hard to avoid
copy-paste technique of creating data objects, messages or simple types. 
Such classes can be generated automatically, but sometimes generated code 
must be mixed with the code written by the programmer. Maintenance of the 
code template should be simple and easy. 

## Solution

I was bored by the different ad-hock code generators and manual modification
of generated code. So I decide to write my own code generator. After few attemps
I realized, that emitinh whole code is not easy to maintain, and the best way is to 
use code templates - files which looks like reasult files, but containing 
variables or even function calls allowing to place result of calculations inside
generated files. Placing special comments inside such template files allow to 
keep the code located between such marks. 

Generation of code can be prepared in form of configuration files, but building 
code generator as single python class used in your won code generator is better 
than creating next domain specific language. Feel free to create your own code 
generator in python with use of meth library. If you want, you can also modify 
code of meth. 

Meth is written in python. Powerfull object oriented script language allowing to 
keep code clean and easy to read. Writing programs generating programs is a 
typical metaprograming. Using python allow to keep you metaprograms clean.

## Features

Meth need template file containing the source of generated files. Template is 
copied line by line to the target replacing variable elements by its value. 

### varialble elements

Variables are denoted as '${ ... }'. The content '...' is simply interpreted 
by the python interpreter and the value is placed in the result file. The value can be: 
- scalar - then its string representation is located in the place of variable.
- list - then set of lines are added with comma endings at the first and middle lines
- list of lines wrapped in 'code_block' class - the content generates multiplied template lines

### manually added code

Lines located between '// -vvv ...' and '// -^^^ ...' are preserved. Programmer can place 
any code between them in generated file. When generation is called, the generator first loads
file and extracts such block to be used in the new file. When file is generated first time, the 
content of template will be stored.

### code added conditionally or in loop

To easily decide about code to add and for generating similar parts of code, two metastatements 
were added:
 - '${#IF condition}' ... - conditionally added code. Conditional code ends at '${#END}' tag. 
   It is also possible to use ${ELSE}. 'condition' is any python expression which value is 
   evalueted when condition is calculated.
 - '${#FOR varname : collection}' - loop. All template text between this tag and '${#END}' is repeated
   for variable named 'varname' trawersing the collection. When the collection is dictionary - 
   use '${#FOR key, value : dictionary}' form of loop.

Metastatements can be nested.
