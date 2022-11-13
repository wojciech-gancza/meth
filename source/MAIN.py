# ----------------------------------------------------------

from meth import code_generator, code_block
from tools import general_name

# Main functionality of source file generator. It 
builder = code_generator(globals())

def generate_some_code():
    return code_block([ "void ${fname}", 
                            "{", 
                            "    // -vvv ${fname} user code", 
                            "    // by default - do nothing",
                            "    // -^^^ end of user code. do not modify",
                            "}"])

builder.set_template("../test/source.cpp")
builder.define("name", general_name("hello World"))
builder.define("fname", "a_function")
builder.define("enum_list", ["FIRST", "SECOND", "THIRD", "AND_FINALLY_FORTH", "LAST"])
builder.generate("../test/_generated/result.cpp")

# ----------------------------------------------------------
