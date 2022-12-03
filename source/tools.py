# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import os

# tools classes and objects
# some nice to use tools which could be usefull when generating the code

from meth import code_block

# class transforming string to identifier with variours notations
class general_name:

    def __init__(self, name):
        self.bare_name = name.split()
        
    def CamelCase(self):
        return "".join([x.capitalize() for x in self.bare_name])
        
    def lowercaseCamel(self):
        if len(self.bare_name):
            first = self.bare_name[0].lower()
            return first + "".join([x.capitalize() for x in self.bare_name[1:]])
        else:
            return ""
        
    def lowercase(self):
        return "_".join([x.lower() for x in self.bare_name])
        
    def UPPERCASE(self):
        return "_".join([x.upper() for x in self.bare_name])
 
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
            line = line + self.elements[-1]
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
                    self._generate_result(prefix + "    ", second) + \
                    [ prefix + "};" ]
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
 
class file_name:
    
    def __init__(self, file_with_path):
        file_with_path = self._change_directory_separators(file_with_path)
        if not self._is_full_path(file_with_path):
            working_directory = self._get_cwd()
            file_elements = file_with_path.split("/")
            working_directory = working_directory.split("/")
            while file_elements:
                if file_elements[0] == "" or file_elements[0] == ".":
                    file_elements = file_elements[1:]
                elif file_elements[0] == "..":
                    file_elements = file_elements[1:]
                    working_directory = working_directory[:-2]
                else:
                    break
            file_with_path = working_directory + file_elements
            self.full_file_name = "/".join(file_with_path)
        else:
            self.full_file_name = file_with_path
    
    def get_name_and_path_relative_to(self, base_path):
        if base_path[-1] == "/":
            base_path = base_path[:-1]
        file = self.full_file_name.split("/")
        path = base_path.split("/")
        while file and path and file[0] == path[0]:
            file = file[1:]
            path = path[1:]
        file_name = "/".join(file)
        if path:
            file_name = ("../" * len(path)) + file_name
        else:
            file_name = "./" + file_name
        return file_name
        
    def get_full_file_name(self):
        return self.full_file_name
        
    def _get_cwd(self):
        cwd = self._change_directory_separators(os.getcwd()) + "/"
        return cwd
        
    def _change_directory_separators(self, path):
        return path.replace("\\", "/")
        
    def _is_full_path(self, path):
        if len(path) == 0:
            return False
        if path[0] == "/":
            return True
        if len(path) > 3 and path[1:3] == ":/":
            return True
        return False
        
# ----------------------------------------------------------

