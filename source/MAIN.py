# ----------------------------------------------------------

from meth import code_generator, code_block
from tools import general_name

# Main functionality of source file generator. It 
template            = "../test/01-1-source_template.cpp"
previous_result     = "../test/01-2-existing_content.cpp"
expected_result     = "../test/01-3-expected_result.cpp"
generated_result    = "../test/_generated/01-3-result.cpp"

builder = code_generator(globals())
builder.set_template(template)
builder.define("name", general_name("hello World"))
builder.define("fname", "a_function")
builder.define("enum_list", ["FIRST", "SECOND", "THIRD", "AND_FINALLY_FORTH", "LAST"])

def generate_some_code_with_placeholders_and_user_code_block():
    return code_block([ 
        "void ${fname}", 
        "{", 
        "    // -vvv ${fname} user code", 
        "    // by default - do nothing",
        "    // -^^^ end of user code. do not modify",
        "}"])

builder.generate(generated_result)

# ----------------------------------------------------------
