# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import os
import re

# file loaded into memory in forn of list of lines.
# whole file content is read during construction.
# futher modification of file is not reflected in object
class file_lines(list):

    def __init__(self, file_name):
        with open(file_name, encoding = 'utf-8') as file:
            for line in file.readlines():
                self.append(line.rstrip())
     
# class used as accessor to content of the result file 
# (if file exists)
class target_content(file_lines):

    def __init__(self, file_name):
        if os.path.exists(file_name):
            file_lines.__init__(self, file_name)
     
# file to store as result file. File is overwritten 
# when store operation is called
class result_file:

    def __init__(self, file_content):
        self.lines = file_content

    def store(self, file_name):
        with open(file_name, "w", encoding = 'utf-8') as file:
            file.write("\n".join(self.lines))

# line content with additional information
class line_content:

    def __init__(self, text):
        self.text = str(text)
        
    def __str__(self):
        return self.text
        
    def is_persistent_block_begin(self):
        return re.match("^\s*// -vvv.*", self.text)
      
    def is_persistent_block_end(self):
        return re.match("^\s*// -\^\^\^.*", self.text)
        
    def get_placeholder(self):
        return re.search("[$][{][^${}]*[}]", self.text)

# just a class to denote that the code lines should be 
# threated as code, so no decoration between lines is performed
# but the lines are interpreted
class code_block:
    
    def __init__(self, list_od_lines):
        self.list_of_lines = list_od_lines
        
    def get_list_of_lines(self):
        return self.list_of_lines

# just gives string from the list. One by obe
class list_walker:

    def __init__(self, list_of_lines):
        self.lines_array = list_of_lines
        self.lines_count = len(self.lines_array)
        self.current_line = 0
        self.replace_from = None
        
    def is_end(self):
        return (self.current_line == self.lines_count)
    
    def get_line(self):
        if self.is_end():
            return None
        else:
            line = self.lines_array[self.current_line]
            self.current_line = self.current_line + 1
            return line_content(line)
            
    def set_mark_range_to_delete(self):
        self.replace_from = self.current_line - 1
    
    # replace last read line by the given list. It also back line pointer
    # to point to first line of added array
    def push_back(self, lines):
        if self.replace_from is None:
            self.lines_array = self.lines_array[:self.current_line-1] + lines + self.lines_array[self.current_line:]
            self.current_line = self.current_line - 1
        else:
            self.lines_array = self.lines_array[:self.replace_from] + lines + self.lines_array[self.current_line:]
            self.current_line = self.replace_from
            self.replace_from = None
        self.lines_count = len(self.lines_array)

    def go_to_line_with(self, content):
        self.current_line = 0
        while not self.is_end():
            source_line = self.get_line()
            if str(content).strip() == str(source_line).strip():
                break
                
    def go_to_end_of_content_block(self):
        while not self.is_end():
            line = self.get_line()
            if line.is_persistent_block_end():
                break

