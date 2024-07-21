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

# class geerating code supporting c++ enums
class cpp_enum:

    def __init__(self, enum_values):
        self.elements = enum_values   
        
    def _get_max_length(self):
        max_length = 0
        for text in self.elements:
            length = len(text)
            if length > max_length:
                max_length = length
        return max_length
        
    def _get_min_length(self, elements):
        if len(elements) == 0:
            return 0
        min_length = len(elements[0])
        for text in elements[1:]:
            length = len(text)
            if length < min_length:
                min_length = length
        return min_length
        
    def _get_items_in_line(self, width):
        if width < 12:
            return 4
        else:
            return 2
    
    def get_items_as_list(self, quotation = ''):
        item_width = self._get_max_length()
        max_items_in_line = self._get_items_in_line(item_width)
        line = ""
        items_in_line = 0
        result = []
        if len(self.elements) > 0:
            for text in self.elements[:-1]:
                line = line + quotation + text + quotation
                items_in_line = items_in_line + 1
                if items_in_line == max_items_in_line:
                    result.append(line)
                    line = ""
                    items_in_line = 0
                else:
                    line = line + "," + (" " * (1 + item_width - len(text)))
            line = line + quotation + self.elements[-1] + quotation
        if line != "":
            result.append(line)
        return result
         
    def code_of_convert_from_string(self):
        return code_block(self._generate_result("", self.elements))
        
    def _generate_case(self, prefix, case_map):
        lines_of_code = []
        index = list(case_map.keys())
        index.sort()
        for case_key in index[:-1]:
            lines_of_code.append(prefix + "case " + str(case_key) + ":")
            value = case_map[case_key]
            lines_of_code = lines_of_code + self._generate_result(prefix + "    ", value)
        lines_of_code.append(prefix + "default:")
        lines_of_code = lines_of_code + self._generate_result(prefix + "    ", case_map[index[-1]])
        return lines_of_code

    def _generate_result(self, prefix, value_to_return):
        if len(value_to_return) == 1:
            return [ prefix + "return " + value_to_return[0] + ";" ]
        else:
            case_map, position = self._create_best_selection_map(value_to_return)
            selector = self._get_selector(position)
            if len(case_map) == 2:
                condition_value, first, second = self._generate_if_data(case_map)
                return [prefix + "if( " + selector + " == " + str(condition_value) + " )"] + \
                    self._generate_result(prefix + "    ", first) + \
                    [ prefix + "else"] + \
                    self._generate_result(prefix + "    ", second)
            else:
                return [prefix + "switch( " + selector + " )", "{"] + \
                    self._generate_case(prefix, case_map) + \
                    [ prefix + "};" ]
    
    def _get_selector(self, char_position):
        if (char_position < 0):
            return "text.size()"
        else:
            return "text[" + str(char_position) +"]"
    
    def _generate_if_data(self, case_map):
        keys = list(case_map.keys())
        keys.sort()
        return keys[0], case_map[keys[0]], case_map[keys[1]]
    
    def _create_selection_map_at_char(self, values, position):
        result_map = { }
        for value in values:
            key = "'" + value[position] + "'"
            if key in result_map.keys():
                result_map[key].append(value)
            else:
                result_map[key] = [ value ]
        return result_map
                    
    def _create_selection_map_at_length(self, values):
        result_map = { }
        for value in values:
            key = len(value)
            if key in result_map.keys():
                result_map[key].append(value)
            else:
                result_map[key] = [ value ]
        return result_map
                    
    def _create_best_selection_map(self, values):
        best_map = { }
        best_position = -1
        for i in range(0, self._get_min_length(values)):
            map_case = self._create_selection_map_at_char(values, i)
            if len(map_case) > len(best_map):
                best_map = map_case
                best_position = i
        map_by_len = self._create_selection_map_at_length(values)
        if len(map_by_len) >= len(best_map):
            return map_by_len, -1
        else:
            return best_map, best_position
 
# ----------------------------------------------------------
