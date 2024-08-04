
# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

# Data objects C++ class generator. Generated classes are serializable 
# and have all necessary comparision and can be constructed from string
# text format as well as could be dumped in human readable form
# Generated data objects could be used as normal, but highly specialized 
# types providing full usage type controll of C++ compiler.

from .meth import code_generator
from .tools import general_name, file_name, code_block
from inspect import currentframe, getmodule

class data_types_generator:

    def __init__(self, solution_root_folder):
        self.solution_root_folder = file_name(solution_root_folder).get_full_file_name()
        self.generated_files = []
        self.generator = code_generator( globals() )
        self.need_integer_toolbox = False
        self.need_string_toolbox = False
        self.need_enum_toolbox = False

    def define_output_directories(self, target_folder, library_files_folder):
        self.library_files_folder = file_name(library_files_folder)
        self.target_folder = file_name(target_folder)
        self.meth_directory = file_name(__file__ + "/..");
        self.template_folder = file_name(self.meth_directory.get_full_file_name() + "/templates/data_types")
        tools_relative_path = self._add_path_separator_if_needed(self.library_files_folder.get_name_and_path_relative_to(self.target_folder.get_full_file_name()))
        tools_relative_path = self._add_path_separator_if_needed(tools_relative_path)
        self.generator.define("meth_directory",self.meth_directory.get_name_and_path_relative_to(self.solution_root_folder))
        self.generator.define("tools_path", tools_relative_path)
        self.generator.define("export_specifier", "")
        self.generator.define("export_definition_include", "")

    def define_export(self, export_specifier, export_definition_include):
        self.export_specifier = export_specifier
        self.generator.define("export_specifier", export_specifier)
        self.export_definition_include = export_definition_include

    def create_integer_type(self, namespace, name, *, base_type="int", default_value=0, min_value=None, max_value=None, compareable=False, ordered=False):
        self._set_name(namespace, name)
        self._set_base_type(base_type, default_value)
        self._set_range(min_value, max_value)
        self._set_comparision(compareable, ordered)
        self._set_template("integer_type.h.template", ".h")
        self._set_trace()
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)
        self.need_integer_toolbox = True

    def create_string_type(self, namespace, name, *, default_value = "", max_length=None, compareable=False, ordered=False, compare_strategy="Default"):
        self._set_name(namespace, name)
        self._set_type_properties(max_length, default_value)
        self._set_comparision(compareable, ordered, compare_strategy)
        self._set_template("string_type.h.template", ".h")
        self._set_trace()
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)
        self.need_string_toolbox = True

    def create_enum_type(self, namespace, name, values, *, default_value = None, compareable=False, ordered=False):
        self._set_name(namespace, name)
        self._set_values(values, default_value)
        self._set_comparision(compareable, ordered)
        self._set_template("enum_type.h.template", ".h")
        self._set_trace()
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)
        self._set_template("enum_type.cpp.template", ".cpp")
        self._set_trace()
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)
        self.need_enum_toolbox = True

    def add_toolbox_files(self):
        need_common_tools = False
        if self.need_integer_toolbox:
            need_common_tools = True
        if self.need_enum_toolbox:
            need_common_tools = True
        if self.need_string_toolbox:
            self._create_library_file("meth_toolbox_strings.h", "_meth_toolbox_strings.h.template")
            self._create_library_file("meth_toolbox_strings.cpp", "_meth_toolbox_strings.cpp.template")
            need_common_tools = True
        if need_common_tools:
            self._create_library_file("meth_toolbox_value_error.h", "_meth_toolbox_value_error.h.template")
            self._create_library_file("meth_toolbox_deserialization_interface.h", "_meth_toolbox_deserialization_interface.h.template")
            self._create_library_file("meth_toolbox_deserialization_interface.cpp", "_meth_toolbox_deserialization_interface.cpp.template")
            self._create_library_file("meth_toolbox_serialization_interface.h", "_meth_toolbox_serialization_interface.h.template")
            self._create_library_file("meth_toolbox_serialization_interface.cpp", "_meth_toolbox_serialization_interface.cpp.template")
    
    def _set_values(self, values, default_value):
        self.values = values
        self.generator.define("values",values)
        if not default_value:
            default_value = values[0]
        self.default_value = default_value
        self.generator.define("default_value", str(default_value))
        if len(values) < 256:
            self.base_type = "uint8_t"
        elif len(values) < 65536:
            self.base_type = "uint16_t"
        else:
            self.base_type = "uint32_t"
        self.generator.define("base_type", self.base_type)
 
    def _add_path_separator_if_needed(self, path):
        if not path:
            return ""
        if path[-1] != '/':
            return path + '/'
        return path

    def _create_library_file(self, result_file_name, template_name):
        self._set_trace()
        self.generator.define("file_name", self.output_file_name.get_name_and_path_relative_to(self.solution_root_folder))
        self._set_template(template_name, "")
        self.output_file_name = file_name(self.library_files_folder.get_full_file_name() + "/" + result_file_name)
        created_file_location = self._generate()
        self.generated_files.append(created_file_location)

    def _set_name(self, namespace, name):
        self.namespace = general_name(namespace)
        self.generator.define("namespace",self.namespace.CamelCase())
        self.type_name = general_name(name)
        self.generator.define("class_name",self.type_name.CamelCase())
        self.generator.define("field_name",self.type_name.lowercase())
        self.header_file_name = self.namespace.lowercase() + "_" + self.type_name.lowercase() + ".h"
        self.generator.define("header_file_name", self.header_file_name)

    def _set_base_type(self, base_type, default_value):
        self.base_type = base_type
        self.generator.define("base_type", base_type)
        self.default_value = default_value
        self.generator.define("default_value", str(default_value))

    def _set_type_properties(self, max_length, default_value):
        self.max_length = max_length
        self.generator.define("max_length", max_length)
        self.default_value = default_value
        self.generator.define("default_value", str(default_value))
        if max_length < 256:
            self.generator.define("length_cathegory", "Short")
        elif max_length < 65536:
            self.generator.define("length_cathegory", "Long")
        else:
            self.generator.define("length_cathegory", "VeryLong")

    def _set_range(self, min_value, max_value):
        if not min_value is None and not max_value is None:
            self.generator.define("min_value", str(min_value))
            self.generator.define("max_value", str(max_value))
            self.generator.define("range_controll", True)
        else:
            self.generator.define("min_value", 0)
            self.generator.define("max_value", 0)
            self.generator.define("range_controll", False)

    def _set_comparision(self, compareable, ordered, compare_strategy=None):
        if ordered:
            self.generator.define("compareable", True)
            self.generator.define("ordered", ordered)
            self.generator.define("compareable_flag_text", "true")
            self.generator.define("ordered_flag_text", "true")
        elif compareable:
            self.generator.define("compareable", compareable)
            self.generator.define("ordered", False)
            self.generator.define("compareable_flag_text", "true")
            self.generator.define("ordered_flag_text", "false")
        else:
            self.generator.define("compareable", False)
            self.generator.define("ordered", False)
            self.generator.define("compareable_flag_text", "false")
            self.generator.define("ordered_flag_text", "false")
        if not compare_strategy is None:
            self.generator.define("compare_strategy", str(compare_strategy))

    def _set_template(self, template_name, file_type):
        self.template_name = file_name(self.template_folder.get_full_file_name() + "/" + template_name)
        self.generator.define("template_location", self.template_name.get_name_and_path_relative_to(self.solution_root_folder))
        self.output_file_name = file_name(self.target_folder.get_full_file_name() + "/" + self.namespace.lowercase() + "_" + self.type_name.lowercase() + file_type)
        self.generator.define("file_name", self.output_file_name.get_name_and_path_relative_to(self.solution_root_folder))

    def _set_trace(self):
        frame = currentframe().f_back.f_back
        generator_code_line = frame.f_lineno
        generator_code_file = file_name(getmodule(frame).__file__)
        self_generator_location = generator_code_file.get_name_and_path_relative_to(self.solution_root_folder) + " [" + str(generator_code_line) + "]"
        self.generator.define("generator_location", self_generator_location)

    def _generate(self):
        self.generator.define("export_definition_include", file_name(self.export_definition_include).get_name_and_path_relative_to(self.output_file_name.get_full_path()))
        self.generator.set_template(self.template_name.get_full_file_name())
        self.generator.generate(self.output_file_name.get_full_file_name())
        return self.output_file_name.get_full_file_name()
    
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

# -------------------------------------------------------------------