# main functionality - generator creating output files
class code_generator:

    def __init__(self, global_dictionary):
        self.symbols = {  }
        self.template_file_name = ""
        self.global_dictionary = global_dictionary
        
    def define(self, name, value):
        self.symbols[str(name)] = value
        
    def set_template(self, template_file_name):
        self.template_file_name = template_file_name
     
    def generate(self, result_file_name):
        template = file_lines(self.template_file_name)
        transformed = self._transform(template)
        stored_file = target_content(result_file_name)
        output_content = self._combine_with_user_code(transformed, stored_file)  
        output = result_file(output_content)
        output.store(result_file_name)
        
    def _transform(self, template):
        walker = list_walker(template)
        while not walker.is_end():
            line = walker.get_line()
            replacement = self._process_line(line, walker)
            if not replacement is None:
                walker.push_back(replacement)
        return walker.lines_array
 
    def _combine_with_user_code(self, transformd_template, existing_file):
        generated = list_walker(transformd_template)
        previous = list_walker(existing_file)
        result = [ ]
        while not generated.is_end():
            line = generated.get_line()
            result.append(str(line))
            if line.is_persistent_block_begin():
                previous.go_to_line_with(line)
                if previous.is_end():
                    self._copy_lines(generated, result)
                else:
                    self._copy_lines(previous, result)
                    generated.go_to_end_of_content_block()
        return result

    # transfroms single line. Result is list of result lines to replace passed one
    def _process_line(self, line, source_reader):
        placeholder_match = line.get_placeholder()
        line_text = str(line)
        if placeholder_match:
            before = line_text[:placeholder_match.start(0)]
            after = line_text[placeholder_match.end(0):]
            expression = line_text[placeholder_match.start(0)+2:placeholder_match.end(0)-1]
            if expression.strip()[0] == "#":  # this is not simple expression, but metastatement
                return self._process_metatatement(before, after, expression.strip()[1:], source_reader)
            else:
                value = self._calculate_result(expression)
                return self._combine_lines_from(before, value, after)   
        return None
    
    # calculate result of expression to place in created text
    def _calculate_result(self, expression):
        return eval(expression, self.global_dictionary, self.symbols)

    def _combine_lines_from(self, before, value, after):
        if type(value) is list:
            list_len = len(value)
            if list_len == 0:
                return [ before+after ]
            if list_len == 1:
                return [ before+str(value[0])+after ]
            else:
                result = self._combine_lines_from(before, value[0], ",")
                prefix = self._whitespace_text(before)
                for scalar in value[1:-1]:
                    result = result + self._combine_lines_from(prefix, scalar, ",")
                result = result + self._combine_lines_from(prefix, value[-1], after)
                return result
        elif type(value) is code_block:
            result = [ ]
            for line in value.get_list_of_lines():
                result = result + self._combine_lines_from(before, line, after)
            return result
        else:
            return [ before+str(value)+after ]
            
    def _whitespace_text(self, text):
        return re.sub("\S", " ", text)
    
    def _copy_lines(self, source, target):
        while not source.is_end():
            line = source.get_line()
            target.append(str(line))
            if line.is_persistent_block_end():
                return
    
    # emits lines created returned by metaexpression
    def _process_metatatement(self, before, after, expression, source_reader):
        match = re.search("^\s*IF\s*", expression)
        if match:
            condition = expression[match.end(0):]
            return self._process_meta_IF(condition, before, after, source_reader)            
        #
        #
        #
        #
        #
        #
        source_reader.set_mark_range_to_delete()
        blocks, after = self._read_metastatement_body(after, source_reader)
        block = self._select_metastatement_block(blocks, 0)
        return self._decorate_with_start_end(block, before, after)
        
    def _process_meta_IF(self, condition, before, after, source_reader):
        condition_value = self._calculate_result(condition)
        source_reader.set_mark_range_to_delete()
        blocks, after = self._read_metastatement_body(after, source_reader)
        if condition_value:
            select_block = 0
        else:
            select_block = 1
        block = self._select_metastatement_block(blocks, select_block)
        return self._decorate_with_start_end(block, before, after)    
        
    def _select_metastatement_block(self, blocks, index):
        if index < len(blocks):
            return blocks[index]
        else:
            return [ ]
            
    def _decorate_with_start_end(self, block, before, after):
        if len(block) > 0:
            block[0] = before + block[0]
            block[-1] = block[-1] + after
            return block
        else:
            line = before + after
            if line == "":
                return [  ]
            else:
                return [ line ]
        
    # returns position of metastatement and type of metastatement located in line. Type is
    # denoted as numbers: 
    #   +1: entering scope metastatements (IF, FOR)
    #    0: contunuation of scope (ELSE)
    #   -1: leagind scope (END)
    class _metastatement_location:
    
        def __init__(self, start, end, depth_change):
            self.start = start
            self.end = end
            self.depth_change = depth_change 
            
    def _check_metastatement(self, line, start_at):
        to_search = line[start_at:]
        found = re.search("[$][{]\s*#\s*(IF|ELSE|END|FOR)\s*[^${}]*[}]", to_search)
        if found:
            position = start_at + found.start(0)
            end = start_at + found.end(0)
            metastatement = line[position :end]
            if re.match("[$][{]\s*#\s*FOR.*", metastatement):
                return code_generator._metastatement_location(position, end, +1)
            if re.match("[$][{]\s*#\s*IF.*", metastatement):
                return code_generator._metastatement_location(position, end, +1)
            if re.match("[$][{]\s*#\s*END.*", metastatement):
                return code_generator._metastatement_location(position, end, -1)
            else:
                return code_generator._metastatement_location( position, end, 0) # ("ELSE")
        else:
            return None
    
    def _strip_starting_empty_lines(self, result):
        for i in range(0, len(result)):
            if len(result[i]) > 0:
                if result[i][0] == "":
                    result[i] = result[i][1:]
        return result
    
    def _read_metastatement_body(self, line, source_reader):
        current_level = 1
        result = [ ]
        current_block = [ ]
        check_from_position = 0
        after_metastatement = ""
        begin_of_data = 0
        while True:
            found = self._check_metastatement(line, check_from_position)
            if not found:
                current_block.append(line[begin_of_data:])
                if source_reader.is_end():
                    break
                line = str(source_reader.get_line())
                check_from_position = 0
                begin_of_data = 0
            else:
                if current_level == 1 and found.depth_change <= 0:
                    last_line = line[begin_of_data:found.start]
                    if last_line != "":
                        current_block.append(last_line)
                    after_metastatement = line[found.end:]
                    if found.depth_change == 0:
                        result.append(current_block)
                        current_block = []
                        check_from_position = found.end
                        begin_of_data = found.end
                    else:
                        break
                else:
                    check_from_position = found.end
                    current_level = current_level + found.depth_change
        if current_block != []:
            result.append(current_block)
        return self._strip_starting_empty_lines(result), after_metastatement   
    
# ----------------------------------------------------------
