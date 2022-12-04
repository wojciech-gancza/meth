# ----------------------------------------------------------

from meth import code_generator, code_block, list_walker
from tools import general_name, cpp_enum, file_name
from simple_data_objects import simple_data_object_builder

"""
# Main functionality of source file generator. It 
template            = "../test/03-1-source_template.cpp"
generated_result    = "../test/_generated/03-1-result.cpp"

builder = code_generator(globals())
builder.set_template(template)

builder.define("enum1", cpp_enum(["E1X223", "BETA", "SOMETHONG_ELSE", "X", "KULA314", "MOVIE", "DDS", "MDF", "XRAYMACHINE", "FOXTROT", "B554"]))
builder.define("enum2", cpp_enum(["X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "XA", "XB", "XC", "XD", "XE", "XF"]))
builder.define("emitE1", True)
builder.define("convert_to_string", False)

def show_metastatement_search_result(line, result, starting_at):
    if result is None:
        print("Metastatement was not found when analising '" + line + "' starting at position " + str(starting_at))
    else:
        part = line[result.start:result.end]
        print("In line '" + line + "' found metastatement '" + part + "' metastatement depth change is: " + str(result.depth_change))

line = "xxxcs${#END}dddsdsds"
x = builder._check_metastatement(line, 3)
show_metastatement_search_result(line, x, 3)

line = "xxxcs${ #  FOR x : collection() }dddsdsds"
x = builder._check_metastatement(line, 0)
show_metastatement_search_result(line, x, 0)

line = "${#IF x}"
x = builder._check_metastatement(line, 0)
show_metastatement_search_result(line, x, 0)

print("----------------------------")

line = "something before${#IF condition}under condition${#ELSE}elsewere${#END}after condition"
x = builder._read_metastatement_body("under condition${#ELSE}elsewere${#END}after condition", None)
print(x)

file_content = ["first ${#IF xxx}something in same line", \
                "${#IF}", \
                "conditional", \
                "${#END}", \
                "second line under if", \
                "", \
                "In this line would be 'ELSE' ${#ELSE}this is part of else", \
                "X${#FOR x : col}in loop${#END}Y", \
                "After this line is juse END", \
                "${#END}" ]
lines = list_walker(file_content)
lines.get_line() # skip line passed down as partial parameters
x = builder._read_metastatement_body("something in same line", lines)
print(x)

# ----------------------------------------------------------
builder.define("someMap", { "A": 12, "B": 127, "C": 998543 })

builder.generate(generated_result)
"""
# ----------------------------------------------------------


#type_name = general_name("story points")
#base_type = "uint16_t"
#default_value = "0"
#namespace = "Data"
#base_path = "C:/Users/wgan/Desktop/WGan/PROGRAMOWANIE/meth/"

#output_file_name_and_path   = file_name("../test/_generated/" + type_name.lowercase() + ".h")
#generator_name_and_path     = file_name(__file__)
#template_name_and_path      = file_name("../templates/simple_type.h.template")

#builder = code_generator(globals())
#builder.set_template("../templates/simple_type.h.template")

#builder.define("output_file_name_and_path", output_file_name_and_path.get_name_and_path_relative_to(base_path))
#builder.define("generator_name_and_path", generator_name_and_path.get_name_and_path_relative_to(base_path))
#builder.define("template_name_and_path", template_name_and_path.get_name_and_path_relative_to(base_path))
#builder.define("namespace", namespace)
#builder.define("type_name", type_name.CamelCase())
#builder.define("base_type", base_type)
#builder.define("default_value", default_value)

#builder.generate(output_file_name_and_path.get_full_file_name())

builder = simple_data_object_builder(globals(), "Data", "../test/_generated/")
builder.create_simple_type("story points", "uint16_t", 0)
builder.create_string_type("comment")
builder.create_enum_type("type", ["Task", "Index", "Sprint"], True)

# ----------------------------------------------------------
