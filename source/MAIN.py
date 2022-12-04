# ----------------------------------------------------------

from meth import code_generator, code_block, list_walker
from tools import general_name, cpp_enum, file_name

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

class simple_data_object_builder:

    def __init__(self, namespace, target_path, base_path = ".."):
        self.generator = code_generator(globals())
        self.target_path = target_path
        self._set_base_path(base_path)
        generator_name_and_path = file_name(__file__)
        self.generator.define("generator_name_and_path", generator_name_and_path.get_name_and_path_relative_to(base_path))
        self.generator.define("namespace", namespace)
        
    def create_simple_type(self, name, base_type, default_value):
        self.generator.define("base_type", base_type)
        type_name = general_name(name)
        self._generate_simple_type_header_file("simple_type.h.template", type_name, default_value)
        
    def create_string_type(self, name, default_value = ""):
        self.generator.define("base_type", "std::string")
        self.generator.define("include_with_base_type", "<string>")
        self.generator.define("is_move_allowed", True)
        type_name = general_name(name)
        self._generate_simple_type_header_file("object_type.h.template", type_name, default_value)
        
    def create_enum_type(self, name, enum_values, base_type = "int", default_value = None):
        self.generator.define("base_type", base_type)
        self.generator.define("enum_values", enum_values)
        if default_value is None:
            default_value = enum_values[0]
        type_name = general_name(name)
        self._generate_simple_type_header_file("enum_type.h.template", type_name, default_value)
        
    def _generate_simple_type_header_file(self, template_name, type_name, default_value):
        self.generator.define("type_name", type_name.CamelCase())
        self.generator.define("default_value", default_value) 
        self._select_template(template_name)
        output_file_name = self._create_header_file_name(type_name)
        self.generator.generate(output_file_name)
    
    def _create_header_file_name(self, type_name):
        output_file_name_and_path = file_name(self.target_path + type_name.lowercase() + ".h")
        self.generator.define("output_file_name_and_path", output_file_name_and_path.get_name_and_path_relative_to(self.base_path))
        return output_file_name_and_path.get_full_file_name()
     
    def _select_template(self,  template_name):
        template_name_and_path = file_name("../templates/simple_data_objects/" + template_name)
        self.generator.define("template_name_and_path", template_name_and_path.get_name_and_path_relative_to(self.base_path))
        self.generator.set_template(template_name_and_path.get_full_file_name())
     
    def _set_base_path(self, base_path):
        path = file_name(base_path)
        self.base_path = path.get_full_file_name()

builder = simple_data_object_builder("Data", "../test/_generated/")
builder.create_simple_type("story points", "uint16_t", 0)
builder.create_string_type("comment")
builder.create_enum_type("type", ["Task", "Index", "Sprint"])

# ----------------------------------------------------------
