# ----------------------------------------------------------

from meth import code_generator, code_block
from tools import general_name, cpp_enum

# Main functionality of source file generator. It 
template            = "../test/03-1-source_template.cpp"
generated_result    = "../test/_generated/03-1-result.cpp"

builder = code_generator(globals())
builder.set_template(template)

builder.define("enum1", cpp_enum(["E1X223", "BETA", "SOMETHONG_ELSE", "X", "KULA314", "MOVIE", "DDS", "MDF", "XRAYMACHINE", "FOXTROT", "B554"]))
builder.define("enum2", cpp_enum(["X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "XA", "XB", "XC", "XD", "XE", "XF"]))
builder.define("emitE1", True)
builder.define("convert_to_string", True)

# builder.generate(generated_result)

a, b, c = builder._check_metastatement("xxxcs${#END}dddsdsds", 3)
print(a, b, c)
a, b, c = builder._check_metastatement("xxxcs${ #  FOR x : collection() }dddsdsds", 0)
print(a, b, c)
a, b, c = builder._check_metastatement("${#IF x}", 0)
print(a, b, c)

# ----------------------------------------------------------
