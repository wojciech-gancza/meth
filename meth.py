#--------------------------------------------------------------------------

import methtools
import re
import math

#--------------------------------------------------------------------------
# assumptions:
# - files are processed line by line
# - values of ${...} are not interpreted. No ${...} calculation in values
# - no error handling is made. This is development tools - errors are just errors
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

#--------------------------------------------------------------------------

class Metamorph:

    def __init__(self, patterns_path, output_path):
        self.patterns_path = str(patterns_path)
        self.output_path = str(output_path)

    def generate(self, pattern_file_name, output_file_name, variable_map):
        file_pattern_reader = methtools.FileReader(self.patterns_path + "/" + pattern_file_name)
        output = methtools.GeneratedFile(self.output_path + "/" + output_file_name);

        variable_map["format"] = ListFormatter()
        self._morph(file_pattern_reader, output, variable_map)

        output.save()

    def _morph(self, pattern_lines_source, output, variable_map, evalueate_expressions=True):
        while not pattern_lines_source.is_eof():
            pattern_file_line = pattern_lines_source.get_line()
            line = methtools.DecomposedText(pattern_file_line)
            while line.expression:
                buffered_output = methtools.OutputAllExceptLast(output, line.before_expression)

                if line.expression[0] == "#":
                    command_text = methtools.ParameterExtractor(line.expression)
                    just_command = command_text.pop_word()

                    # include command includes separate file (path relative to patterns folder)
                    # interpreting it with additional variables passed in command
                    # text before statement is used as first line prefix, other lines are prefixed 
                    # by the whitespaced prefix
                    if just_command == "#include":
                        if evalueate_expressions:
                            included_file_name = eval(command_text.pop_word(), variable_map)
                            include_file_reader = methtools.FileReader(self.patterns_path + "/" + included_file_name)
                            parameters = eval("{ " + command_text.tail + " }", variable_map)
                            variable_map_with_parameters = { **variable_map, **parameters }
                            self._morph(include_file_reader, buffered_output, variable_map_with_parameters)
                            result_line = buffered_output.buffered_last_output + line.after_expression                    
                        else:
                            result_line = line.before_expression + line.after_expression 
                    # conditionals placing a part of code conditionally: 
                    # ${#if ...} ... ${#end}, or
                    ### ${#if ...} ... ${#else} ... ${#end}
                    elif just_command == "#if":
                        condition = eval(command_text.tail, variable_map)
                        if condition:
                            conditional_input = methtools.FirstReadThis(line.before_expression + line.after_expression, pattern_lines_source)
                            evaluating_block_result = self._morph(conditional_input, output, variable_map, evalueate_expressions)
                            if evaluating_block_result.expression[0:4] == "#end":
                                result_line = evaluating_block_result.before_expression + evaluating_block_result.after_expression
                            elif evaluating_block_result.expression[0:5] == "#else":
                                input_to_skip = methtools.FirstReadThis(evaluating_block_result.after_expression, pattern_lines_source)
                                dummy_output = methtools.DummyOutput()
                                skipping_block_result = self._morph(input_to_skip, dummy_output, variable_map, False)
                                result_line = evaluating_block_result.before_expression + skipping_block_result.after_expression
                        else:
                            input_to_skip = methtools.FirstReadThis(line.after_expression, pattern_lines_source)
                            dummy_output = methtools.DummyOutput()
                            skipping_block_result = self._morph(input_to_skip, dummy_output, variable_map, False)
                            if skipping_block_result.expression[0:4] == "#end":
                                result_line = line.before_expression + skipping_block_result.after_expression
                            elif skipping_block_result.expression[0:5] == "#else":
                                conditional_input = methtools.FirstReadThis(line.before_expression + skipping_block_result.after_expression, pattern_lines_source)
                                evaluating_block_result = self._morph(conditional_input, output, variable_map, evalueate_expressions)
                                result_line = evaluating_block_result.before_expression + evaluating_block_result.after_expression
                    
                    # loops allow generation of code in loops
                    # with control variable traversing a list of values         
                    elif just_command == "#for":
                        control_variable_name = command_text.pop_word()
                        command_text.pop_word() # should read 'in'
                        values = eval(command_text.tail, variable_map)
                        if values is None:
                            values = []
                        elif type(values) is not list:
                            values = [ str(values) ]
                        if values == []:
                            input_to_skip = methtools.FirstReadThis(line.after_expression, pattern_lines_source)
                            dummy_output = methtools.DummyOutput()
                            skipping_block_result = self._morph(input_to_skip, dummy_output, variable_map, False)
                            result_line = line.before_expression + skipping_block_result.after_expression
                        else:
                            before_iteration = line.before_expression
                            for value in values:
                                enchaced_variable_map = { **variable_map, control_variable_name : value }
                                input_to_evaluate = methtools.FirstReadThis(before_iteration + line.after_expression, pattern_lines_source.copy())
                                evaluating_block_result = self._morph(input_to_evaluate, output, enchaced_variable_map, evalueate_expressions)
                                before_iteration = evaluating_block_result.before_expression
                            pattern_lines_source = input_to_evaluate.decorated_reader
                            result_line = before_iteration + evaluating_block_result.after_expression

                    # just return controll to recursive caller indicationg end of block
                    elif just_command == "#end":
                        return line
                    elif just_command == "#else":
                        return line
                else:
                    # expression value can be any type - in worst case it will be
                    # casted to string by python. But None represents empty string,
                    # and lists are list of lines
                    if evalueate_expressions:
                        placeholder_value = eval(line.expression, variable_map)
                    else:
                        placeholder_value = ""
                    #------------------------------------------------------ ----
                    if placeholder_value is None or placeholder_value == []:
                        buffered_output.append("")
                    elif type(placeholder_value) is list:
                        for value in placeholder_value[:-1]:
                            buffered_output.append( str(value) + "\n" )
                        buffered_output.append( str(placeholder_value[-1]))
                    else:
                        buffered_output.append( str(placeholder_value) )
                    result_line = buffered_output.buffered_last_output + line.after_expression

                line = methtools.DecomposedText(result_line)
            else:
                output.append(line.whole_text)
        return None
 
#--------------------------------------------------------------------------
