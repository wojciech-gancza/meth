#--------------------------------------------------------------------------

import methtools

#--------------------------------------------------------------------------
# assumptions:
# - files are processed line by line
# - values of ${...} are not interpreted. No ${...} calculation in values
# - no error handling is made. This is development tools - errors are just errors
#--------------------------------------------------------------------------

class Metamorph:

    def __init__(self, patterns_path):
        self.patterns_path = str(patterns_path)

    def generate(self, pattern_file_name, output_file_name, variable_map):
        file_pattern_reader = methtools.FileReader(self.patterns_path + "/" + pattern_file_name)
        output = methtools.GeneratedFile(output_file_name);
        self._morph(file_pattern_reader, output, variable_map)
        output.save()

    def _morph(self, pattern_lines_source, output, variable_map, should_evalueate_expressions=True):
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
                        if should_evalueate_expressions:
                            included_file_name = eval(command_text.pop_word(), variable_map)
                            include_file_reader = methtools.FileReader(self.patterns_path + "/" + included_file_name)
                            parameters = eval("{ " + command_text.tail + " }", variable_map)
                            variable_map_with_parameters = { **variable_map, **parameters }
                            self._morph(include_file_reader, buffered_output, variable_map_with_parameters)
                            result_line = buffered_output.get_buffered_last_output() + line.after_expression                    
                        else:
                            result_line = line.before_expression + line.after_expression 
                    # conditionals placing a part of code conditionally: 
                    # ${#if ...} ... ${#end}, or
                    ### ${#if ...} ... ${#else} ... ${#end}
                    elif just_command == "#if":
                        condition = eval(command_text.tail, variable_map)
                        if condition:
                            conditional_input = methtools.FirstReadThis(line.before_expression + line.after_expression, pattern_lines_source)
                            evaluating_block_result = self._morph(conditional_input, output, variable_map, should_evalueate_expressions)
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
                                evaluating_block_result = self._morph(conditional_input, output, variable_map, should_evalueate_expressions)
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
                                evaluating_block_result = self._morph(input_to_evaluate, output, enchaced_variable_map, should_evalueate_expressions)
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
                    if should_evalueate_expressions:
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
