# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

# Simple data objects builder is an example of use of code generator for
# creation of simple data objects which could be used as messages or 
# database record representation 

from meth import code_generator
from tools import general_name, cpp_enum, file_name

class simple_data_object_builder:

    def __init__(self, globals_map, namespace, target_path, base_path = ".."):
        self.generator = code_generator(globals_map)
        self.target_path = target_path
        self._set_base_path(base_path)
        generator_name_and_path = file_name(__file__)
        self.generator.define("generator_name_and_path", generator_name_and_path.get_name_and_path_relative_to(base_path))
        self.generator.define("namespace", namespace)
        
    def create_simple_type(self, name, base_type, default_value):
        self.generator.define("base_type", base_type)
        type_name = general_name(name)
        self._generate_simple_type_source_file("simple_type.h.template", type_name, default_value, "h")
        
    def create_string_type(self, name, default_value = ""):
        self.generator.define("base_type", "std::string")
        self.generator.define("include_with_base_type", "<string>")
        self.generator.define("is_move_allowed", True)
        type_name = general_name(name)
        self._generate_simple_type_source_file("object_type.h.template", type_name, default_value, "h")
        
    def create_enum_type(self, name, enum_values, use_strings = False, base_type = "int", default_value = None):
        self.generator.define("base_type", base_type)
        self.generator.define("enum_values", enum_values)
        self.generator.define("use_strings_support", use_strings)
        if default_value is None:
            default_value = enum_values[0]
        type_name = general_name(name)
        self._generate_simple_type_source_file("enum_type.h.template", type_name, default_value, "h")
        if use_strings:
            self.generator.define("header_file_name", type_name.lowercase())
            self._generate_simple_type_source_file("enum_type.cpp.template", type_name, default_value, "cpp")
        
    def create_composite(self, name, element_names):
        self.generator.define("element_types", [general_name(x) for x in element_names])
        type_name = general_name(name)
        self._generate_simple_type_source_file("composite_type.h.template", type_name, "", "h")
        
    def _generate_simple_type_source_file(self, template_name, type_name, default_value, extension):
        self.generator.define("type_name", type_name.CamelCase())
        self.generator.define("default_value", default_value) 
        self._select_template(template_name)
        output_file_name = self._create_file_name(type_name, extension)
        self.generator.generate(output_file_name)
    
    def _create_file_name(self, type_name, extenstion):
        output_file_name_and_path = file_name(self.target_path + type_name.lowercase() + "." + extenstion)
        self.generator.define("output_file_name_and_path", output_file_name_and_path.get_name_and_path_relative_to(self.base_path))
        return output_file_name_and_path.get_full_file_name()
     
    def _select_template(self,  template_name):
        template_name_and_path = file_name("../templates/simple_data_objects/" + template_name)
        self.generator.define("template_name_and_path", template_name_and_path.get_name_and_path_relative_to(self.base_path))
        self.generator.set_template(template_name_and_path.get_full_file_name())
     
    def _set_base_path(self, base_path):
        path = file_name(base_path)
        self.base_path = path.get_full_file_name()

# ----------------------------------------------------------
