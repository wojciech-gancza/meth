#--------------------------------------------------------------------------

import os
import math

#--------------------------------------------------------------------------

class Environment:

    def __init__(self):
        self.script_path = AbsolutePath(__file__).parent()
        self.patterns_path = self.script_path.create_changed_by("patterns")

#--------------------------------------------------------------------------

class ListFormatter:

    def comma_separated(self, list_of_texts):
        if not self._is_it_list_to_format(list_of_texts):
            return self._convert_to_string(list_of_texts)
        return [ line_of_text + "," for line_of_text in list_of_texts[:-1] ] + [ list_of_texts[-1] ]

    def inheritance_list(self, list_of_texts):
        if not self._is_it_list_to_format(list_of_texts):
            return self._convert_to_string(list_of_texts, ": ")
        return [ ": " + list_of_texts[0] ] + [ ", " + line_of_text for line_of_text in list_of_texts[1:] ]

    def multicolumn_list(self, list_of_texts, *, max_width=120, min_column_width=8):
        if not self._is_it_list_to_format(list_of_texts):
            return self._convert_to_string(list_of_texts)
        list_with_commas = self.comma_separated(list_of_texts);
        column_width = self._calculate_column_width(min_column_width, list_with_commas)
        columns_count = math.floor(max_width / column_width)
        if columns_count < 2:
            return list_with_commas
        rows_list = []
        while list_with_commas != []:
            if len(list_with_commas) > columns_count:
                current_row = list_with_commas[:columns_count]
                list_with_commas = list_with_commas[columns_count:]
            else:
                current_row = list_with_commas
                list_with_commas = []
            row_text = "".join(self._aligh_width_with_spaces(column_width, current_row[:-1])) + current_row[-1]
            rows_list.append(row_text)
        return rows_list

    def bitmasks_enum(self, list_of_texts):
        if not self._is_it_list_to_format(list_of_texts):
            list_of_texts = [ self._convert_to_string(list_of_texts) ]
        list_of_texts = self._decorate_with_bitmasks(list_of_texts)
        return self.comma_separated(list_of_texts)

    def bitmasks_constants(self, list_of_texts, prefix = ""):
        if not self._is_it_list_to_format(list_of_texts):
            list_of_texts = [ self._convert_to_string(list_of_texts) ]
        list_of_texts = [prefix + text for text in list_of_texts]
        list_of_texts = self._decorate_with_bitmasks(list_of_texts)
        return [ text +";" for text in list_of_texts]

    def _is_it_list_to_format(self, list_of_texts):
        return ( type(list_of_texts) == list and list_of_texts != [] )

    def _convert_to_string(self, list_of_texts, prefix = ""):
        if list_of_texts:
            return prefix + str(list_of_texts)
        else:
            return ""
 
    def _calculate_column_width(self, min_column_width, list_of_texts):
        column_width = min_column_width
        for text in list_of_texts:
            if len(text)+1 > column_width:
                column_width = len(text)+1
        return column_width

    def _aligh_width_with_spaces(self, test_width, list_of_texts_to_align):
        return [ text + " " * (test_width - len(text) ) for text in list_of_texts_to_align ]

    def _decorate_with_bitmasks(self, list_of_texts):
        texts_width = self._calculate_column_width(4, list_of_texts)
        aligned_list = self._aligh_width_with_spaces(texts_width, list_of_texts)
        hex_value_format = "= 0x{:0" + str(math.ceil(len(list_of_texts) / 4)) + "x}"
        assignments = []
        current_value = 1
        for text in aligned_list:
            assignments.append(text + hex_value_format.format(current_value) )
            current_value = 2 * current_value
        return assignments

#--------------------------------------------------------------------------

class AbsolutePath:

    def __init__(self, path):
        full_path = os.path.abspath(str(path))
        self.full_path = full_path.replace("\\", "/")

    def parent(self):
        path = os.path.dirname(self.full_path)
        return AbsolutePath(path)

    def create_changed_by(self, local_path):
        return AbsolutePath( self.full_path + "/" + local_path )

    def get_relative_to(self, absolute_path):
        absolute_path = AbsolutePath(absolute_path)
        return os.path.relpath(self.full_path, absolute_path.full_path).replace("\\", "/")

    def __str__(self):
        return self.full_path

    def get_as_directory(self):
        return self.full_path + "/"

#--------------------------------------------------------------------------

class Name:

    def __init__(self, name_as_space_separated_text):
        name_blocks = name_as_space_separated_text.split(":")
        namespaces = name_blocks[:-1]
        undecorated_name = name_blocks[-1]
        self.namespace = [ self._convert_to_word_list(namespace) for namespace in namespaces]
        self.undecorated_name = self._convert_to_word_list(undecorated_name)

    def lowercaseCamelName(self): # objects, variables
        return self.undecorated_name[0] + self._convert_to_camelcase_text(self.undecorated_name[1:])

    def UppercaseCamelName(self): # classes
        return self._convert_to_camelcase_text(self.undecorated_name)

    def lowercase_name(self): # objects, fields, parameters, variables
        return self._convert_to_lowercase_text(self.undecorated_name)

    def UPPERCASE_NAME(self): # defines, macrodefinitions, constants
        return self.lowercase_name().upper()

    def UppercaseCamelsNamespaces(self): # list of namespaces
        return [self._convert_to_camelcase_text(element) for element in self.namespace]

    def lowercase_namespace_and_name(self, default_namespace = None): # file names
        if self.namespace:
            elements = [self._convert_to_lowercase_text(namespace) for namespace in self.namespace]
            elements.append(self.lowercase_name())
            return self._convert_to_lowercase_text(elements)
        elif default_namespace:
            namspace = Name(default_namespace)
            elements = [namspace.lowercase_namespace_and_name(), self.lowercase_name()]
            return self._convert_to_lowercase_text(elements)
        else:
            return self.lowercase_name()

    def _convert_to_word_list(self, name):
        return [word.strip() for word in name.split(" ") if word.strip() ]

    def _convert_to_lowercase_text(self, array_of_words):
        return "_".join( [word.lower() for word in array_of_words] )

    def _convert_to_camelcase_text(self, array_of_words):
        return "".join( [word.capitalize() for word in array_of_words] )

#--------------------------------------------------------------------------

class EnumCodeGenerator:

    def __init__(self, names):
        self.names_texts = [name.UPPERCASE_NAME() for name in names]

    def generate_code(self):
        return self._generate_code(self.names_texts)

    def _generate_code(self, names_list):
        if len(names_list) == 1:
            return [ "return E_" + names_list[0] + ";" ]
        switch_statement_data = self._check_best_way_to_distinguish(names_list)
        switch_expression = switch_statement_data[0]
        switch_cases = switch_statement_data[1]
        precondition_length = switch_statement_data[2]
        switch_case_keys = list(switch_cases.keys())
        switch_case_keys.sort()
        if len(switch_cases) == 2:
            first_key = switch_case_keys[0]
            first_key_code = self._indent( self._generate_code(switch_cases[first_key]) ) 
            second_key = switch_case_keys[1]
            second_key_code = self._indent( self._generate_code(switch_cases[second_key]) ) 
            return [ "if (" + switch_expression + " == " + first_key + ")", "{"] + \
                   self._indent(first_key_code) + \
                   [ "}", "else", "{" ] + \
                   self._indent(second_key_code) + \
                   [ "}" ] 
        else:
            result_code = []
            if precondition_length:
                result_code = ["if (text.length() < " + str(precondition_length) + ")", "{", "  return E_" + names_list[-1] + ";", "}"]
            result_code = result_code + [ "switch (" + switch_expression + ")", "{" ]
            for key in switch_case_keys[:-1]:
                key_code = self._indent( self._generate_code(switch_cases[key]) )
                result_code = result_code + self._indent( ["case " + key + ":", "{"] + key_code + ["}"])   
            last_key = switch_case_keys[-1]
            last_key_code = self._indent( self._generate_code(switch_cases[last_key]) ) 
            return result_code + self._indent(["default:", "{"] + last_key_code + ["}"]) + ["}"]

    def _indent(self, code_block):
        return [ "  " + code_line for code_line in code_block ]

    def _check_best_way_to_distinguish(self, names_list):
        select_by_length = self._group_by_length(names_list)
        select_by_character_at_position = [ ]
        consider_characters_count = min(select_by_length.keys())
        for character_index in range(consider_characters_count):
            select_by_character_at_position.append(self._gruop_by_character(character_index, names_list))
        bigest_difference_by_character = max([len(seleced_by_character_at_position) for seleced_by_character_at_position in select_by_character_at_position])
        difference_by_lenght = len(select_by_length)
        if difference_by_lenght > bigest_difference_by_character:
            return ("text.length()", select_by_length, None)
        else:
            for character_index in range(consider_characters_count):
                if len(select_by_character_at_position[character_index]) == bigest_difference_by_character:
                     return ("text[" + str(character_index) + "]", select_by_character_at_position[character_index], consider_characters_count)

    def _gruop_by_character(self, character_index, names_list):
        selector_map = { }
        for name in names_list:
            character = name[character_index]
            if character in selector_map.keys():
                selector_map[character].append(name)
            else:
                selector_map["'" + character + "'"] = [ name ]
        return selector_map

    def _group_by_length(self, names_list):
        selector_map = { }
        for name in names_list:
            length = len(name)
            if length in selector_map.keys():
                selector_map[length].append(name)
            else:
                selector_map[length] = [name]
        return selector_map

#--------------------------------------------------------------------------
